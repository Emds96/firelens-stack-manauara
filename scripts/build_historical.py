#!/usr/bin/env python3
"""Export 2022-2024 monthly series from the *same* aggregate as VAL-TRAD-02.
Requires six official Brazil annual CSVs in --cache (or internet).
Does not conceal incomplete December local-solar boundary without adjacent 2025 UTC file.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts import firms_nrt  # for status consistency (stdlib only)
from docs.research import validacao_tradutor1_reproduzivel as original


def build(cache, validation_path):
    validation=json.loads(Path(validation_path).read_text(encoding='utf8'))
    experiments={}
    records=defaultdict(int)
    files=[]
    for year in (2022,2023,2024):
        for satellite in ('modis','viirs-jpss1'):
            stats=Counter()
            original.ingest(year,satellite,cache,records,stats)
            files.append({'year':year,'satellite':satellite,**dict(stats)})
    for region in ('A','B'):
        for year in (2023,2024):
            years=[2022] if year==2023 else [2022,2023]
            experiment=original.evaluate(records,region,'D',years,year)
            target=next(x for x in validation['daytime_holdouts'] if x['region']==region and x['test']==year)
            if experiment['methods']['global']['WAPE'] != target['global']['WAPE']:
                raise RuntimeError(f"Validação histórica não reproduzida: {region}/{year}; calc={experiment['methods']['global']['WAPE']} ref={target['global']['WAPE']}")
            experiments[(region,year)]=experiment
    months=[]
    for region in ('A','B'):
        for year in (2022,2023,2024):
            for month in range(1,13):
                modis=sum(count for (r,s,d,y,m,*cell),count in records.items() if r==region and s=='Aqua' and d=='D' and y==year and m==month)
                viirs=sum(count for (r,s,d,y,m,*cell),count in records.items() if r==region and s=='NOAA20' and d=='D' and y==year and m==month)
                factor=experiments[(region,year)]['global_coefficient'] if year>=2023 else None
                months.append({'region':region,'year':year,'month':month,'modis_aqua':modis,
                               'viirs_noaa20':viirs,
                               'viirs_in_modis_scale':round(viirs*factor,2) if factor is not None else None,
                               'global_factor':factor,
                               'complete_local_solar_month':month != 12,
                               'caveat': 'Dezembro potencialmente incompleto: faltam observações UTC do ano seguinte' if month==12 else None})
    return {'schema_version':1,'status':'ready','area':'Recortes retangulares experimentais A e B (não equivalem ao Amazonas)',
            'source':'NASA FIRMS country yearly Brazil, arquivo histórico consolidado',
            'source_url':'https://firms.modaps.eosdis.nasa.gov/data/country/',
            'years':[2022,2023,2024], 'time_basis':'mês solar local (UTC + longitude/15 horas)',
            'filters':'type=0 when available; Aqua confidence>=30; NOAA20 n/h; somente diurno D',
            'aggregation':'Contagens de pixels em células de 1° por mês; NÃO incêndios individuais',
            'method':'Fator global NOAA20->MODIS Aqua treinado em anos anteriores; nunca no ano de teste',
            'regions':original.REGIONS,'files':files,'months':months,
            'warnings':['O período 2022-2024 não representa a série histórica 2000-2026.',
                        'Dezembro pode estar incompleto por cruzamento de ano UTC/solar; não utilizar sem ressalva.',
                        'WAPE original é calculado em células mensais 1°, NÃO pelo gráfico de totais mensais.']}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache',type=Path,default=Path('firms_cache'))
    parser.add_argument('--validation',type=Path,default=Path('data/validacao.json'))
    parser.add_argument('--output',type=Path,default=Path('data/historico.json'))
    args=parser.parse_args()
    result=build(args.cache,args.validation)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Séries mensais geradas e métricas verificadas em data/validacao.json')


if __name__=='__main__':
    main()
