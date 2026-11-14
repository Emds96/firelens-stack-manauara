# SCI-03 — Relative thermal-activity patterns, MODIS Aqua and VIIRS NOAA-20

Stack Manauara · FireLens · 14/11/2026 · **Scientific decision pending main session**

## Resumo executivo — Português (Brasil)

**Conclusão:** a normalização relativa dos focos por mês/célula ajuda a comparar a distribuição de detecções MODIS/VIIRS, mas **não é uma harmonização física validada nem comprovadamente superior ao fator global**.

Em **2026 (janeiro–outubro completo)**: 8.002 pixels MODIS Aqua e 42.636 NOAA-20; Spearman mensal 0,948 e espacial 0,925; as dez células mais ativas compartilharam oito posições geográficas. Setembro foi o mês mais ativo dos dois sensores. Entretanto, entre janeiro e julho, apesar de ambos serem SP, Spearman espacial caiu para 0,628 (264 pixels MODIS), revelando concordância não uniforme.

Em **2025**: Spearman mensal 0,976 e espacial 0,918; 8/10 células em comum. Isso **não contradiz** o WAPE anual absoluto de 50,73% — as métricas respondem a perguntas distintas. No controle de contagem absoluta apenas janeiro–outubro, WAPE foi 22,09% em 2024 e 47,49% em 2025, com treinamento em anos anteriores.

**Ressalvas:** novembro 2026 foi excluído por incompletude; agosto 2026 mistura MODIS SP/NOAA-20 NRT e setembro–outubro usa NRT/NRT; falta `type` no NRT consultado. Não inferir incêndios individuais, risco, tendências, causas ou cobertura contínua. Os resultados são exploratórios, não devem aparecer no site sem revisão da sessão principal.

**Evidência:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43653164498 — 35 testes automatizados e fontes oficiais reconsultadas, com hashes por arquivo/janela em `data/sci03_resultados.json`.

## Conclusion first

**Relative normalization is defensible as DESCRIPTIVE pattern comparison, not yet a validated harmonization or demonstrated improvement in physical fire estimates.** A global positive multiplicative adjustment leaves shares, ranks and top-k unchanged by algebra. Thus identical relative pattern scores after global scaling cannot establish superiority of a new correction method.

## 2026 prioritized — 1 January through 31 October, UTC, closed months

FIRMS Area API was used for non-overlapping source/product date ranges; every response is listed with SHA-256, sanitized URL, SP/NRT category and CSV attributes in the accompanying JSON. Dates of query availability do not prove cloud-free overpasses or continuous physical coverage.

Jan–Jul both SP; Aug MODIS SP and NOAA-20 NRT; Sep–Oct both NRT. November 2026 excluded as incomplete. The type attribute is not present in observed NRT rows; vegetated-fire filtering differs from SP records.

| 2026 scope | MODIS pixels | NOAA-20 pixels | Monthly TV | Spatial TV | Spatial Spearman | Shared top-10 1-degree cells |
|---|---:|---:|---:|---:|---:|---:|
| jan_oct (SP+NRT/varies_by_sensor) | 8002 | 42636 | 0.077 | 0.113 | 0.925 | 8 |
| sp_sp_jan_jul (SP/SP) | 264 | 2098 | 0.062 | 0.333 | 0.628 | 6 |
| mixed_august (SP/NRT) | 2153 | 10451 | — | 0.129 | 0.896 | 9 |
| nrt_nrt_sep_oct (NRT/NRT) | 5585 | 30087 | 0.082 | 0.119 | 0.921 | 9 |

TV is total variation distance: 0=identical normalized distribution, 1=disjoint. Spearman rho measures rank agreement. For a single month (August), temporal agreement is not informative. Neither metric measures error against individual fires.

## Ranking of most observed months and 1-degree cells (2025 and 2026)

### 2025 — January through October
- **Aqua**: highest monthly shares: month 08: 1765 (44.8%); month 09: 891 (22.6%); month 10: 825 (20.9%). Most active cells: 1° cell southwest (-8,-64): 375 (9.5%); 1° cell southwest (-7,-60): 228 (5.8%); 1° cell southwest (-4,-60): 208 (5.3%).
- **NOAA20**: highest monthly shares: month 08: 7534 (39.6%); month 10: 4812 (25.3%); month 09: 4401 (23.1%). Most active cells: 1° cell southwest (-8,-64): 1213 (6.4%); 1° cell southwest (-7,-60): 1102 (5.8%); 1° cell southwest (-10,-66): 1040 (5.5%).

### 2026 — January through October
- **Aqua**: highest monthly shares: month 09: 3518 (44.0%); month 08: 2153 (26.9%); month 10: 2067 (25.8%). Most active cells: 1° cell southwest (-4,-60): 871 (10.9%); 1° cell southwest (-7,-60): 744 (9.3%); 1° cell southwest (-4,-62): 461 (5.8%).
- **NOAA20**: highest monthly shares: month 09: 16489 (38.7%); month 10: 13598 (31.9%); month 08: 10451 (24.5%). Most active cells: 1° cell southwest (-4,-60): 4155 (9.7%); 1° cell southwest (-7,-60): 3715 (8.7%); 1° cell southwest (-4,-59): 2863 (6.7%).

## Independent years: descriptive agreement 2023, 2024, 2025, 2026

Each year is evaluated independently; no coefficient is fitted using its observations for held-out WAPE. Share distributions are normalized per sensor within the observed window for descriptive comparisons, **not** a predictive calibration. Same geographic 1° cells and UTC January–October months for all four years.

| Year | MODIS pixels | NOAA-20 pixels | TV months | JS divergence months (bits) | Spearman months | TV spatial | Spearman spatial | Shared top-10 spatial |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 17468 | 70276 | 0.054 | 0.004 | 0.976 | 0.078 | 0.972 | 7 |
| 2024 | 22300 | 87776 | 0.015 | 0.000 | 0.988 | 0.077 | 0.959 | 9 |
| 2025 | 3941 | 19017 | 0.060 | 0.004 | 0.976 | 0.139 | 0.918 | 8 |
| 2026 | 8002 | 42636 | 0.077 | 0.005 | 0.948 | 0.113 | 0.925 | 8 |

JS is Jensen–Shannon divergence in bits, 0=identical. Rank correlation and TV are distinct from accuracy of estimated fire counts.

## Control: absolute-count global scaling, fitted only on earlier years

| Prior training years | Held-out year | Global factor (Jan–Oct) | Raw WAPE | Scaled WAPE |
|---|---:|---:|---:|---:|
| 2023 | 2024 | 0.24856281 | 294.56% | 22.09% |
| 2023,2024 | 2025 | 0.25161339 | 384.42% | 47.49% |

These WAPEs were computed for January–October only and DO NOT replace original full-year TEST-01 values (2024 23.11%; 2025 50.73%). They are absolute count errors relative to MODIS observations, **not** directly comparable numerically with TV, JS or Spearman. No 2026 WAPE was computed with the old factor because the SP/NRT mix and missing NRT type field prevent claiming equivalent processing.

## Method and reproducibility

1. Redownload annual NASA FIRMS Brazil CSVs 2023–2025, verify original SHA-256 and annual eligible counts against TEST-01; clip Jan–Oct.
2. Requery 2026 NASA FIRMS Area API using dates and SP-preferred, NRT-gap-filling source selection, in 1–5 day disjoint windows. Exclude November.
3. Filter MODIS Aqua confidence ≥30, NOAA-20 n/h, daytime D, type=0 if available, inside simplified Amazonas polygon; aggregate 1° × UTC month.
4. Compute relative share in a year/period = native sensor pixel count in a month/cell divided by that same sensor's total in period. Then compute TV, Jensen–Shannon divergence, Spearman on union of active categories, and overlap among top 10 1-degree spatial cells.
5. Evaluate global factor trained only on earlier years on historical independent years 2024/2025; never optimize with test year.
6. Delimit 2026 SP/SP Jan–Jul, SP/NRT August and NRT/NRT Sep–Oct, disclose field disparities. Distinct SP and NRT product records never overlap per sensor/day.

Sources: https://firms.modaps.eosdis.nasa.gov/data/country/ ; https://firms.modaps.eosdis.nasa.gov/api/area/ ; https://firms.modaps.eosdis.nasa.gov/api/data_availability/ ; https://www.earthdata.nasa.gov/data/tools/firms
Detailed archive SHA-256 and 2026 API response SHA-256 / date windows are stored in data/sci03_resultados.json without revealing FIRMS_MAP_KEY.

### Historical source hashes
| Year | Product | SHA-256 |
|---|---|---|
| 2023 | modis | 659ce5160d96fb2f82491efe4464eb30a0fc8fbbaa373f2962187b7069ae48b2 |
| 2023 | viirs-jpss1 | aa1344aaeedf4fd1475baddb2f505f9a902c7f976b38af5ee1144fcdd3ad95c6 |
| 2024 | modis | b617f757e2b1279802412e71cd457f26a3714e21045fce2aaf25fee908a0c305 |
| 2024 | viirs-jpss1 | 219e933850ceef91452f0d7722b6a0595edd52730674815a6c3fd695d03ebb46 |
| 2025 | modis | 1da12d96d12dc23d72026f638b9e09085a5a61d174def0e9899385af45d67b62 |
| 2025 | viirs-jpss1 | 01a4ea954a97ea85ac43450682a87a3de4dbbcb5dff54b997d9da57370f3d8d9 |

## Scientific interpretation, uncertainties and decision

**Observed:** native pixel distributions, ranked months, ranked 1° cells and quantified agreement for each sensor/period.
**Mathematically established:** global positive scale factor cannot improve the ranking or relative shares, so greater clarity is the main benefit of displaying percentages.
**Hypotheses only:** changing orbit coverage, cloud obscuration, fire cause, climate trends, or physical difference in individual fires. These were not tested.
**Restrictions:** 2026 NRT type field absent; different sensor resolutions/sensitivity and observation schedules; no clear-sky denominator; simplified, not officially verified Amazonas border; NRT can be revised; low detection counts affect share variability; spatial 1° aggregation smooths detail.
**Recommended for FireLens:** consider a future view showing separate month and area shares **for both sensors** with clearly different SP/NRT processing and caveats. Do NOT call relative normalization validated sensor correction, fire risk, prediction or proof of true fire events.

**Decision SCI-03 / status:** evidence-ready proposal, pending review and approval by main session. No UI changes and no TEST-02. Reason: relative metrics help explain observed concentration, not outperform absolute count scaling on a commensurable metric. Alternative: new complex model declined until evidence and time allow. Validation: reproduce source hashes, independent WAPE, distributions, tests and cross-version limits. Responsible: Stack Manauara engineering · 14/11/2026.

## Reproduction
Run unit tests: python -m unittest discover -s tests -v
Historical: python -m scripts.sci03_sources historical --out /tmp/sci03_historical.json
2026: python -m scripts.sci03_sources recent --out /tmp/sci03_recent.json (requires FIRMS_MAP_KEY from GitHub Actions secret)
Compare: python -m scripts.sci03_compare --historical /tmp/sci03_historical.json --recent /tmp/sci03_recent.json --out data/sci03_resultados.json
Report: python -m scripts.sci03_report --results data/sci03_resultados.json --historical /tmp/sci03_historical.json --recent /tmp/sci03_recent.json
