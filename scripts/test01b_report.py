#!/usr/bin/env python3
"""Combine TEST-01B A/B independent investigations and write factual report."""
import argparse
import datetime as dt
import json
from pathlib import Path

def prepare(a,b,baseline):
    return {"id":"TEST-01B","created_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
            "status":"scientific_review_pending","investigation_a":a,"investigation_b":b,
            "original_holdouts":baseline.get("holdouts",[]),
            "interface_changed":False,"original_test01_files_changed":False,
            "test02_started":False,"scientific_approval":"pending_main_session"}

def make_report(r):
    a,b=r["investigation_a"],r["investigation_b"]
    diags=a.get("evaluations",[])
    br=b.get("retrieval",{})
    lines=["# TEST-01B — Diagnóstico 2025 e levantamento 2026",
      "",
      "Engenharia Stack Manauara · "+r["created_utc"]+" · Aprovação científica pendente da sessão principal.",
      "Interface, dados já publicados e arquivos TEST-01 permanecem sem alteração; TEST-02 não iniciado.",
      "",
      "## A. Por que o WAPE aumentou em 2025?",
      "WAPE é erro absoluto agregado por célula-mês de 1 grau, dividido pelo total MODIS Aqua. Não representa erro contra incêndios confirmados.",
      "Os números abaixo reproduzem os holdouts TEST-01 sem usar o ano avaliado no treino.",
      "",
      "| Treino | Avaliação | Fator | MODIS | NOAA-20 | Previsto | Erro absoluto | WAPE bruto | WAPE ajustado | Viés predito-MODIS |",
      "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for x in diags:
        t=x["totals"]
        lines.append("| {} | {} | {:.8f} | {} | {} | {:.1f} | {:.1f} | {:.2f}% | {:.2f}% | {:+.1f} |".format(
            ",".join(map(str,t["training_years"])),t["year"],t["factor"],t["modis_pixels"],
            t["noaa20_pixels"],t["predicted_pixels"],t["sum_absolute_error_scaled"],
            100*t["raw_wape"],100*t["scaled_wape"],t["signed_bias_pred_minus_modis"]))
    d=a.get("denominator_effect",{})
    lines.extend([
      "",
      "### Efeito do denominador e estabilidade",
      "- Denominador MODIS 2024 = {}; 2025 = {}; queda {}%.".format(
          d.get("modis_2024"),d.get("modis_2025"),d.get("modis_denominator_decline_pct")),
      "- Erro absoluto 2024 = {}; 2025 = {}; variação {}%.".format(
          d.get("abs_error_2024"),d.get("abs_error_2025"),d.get("abs_error_change_pct")),
      "- A redução do denominador torna o WAPE relativo maior mesmo quando o erro absoluto diminui; não atribuir causalidade física sem dados de observação.",
      "- Viés positivo indica superestimação frente ao MODIS; viés negativo, subestimação.",
      "",
      "| Ano | MODIS/NOAA-20 observado (não calibrado para previsão) |",
      "|---|---:|"])
    for year,value in a.get("annual_sensor_ratios",{}).items():
        lines.append("| {} | {:.7f} |".format(year,value["aqua_per_noaa20"]))
    for x in diags:
        lines+=["","### Diagnóstico de erros por mês — "+str(x["totals"]["year"]),
                "| Mês UTC | MODIS | NOAA-20 | Previsto | Erro absoluto | Contribuição WAPE (p.p.) | Parcela erro (%) | Viés |",
                "|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for v in x["monthly"]:
            lines.append("| {} | {} | {} | {:.2f} | {:.2f} | {:.3f} | {:.2f} | {:+.2f} |".format(
                v["month"],v["modis"],v["noaa20"],v["predicted"],v["abs_error"],
                v["wape_contribution_percentage_points"],v["share_of_absolute_error_pct"],v["signed_bias"]))
        lines+=["","### Células com maior erro — "+str(x["totals"]["year"]),
                "| Latitude 1° | Longitude 1° | Erro absoluto |",
                "|---:|---:|---:|"]
        for v in x["spatial_top_30"][:12]:
            lines.append("| {} | {} | {} |".format(v["latitude_cell_south"],v["longitude_cell_west"],v["abs_error"]))
        lines.append("Três meses concentram {}% do erro; dez células concentram {}%.".format(
            x["top_3_months_error_share_pct"],x["spatial_error_top_10_share_pct"]))
    lines+=["","## Auditoria da fonte histórica",
      "Arquivos públicos oficiais NASA FIRMS Brasil 2023–2025 recuperados novamente, cada hash SHA-256 conferido com TEST-01. Filtros diurnos MODIS Aqua >=30 e NOAA20 n/h, type=0 se disponível, mesma geometria simplificada do Amazonas.",
      "| Ano | Sensor | Pixels válidos | SHA-256 | Intervalo dos registros retidos UTC |",
      "|---|---|---:|---|---|"]
    for f in a.get("source_files",[]):
        lines.append("| {} | {} | {} | {} | {} até {} |".format(
            f["year"],f["sensor"],f["counts"]["retained_pixels"],f["sha256"],
            f["first_retained_utc"],f["last_retained_utc"]))
    lines+=["",
      "## B. Recuperação de dados 2026",
      "Fontes oficiais: https://firms.modaps.eosdis.nasa.gov/download/ ; https://firms.modaps.eosdis.nasa.gov/api/data_availability/ ; https://firms.modaps.eosdis.nasa.gov/api/area/ ; https://nrt3.modaps.eosdis.nasa.gov/help/ .",
      "Archive Download por intervalo requer autenticação Earthdata ou e-mail/código e envia instruções posteriores. Nenhum pedido interativo foi falsamente registrado. Arquivo NRT nrt3 exige token Earthdata diferente da MAP_KEY.",
      "Area API foi consultada com segredo FIRMS_MAP_KEY protegido. Consultas limitadas a 5 dias, preferência por SP, NRT somente para dias sem SP, sem mistura na mesma data.",
      "**Estado:** "+br.get("status","não executado"),
      "",
      "| Produto | Disponível de | Até |",
      "|---|---|---|"]
    for prod in ("MODIS_SP","MODIS_NRT","VIIRS_NOAA20_SP","VIIRS_NOAA20_NRT"):
        x=b.get("availability",{}).get(prod,{})
        lines.append("| {} | {} | {} |".format(prod,x.get("min_date","não disponível"),x.get("max_date","não disponível")))
    lines+=["","| Sensor | Dias consultados sem erro | Dias sem fonte na API | Janelas falhas | Pixels válidos obtidos | Processamento |",
            "|---|---:|---:|---:|---:|---|"]
    for name,s in br.get("sensors",{}).items():
        lines.append("| {} | {} | {} | {} | {} | {} |".format(
            name,s.get("source_coverage_query_days",0),len(s.get("unavailable_days",[])),
            len(s.get("failed_windows",[])),s.get("eligible_pixels",0),
            json.dumps(s.get("processing_counts",{}),ensure_ascii=False)))
    lines+=["",
      "Manifests de cada requisição (URL sem chave, datas, versão SP/NRT, hash do corpo, esquema CSV, contagens e erros) estão preservados no JSON. Consultar o último dia não garante que todas as órbitas já passaram.",
      "",
      "### Comparação por período equivalente",
      "Séries históricas foram recortadas em 1º de janeiro–14 de novembro, mesmos dias do calendário, com os mesmos filtros e contorno.",
      "| Ano | MODIS Aqua bruto | NOAA-20 bruto | Origem |",
      "|---|---:|---:|---|"]
    for year,counts in a.get("historical_same_period_2026_candidate",{}).items():
        lines.append("| {} | {} | {} | CSV anual NASA |".format(year,counts["Aqua"],counts["NOAA20"]))
    sensors=br.get("sensors",{})
    complete=(br.get("status")=="all_requested_days_queried" and
              all(sensors.get(k,{}).get("day_catalogue_is_complete",False) for k in ("MODIS_AQUA","NOAA20")))
    if complete:
        lines.append("| 2026 | {} | {} | SP/NRT conforme intervalo, dados provisórios onde NRT |".format(
            sensors["MODIS_AQUA"]["eligible_pixels"],sensors["NOAA20"]["eligible_pixels"]))
        conclusion="PARCIALMENTE, como contagens descritivas por mesmos dias. Diferenças SP/NRT e passagens não aferidas impedem afirmações de anomalias ou de tendência."
    else:
        lines.append("| 2026 | não comparável no período completo | não comparável no período completo | intervalos ausentes ou consultas falhas |")
        conclusion="NÃO para o período integral; fontes ou intervalos insuficientes. Nenhuma data sem consulta foi preenchida com zero."
    lines+=["","**Conclusão sobre comparação 2026:** "+conclusion,
            "",
            "## Fatos, hipóteses e limites",
            "**Fato matemático:** os erros brutos, ajustados e assinados são reproduzidos sobre as mesmas células e anos de avaliação.",
            "**Hipóteses não demonstradas:** causas climáticas, mudança da ocorrência real de incêndios, nuvens, horários de passagem e características instrumentais específicas de 2025.",
            "**Incertezas:** contorno estadual simplificado não auditado contra IBGE oficial; ausência de cobertura clear-sky, diferença entre SP e NRT, latência de disponibilidade e possível mudança de arquivos NRT.",
            "Para o público, só exibir detecções originais com satélite, data, cobertura/versão e ressalvas. Harmonização é exploratória; não afirmar número real de incêndios, risco, previsão ou causa.",
            "",
            "## Decisão TEST-01B e TEST-02",
            "**Status:** relatório técnico produzido; aprovação científica da sessão principal pendente.",
            "**Motivo:** investigar instabilidade em 2025 e recuperar 2026 sem extrapolar dados; aceita-se incerteza em vez de melhorar artificialmente WAPE.",
            "**Evidência:** arquivos NASA com hash, análises temporais por célula/mês, inventário 2026 e execução de testes unitários.",
            "**Riscos:** fontes NRT provisórias, fronteira simplificada, recortes NRT/SP, lacunas de órbita e tempo limitado.",
            "**Próxima validação:** obter geometria IBGE, examinar cobertura de passagens, revisar SP/NRT e repetir métricas independentes.",
            "**Responsável/data:** engenharia Stack Manauara, 14/11/2026.",
            "**TEST-02:** NÃO iniciado; autorização permanece com a sessão principal.",
            "",
            "## Reproduzir",
            "- python -m unittest discover -s tests -v",
            "- python -m scripts.test01b_diagnose --output /tmp/test01b-a.json",
            "- FIRMS_MAP_KEY como segredo de ambiente: python -m scripts.test01b_2026 --output /tmp/test01b-b.json",
            "- python -m scripts.test01b_report --a /tmp/test01b-a.json --b /tmp/test01b-b.json",
            "Nunca registrar chaves ou URLs autenticadas em logs/JSON.",""]
    return "\n".join(lines)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--a",default="/tmp/test01b-a.json")
    p.add_argument("--b",default="/tmp/test01b-b.json")
    p.add_argument("--baseline",default="data/test01_historico_amazonas.json")
    p.add_argument("--output",default="data/test01b_resultados.json")
    p.add_argument("--report",default="docs/TEST-01B_INVESTIGACAO.md")
    args=p.parse_args()
    a=json.loads(Path(args.a).read_text(encoding="utf8"))
    b=json.loads(Path(args.b).read_text(encoding="utf8"))
    baseline=json.loads(Path(args.baseline).read_text(encoding="utf8"))
    r=prepare(a,b,baseline)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.report).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    Path(args.report).write_text(make_report(r),encoding="utf8")
    print("TEST-01B REPORT",args.report,"JSON",args.output,
          "status A",a.get("status"),"status B",b.get("status"),flush=True)

if __name__=="__main__":main()
