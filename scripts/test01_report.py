#!/usr/bin/env python3
"""Create TEST-01 scientific report from the actual NASA FIRMS output JSON."""
import argparse
import json
from pathlib import Path

def fmt_report(data):
    audits=[]
    for f in data.get("file_inventory",[]):
        stats=f.get("rows",{})
        audits.append("| {} | {} | {} | {} | {} | {} | {} |".format(
            f["year"],f["sensor"],f["status"],
            stats.get("retained_pixels","—"),
            f.get("first_retained_utc") or "—",f.get("last_retained_utc") or "—",
            f.get("sha256","—")[:18]))
    holdouts=[]
    for h in data.get("holdouts",[]):
        if h["status"]=="evaluated":
            holdouts.append("| {} | {} | {:.8f} | {:.2f}% | {:.2f}% | {} |".format(
                ",".join(map(str,h["training_years"])),h["holdout_year"],
                h["factor_from_training_only"],h["raw_wape"]*100,h["scaled_wape"]*100,
                h["active_cells_month"]))
        else:
            holdouts.append("| {} | {} | — | — | — | {} |".format(
                ",".join(map(str,h.get("training_years",[]))),h["holdout_year"],h["status"]))
    months=[]
    for y in data.get("historical_comparable_years",[]):
        ms=[x for x in data.get("monthly",[]) if x["year"]==y]
        if ms:
            peak=max(ms,key=lambda x:x["viirs_noaa20"])
            low=min(ms,key=lambda x:x["viirs_noaa20"])
            months.append("- {}: máximo mensal NOAA-20 {} ({:d} pixels); mínimo {} ({:d} pixels).".format(
                y,peak["month"],peak["viirs_noaa20"],low["month"],low["viirs_noaa20"]))
    hot=[]
    for c in data.get("recurring_cells",[])[:10]:
        hot.append("| {} | {} | {} | {} |".format(
            c["cell_south_lat"],c["cell_west_lon"],
            ",".join(map(str,c["active_years"])),c["noaa20_pixels"]))
    complete=(len(data.get("historical_comparable_years",[]))==3 and
              all(h["status"]=="evaluated" for h in data.get("holdouts",[])))
    approval=("PARCIALMENTE APROVADO para histórico exploratório 2023–2025; "
              "NÃO aprovado para comparação 2026") if complete else (
              "NÃO APROVADO para histórico 2023–2026; registros insuficientes")
    geom=data.get("geometry",{})
    comp=data.get("comparison_2026",{})
    sections=[
        "# TEST-01 — Padrões históricos da atividade do fogo no Amazonas",
        "",
        "**Data da execução:** "+data.get("created_utc","—"),
        "**Status recomendado à sessão principal:** "+approval,
        "**Status de processamento:** "+data.get("status","—"),
        "",
        "## Pergunta",
        "O que o histórico de detecções térmicas desta região nos ensina?",
        "Registros mensais e células de 1 grau permitem observar recorrência e meses mais ativos somente quando os arquivos são temporalmente comparáveis. Não comprovam incêndios distintos ou área queimada.",
        "",
        "## Fonte e arquivos realmente examinados",
        "NASA FIRMS Country Annual CSV: https://firms.modaps.eosdis.nasa.gov/data/country/",
        "Download anual direto, com hash SHA-256, contagem e período máximo/mínimo dos pixels retidos. HTTP 404 é registrado de modo diferente de falhas de rede.",
        "",
        "| Ano | Sensor | Resultado | Pixels retidos | Primeiro UTC | Último UTC | SHA-256 prefixo |",
        "|---|---|---|---:|---|---|---|",
        *audits,
        "",
        "## Região e método",
        "**Geometria utilizada:** "+geom.get("label","—"),
        "**Fonte do contorno:** "+geom.get("source","—"),
        "**Hash do contorno:** "+geom.get("boundary_sha256","—"),
        "**Tentativa IBGE oficial:** "+json.dumps(geom.get("official_attempt",{}),ensure_ascii=False),
        "",
        "MODIS Aqua, confidence >=30; VIIRS NOAA-20, confidence n/h; type=0 quando disponível; apenas D (diurno); pontos dentro do polígono; células espaciais de 1 grau; mês UTC.",
        "Diferença justificada do VAL-TRAD-02: uso de mês UTC em vez de solar local para evitar ano solar truncado sem arquivos adjacentes. Os WAPEs deste estudo não devem ser comparados diretamente aos dos recortes retangulares A/B.",
        "Fator global = soma MODIS em anos de treino / soma NOAA-20 nos mesmos anos. Validações temporais: 2023→2024 e 2023+2024→2025, **sem utilizar o ano de avaliação para calibrar**.",
        "WAPE = soma dos erros absolutos por célula mensal / soma de pixels MODIS Aqua. Não é erro contra incêndios físicos.",
        "",
        "## Meses com mais e menos detecções (NOAA-20, diurno)",
        *(months or ["Não demonstrável: anos históricos com sensores completos insuficientes."]),
        "",
        "## Escala das contagens: teste independente",
        "| Treino | Teste | Fator global | WAPE bruto | WAPE ajustado | Células-mês ativas / status |",
        "|---|---|---:|---:|---:|---|",
        *holdouts,
        "",
        "## Células recorrentes de 1 grau (NOAA-20)",
        "Recorrência significa pixels detectados em >=2 anos, não o mesmo incêndio.",
        "| Latitude sul da célula | Longitude oeste da célula | Anos | Pixels NOAA-20 |",
        "|---|---|---|---:|",
        *(hot or ["| — | — | — | — |"]),
        "",
        "## Comparação com 2026",
        "**Resultado:** "+comp.get("status","—"),
        "**Justificativa:** "+comp.get("reason","—"),
        "A consulta atual NRT de dois dias não preenche a lacuna janeiro–novembro. Mesmo que exista arquivo anual parcial 2026, é necessário recortar novembro dos outros anos até o mesmo dia antes de comparar; o presente pipeline não atribui anomalias 2026 sem esse teste.",
        "2026 não é automaticamente padrão de ciência consolidado: https://firms.modaps.eosdis.nasa.gov/download/",
        "",
        "## Observações",
        *["- "+x for x in data.get("observations",[])],
        "## Interpretações e hipóteses (não observações comprovadas)",
        *["- Interpretação: "+x for x in data.get("inferences",[])],
        *["- Hipótese: "+x for x in data.get("hypotheses",[])],
        "",
        "## Limitações",
        *["- "+x for x in data.get("limitations",[])],
        "- Dados ausentes não significam zero deteccões nem ausência de fogo.",
        "- Sem ajuste NOAA-20→NOAA-21; sem validação de qualidade do ar ou causa de fogo.",
        "",
        "## Rastreabilidade e decisão",
        "**ID:** TEST-01. **Status:** revisão científica pendente da sessão principal.",
        "**Responsável/data:** engenharia Stack Manauara, 14/11/2026.",
        "**Motivo:** testar calendário do Amazonas sem transferir coeficientes experimentais A/B.",
        "**Alternativas:** reutilizar A/B (rejeitado), anual por país (adotado), NRT isolado (não serve para histórico completo).",
        "**Riscos:** sensibilidade e passagem dos sensores, nuvens, polígono simplificado, arquivos 2026 incompletos, somente 3 anos históricos.",
        "**Validação:** dados com proveniência e hashes, WAPE em anos separados, testes automatizados e período equivalente.",
        "**TEST-02:** não iniciar. Detecção sem registro no período analisado não é incêndio novo nem prova ausência anterior.",
        "",
        "## Reprodução",
        "python -m unittest discover -s tests -v",
        "python -m scripts.test01_historico --output data/test01_historico_amazonas.json",
        "python -m scripts.test01_report --input data/test01_historico_amazonas.json --output docs/TEST-01_HISTORICO.md",
        "Arquivos do site e data/historico.json permanecem inalterados.",
        ""
    ]
    return "\n".join(sections)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/test01_historico_amazonas.json")
    p.add_argument("--output",default="docs/TEST-01_HISTORICO.md")
    a=p.parse_args()
    data=json.loads(Path(a.input).read_text(encoding="utf8"))
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(fmt_report(data),encoding="utf8")
    print("REPORT",a.output,"status",data.get("status"))

if __name__=="__main__":
    main()
