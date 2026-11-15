#!/usr/bin/env python3
"""Produce evidence-only TEST-02 report from real published observation JSON."""
import argparse
import json
from pathlib import Path

CATS=[
 ("four_locks_compatible_unconfirmed","1. Quatro critérios compatíveis (candidato, NÃO confirmado)"),
 ("spatial_overlap_delayed_unconfirmed","2. Sobreposição e intervalo >120 min"),
 ("edge_near_modis_no_expansion_proof","3. Borda: fora da caixa, até 2,5 km"),
 ("viirs_spatially_isolated_not_proven_invisible","4. VIIRS isolado (>2,5 km de qualquer caixa MODIS)"),
 ("unresolved_ambiguous_or_lock_failure","5. Ambíguo / critério não atendido"),
 ("unresolved","5b. Indeterminado")
]

def fmt(x,n=2):
    return "—" if x is None else (f"{x:.{n}f}" if isinstance(x,float) else str(x))

def rows_md(rows,limit=None):
    r=rows[:limit] if limit is not None else rows
    lines=["| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |",
           "|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|"]
    for x in r:
        signal="367 K" if x["i4_saturation"] else "<250 K" if x["i4_possible_folding"] else "—"
        lines.append("| {} | {} | {} | {} | {} | {} | {}×{} | {} | {} | {} | {} | {} | {} |".format(
          x["id"],x["satellite"],x["time_utc"][11:16],x["time_manaus"][11:16],
          fmt(x["latitude"],5),fmt(x["longitude"],5),
          fmt(x["scan_km"]),fmt(x["track_km"]),fmt(x["area_km2_approx"],4),
          fmt(x["t4_k"]),fmt(x["t11_k"]),fmt(x["frp_mw"]),x["confidence"],signal))
    if limit and len(rows)>limit:lines.append(f"\nDetalhe completo de outras {len(rows)-limit} observações no JSON original separado.")
    return "\n".join(lines)

def generate(r,observations,baseline):
    mod=observations["MODIS_NRT"];vrs=observations["VIIRS_NOAA20_NRT"]
    d11=next(d for d in r["daily"] if d["date_utc"]=="2026-11-11")
    original=baseline.get("investigation_b",{}).get("retrieval",{}).get("sensors",{})
    ref_a=original.get("MODIS_AQUA",{}).get("daily_counts",{}).get("2026-11-11")
    ref_v=original.get("NOAA20",{}).get("daily_counts",{}).get("2026-11-11")
    recalc_a=d11["eligible_diurnal_modis_aqua"];recalc_v=d11["eligible_diurnal_noaa20"]
    comparable=(recalc_a==ref_a and recalc_v==ref_v)
    daymod=sorted([m for m in mod if m["date_utc"]=="2026-11-11"],
                  key=lambda z:(z["satellite"],z["time_utc"],z["latitude"],z["longitude"]))
    dayv=sorted([v for v in vrs if v["date_utc"]=="2026-11-11"],
                key=lambda z:(z["time_utc"],z["latitude"],z["longitude"]))
    L=[
      "# TEST-02 — Visão da Águia: análise físico-espacial, 10–14/11/2026",
      "",
      "**Engenharia Stack Manauara | Experimento exploratório | Aprovação científica pendente**",
      "**Executado UTC:** "+r["fetched_at_utc"],
      "",
      "## Veredito",
      "",
      "**A concordância de posição, horário, temperatura e FRP indica possíveis associações, mas NÃO confirma a identidade de um único incêndio e NÃO autoriza fundir pixels automaticamente.**",
      "scan × track é apenas dimensão aproximada; caixas alinhadas à latitude/longitude não são os verdadeiros footprints orientados obtidos de geolocalização Level-2. Limites de 5–8 K e razão FRP entre 0,5 e 2,0 são exploratórios, não critérios NASA validados.",
      "",
      "## NASA FIRMS, registros originais e contorno",
      "",
      "Fonte: https://firms.modaps.eosdis.nasa.gov/api/area/ ; MODIS_NRT (Aqua e Terra) e VIIRS_NOAA20_NRT. Início 2026-11-10, duração 5 dias; todo o Amazonas segundo polígono simplificado. BBox de atenção Manaus/Autazes/Careiro: W -61,5, S -4,5, E -58,5, N -2,0.",
      "",
      "| Produto NASA | Linhas brutas CSV | Linhas retidas no Amazonas | Registros de 11/11 | SHA-256 CSV |",
      "|---|---:|---:|---:|---|"]
    for source,rows in (("MODIS_NRT",mod),("VIIRS_NOAA20_NRT",vrs)):
        meta=r["sources"][source]
        L.append("| {} | {} | {} | {} | {} |".format(
          source,meta["raw_csv_rows"],len(rows),
          sum(x["date_utc"]=="2026-11-11" for x in rows),meta["sha256_csv"]))
        L.append("Colunas preservadas de "+source+": "+", ".join(meta["csv_columns"])+".")
    L+=["",
      "Todas as colunas físicas originais de cada linha dentro do polígono estão em data/test02_observacoes_20261110_14.json como raw_columns; juntamente com UTC, AMT, flag de saturação, área aproximada e identificadores locais. Nenhuma credencial foi salva.",
      "",
      "## Dia 11/11/2026: contagem de pixels, NÃO incêndios",
      "",
      "| Instrumento | Todas as observações e turnos | Elegíveis diurnas com filtros TEST-01B |",
      "|---|---:|---:|",
      "| MODIS Aqua | {} | {} |".format(d11["modis_aqua"]["n"],recalc_a),
      "| MODIS Terra | {} | fora do filtro Aqua histórico |".format(d11["modis_terra"]["n"]),
      "| VIIRS NOAA-20 | {} | {} |".format(d11["noaa20_total"]["n"],recalc_v),
      "",
      "Comparação com TEST-01B: NOAA-20 {} e Aqua {}. Reprodução das contagens diurnas: **{}**.".format(ref_v,ref_a,"sim" if comparable else "não — investigar revisão NRT/esquema/filtros"),
      "Não há dados aqui que comprovem o pico de fumaça em Manaus nem a origem da poluição.",
      "",
      "### MODIS Aqua e Terra em 11/11: dados por observação",
      "",
      rows_md(daymod,100),
      "",
      "### NOAA-20 em 11/11: primeiras 25 linhas; todas no JSON",
      "",
      rows_md(dayv,25),
      "",
      "## Quatro travas testadas",
      "",
      "1. ΔX=|Δlongitude| × 111,32 × cos(latitude média) e ΔY=|Δlatitude| × 110,57, em km; encaixe aproximado se ΔX≤(scan_M+scan_V)/2 e ΔY≤(track_M+track_V)/2.",
      "2. Mesma data e turno D/N; Δt≤120 min classifica vizinhança temporal, >120 min classifica sobreposição defasada. Não existe uma janela orbital universal para todas as passagens.",
      "3. ΔT11=|bright_t31_MODIS−média(bright_ti5_VIIRS)| apenas dos pixels da caixa e janela; 5 K e 8 K usados como análise de sensibilidade.",
      "4. Razão FRP=ΣFRP_VIIRS associados / FRP_MODIS. Usamos intervalo exploratório 0,5–2,0; FRP é potência radiativa instantânea, não energia conservada. Sobreposições entre caixas podem reutilizar o mesmo VIIRS e são sinalizadas.",
      "",
      "### Grupos reais MODIS ↔ VIIRS (exemplos por hora e localização)",
      ""]
    group_examples=r["examples_2026_11_11"]["blocks"]
    if not group_examples:L.append("Nenhum grupo de encaixe espacial aproximado encontrado no dia 11 sob os critérios.")
    for item in group_examples[:6]:
        m=item["modis"];g=item["group"]
        L.extend([
          "#### {} / {} / UTC {} (AMT {})".format(m["id"],m["satellite"],m["time_utc"],m["time_manaus"]),
          "MODIS: coordenadas ({}, {}), dimensões {}×{} km (área ~{} km²); T4 {} K, T11 {} K, FRP {} MW.".format(
           fmt(m["latitude"],5),fmt(m["longitude"],5),fmt(m["scan_km"]),fmt(m["track_km"]),
           fmt(m["area_km2_approx"],3),fmt(m["t4_k"]),fmt(m["t11_k"]),fmt(m["frp_mw"])),
          "VIIRS dentro da caixa e ≤120 min: {}; >120 min: {}; TI5 média {} K; ΔT11 {} K; ΣFRP {} MW; razão VIIRS/MODIS {}; 4 critérios a 8 K: **{}**.".format(
            len(g["in_box_and_within_120min_ids"]),len(g["in_box_over_120min_ids"]),
            fmt(g["viirs_t11_mean_k"]),fmt(g["delta_t11_k"]),fmt(g["viirs_frp_sum_mw"]),
            fmt(g["frp_ratio_viirs_to_modis"],3),
            "compatível, NÃO confirmado" if g["four_locks_candidate_8k"] else "não passou"),
          "",
          rows_md(item["viirs_rows"],30),
          ""
        ])
    L+=["",
      "### Dois grupos de 10/11 com os quatro critérios exploratórios compatíveis",
      "",
      "O dia 11 não teve grupos em até 120 minutos. No dia anterior, os seguintes grupos VIIRS–Aqua são candidatos para verificação posterior com geolocalização Level-2, **não incêndios confirmados**.",
      ""]
    modmap={m["id"]:m for m in mod}
    viirsmap={v["id"]:v for v in vrs}
    strong10=[g for g in r["group_diagnostics"]
              if g["modis_time_utc"].startswith("2026-11-10") and
              g["four_locks_candidate_8k"]]
    for g in strong10:
        m=modmap[g["modis_id"]]
        associated=[viirsmap[v] for v in g["in_box_and_within_120min_ids"]]
        L += ["**{} / {}**: UTC {}, AMT {}, coord ({}, {}), scan×track {}×{} km, "
              "FRP MODIS {} MW, T31 {} K; VIIRS {} pixels, ΣFRP {} MW, média TI5 {} K, "
              "ΔT11 {} K, razão {}, Δt {} minutos.".format(
              m["id"],m["satellite"],m["time_utc"],m["time_manaus"],
              fmt(m["latitude"],5),fmt(m["longitude"],5),
              fmt(m["scan_km"]),fmt(m["track_km"]),fmt(m["frp_mw"]),
              fmt(m["t11_k"]),len(associated),fmt(g["viirs_frp_sum_mw"]),
              fmt(g["viirs_t11_mean_k"]),fmt(g["delta_t11_k"]),
              fmt(g["frp_ratio_viirs_to_modis"],3),
              int(round(abs((__import__("datetime").datetime.fromisoformat(m["time_utc"].replace("Z","+00:00"))-
                 __import__("datetime").datetime.fromisoformat(associated[0]["time_utc"].replace("Z","+00:00"))).total_seconds()/60)))
              ),"",rows_md(associated),""]
    if not strong10:L.append("Nenhum grupo de 10/11 passou nas quatro travas exploratórias.")
    L+=["",
      "### Exemplos de detecções VIIRS distantes das caixas MODIS",
      "",
      rows_md(r["examples_2026_11_11"]["isolated_viirs_examples"]),
      "",
      "## Classificação exclusiva das observações NOAA-20, 11/11",
      "",
      "As quatro classes sugeridas foram mantidas como hipóteses, acrescidas da classe de falha/ambiguidade para não forçar classificação indevida. A primeira é CANDIDATA e não significa incêndio confirmado.",
      "",
      "| Classe de pixel VIIRS | N | FRP médio MW | Área média aprox. km² | T4 média K | T11 média K | I4=367 | I4<250 |",
      "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for key,name in CATS:
        x=d11["categories_viirs_mutually_exclusive"][key]
        L.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
          name,x["n"],fmt(x["frp_avg_mw"]),fmt(x["area_avg_km2_approx"],3),
          fmt(x["t4_avg_k"]),fmt(x["t11_avg_k"]),x["i4_saturation_count"],x["i4_folding_candidate_count"]))
    L+=["",
      "### Somente NOAA-20 elegível diurno — universo dos 222 pixels do TEST-01B",
      "",
      "| Classe VIIRS elegível (n/h, D) | N | FRP médio MW | Área média aprox. km² | T4 média K | T11 média K |",
      "|---|---:|---:|---:|---:|---:|"]
    for key,name in CATS:
        v=d11["eligible_diurnal_viirs_categories"][key]
        L.append("| {} | {} | {} | {} | {} | {} |".format(
            name,v["n"],fmt(v["frp_avg_mw"]),fmt(v["area_avg_km2_approx"],3),
            fmt(v["t4_avg_k"]),fmt(v["t11_avg_k"])))
    L+=["",
      "**Controle:** {} detecções elegíveis; a soma por classe é {}.".format(
          recalc_v,d11["eligible_categories_sum_check"]),
      "",
      "### Entorno Manaus / Autazes / Careiro — caixa geográfica solicitada",
      "",
      "No dia 11, na BBOX local: {} pixels MODIS de todas as plataformas/turnos e {} pixels NOAA-20 de todas as confianças/turnos. Esses números não representam a quantidade de fumaça ou área queimada.".format(
          d11["focus_bbox_counts"]["modis_all"],d11["focus_bbox_counts"]["noaa20_all"]),
      "",
      "| Classe VIIRS na BBOX local | N | FRP médio MW | T4 média K | T11 média K |",
      "|---|---:|---:|---:|---:|"]
    for key,name in CATS:
        v=d11["focus_bbox_viirs_categories"][key]
        L.append("| {} | {} | {} | {} | {} |".format(
            name,v["n"],fmt(v["frp_avg_mw"]),fmt(v["t4_avg_k"]),fmt(v["t11_avg_k"])))
    L += ["",
      "**Controle da área local:** soma de classes = {}.".format(
          d11["focus_categories_sum_check"]),
      "",
      "### Pares geométricos por linha — 11/11/2026, sem fusão",
      "",
      "Cada linha permite reconstituir a relação centro-a-centro (ΔX, ΔY), intervalo UTC entre passagens e motivo da associação. Inclui pares defasados e de borda mesmo quando nenhuma dupla cumpre as quatro travas.",
      "",
      "| MODIS ID / plataforma | VIIRS ID | Δt min | ΔX km | ΔY km | Dist. entre centros km | Fora da borda km | Encaixe | Tipo da associação |",
      "|---|---|---:|---:|---:|---:|---:|---|---|"]
    modmap={m["id"]:m for m in mod}
    for p in r.get("pair_diagnostics_2026_11_11",[]):
        m=modmap[p["modis_id"]]
        L.append("| {} / {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
          p["modis_id"],m["satellite"],p["viirs_id"],fmt(p["minutes"],1),
          fmt(p["dx_km"],3),fmt(p["dy_km"],3),fmt(p["distance_center_km"],3),
          fmt(p["distance_from_box_km"],3),
          "sim" if p["inside_approx_box"] else "não",p["relationship"]))
    if not r.get("pair_diagnostics_2026_11_11"):
        L.append("| — | — | — | — | — | — | — | — | nenhum par na janela |")
    L+=["",
      "**Exclusividade e soma:** {} / {} pixels, conferência: {}. "
      "Grupos MODIS que passaram nas quatro travas (5 K / 8 K): {} / {}. Pixels VIIRS associados a múltiplas caixas MODIS: {} na janela total.".format(
       sum(x["n"] for x in d11["categories_viirs_mutually_exclusive"].values()),
       d11["noaa20_total"]["n"],d11["all_categories_sum_check"],
       d11["four_locks_candidate_groups_5k"],d11["four_locks_candidate_groups_8k"],
       r["viirs_multi_MODIS_spatiotemporal_overlap_count"]),
      "A categoria 4 usa distância >2,5 km da borda das caixas aproximadas MODIS na mesma data, não distância entre centros. Ela NÃO demonstra detecção impossível pelo MODIS, fogo menor, incêndio de sub-bosque ou fumaça originada desse local.",
      "",
      "## Comparação da janela completa (10–14/11)",
      "",
      "| Data UTC | Aqua | Terra | NOAA-20 total | Aqua diurno | NOAA-20 diurno | Grupos 4 travas (8 K) | VIIRS isolados |",
      "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for d in r["daily"]:
        isolated=d["categories_viirs_mutually_exclusive"]["viirs_spatially_isolated_not_proven_invisible"]["n"]
        L.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
          d["date_utc"],d["modis_aqua"]["n"],d["modis_terra"]["n"],
          d["noaa20_total"]["n"],d["eligible_diurnal_modis_aqua"],
          d["eligible_diurnal_noaa20"],d["four_locks_candidate_groups_8k"],isolated))
    L+=["",
      "## Ciência, limitações e decisão TEST-02",
      "",
      "**Fatos verificáveis:** CSVs de origem com hashes, atributos físicos originais, turnos e horários UTC/AMT, áreas nominais, relações espaciais aproximadas, diferenças térmicas, FRP e grupos de observações.",
      "**Limitações científicas:** caixas não correspondem às geometrias orientadas Level-2; T31 e TI5 são temperaturas de brilho de pixels detectados, não temperaturas puras de fundo não queimado; FRP instantâneo não é energia conservada; saturação/folding I4 exige qualidade/radiância para confirmação; há possível sobreposição e dupla contagem. NASA FIRMS não comprova céu limpo, ausência de incêndio, ar poluído nem causalidade da fumaça.",
      "**Decisão TEST-02 / status:** realizado como ensaio descritivo, identidade de um único incêndio NÃO validada; aprovação científica pendente da sessão principal. Alternativas: fusão direta de contagens pelos quatro critérios (não justificada); estudo dos candidatos com órbitas/footprints Level-2 e máscaras de nuvens (recomendado se aprovado).",
      "**Riscos:** confusão entre pixel e incêndio físico, NRT mutável, geometria estadual simplificada, distância temporal e FRP, diferença de sensores. Validação futura: swaths de órbita, geolocalização real e dados independentes.",
      "**Responsável/data:** Engenharia Stack Manauara, 14/11/2026. Nenhuma alteração em TEST-01/01B/SCI-03 nem no frontend.",
      "",
      "## Execução reproduzível",
      "",
      "python -m unittest discover -s tests -v",
      "FIRMS_MAP_KEY como variável de ambiente protegida: python -m scripts.test02_fisico",
      "python -m scripts.test02_report",
      "O relatório e os dados separados foram produzidos pelo workflow TEST-02, usando o segredo protegido; a chave não faz parte de nenhum artefato.",
      ""
    ]
    return "\n".join(L)

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--observations",default="data/test02_observacoes_20261110_14.json")
    a.add_argument("--results",default="data/test02_resultados.json")
    a.add_argument("--baseline",default="data/test01b_resultados.json")
    a.add_argument("--output",default="docs/TEST-02_VISAO_AGUIA.md")
    x=a.parse_args()
    res=json.loads(Path(x.results).read_text())
    rows=json.loads(Path(x.observations).read_text())
    baseline=json.loads(Path(x.baseline).read_text())
    target=Path(x.output)
    target.parent.mkdir(exist_ok=True,parents=True)
    target.write_text(generate(res,rows,baseline),encoding="utf8")
    print("TEST02 REPORT",target,"bytes",target.stat().st_size,flush=True)
if __name__=="__main__":main()
