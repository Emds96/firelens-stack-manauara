# TEST-02 — Visão da Águia: análise físico-espacial, 10–14/11/2026

**Engenharia Stack Manauara | Experimento exploratório | Aprovação científica pendente**
**Executado UTC:** 2026-11-15T01:21:34.635346+00:00

## Veredito

**A concordância de posição, horário, temperatura e FRP indica possíveis associações, mas NÃO confirma a identidade de um único incêndio e NÃO autoriza fundir pixels automaticamente.**
scan × track é apenas dimensão aproximada; caixas alinhadas à latitude/longitude não são os verdadeiros footprints orientados obtidos de geolocalização Level-2. Limites de 5–8 K e razão FRP entre 0,5 e 2,0 são exploratórios, não critérios NASA validados.

## NASA FIRMS, registros originais e contorno

Fonte: https://firms.modaps.eosdis.nasa.gov/api/area/ ; MODIS_NRT (Aqua e Terra) e VIIRS_NOAA20_NRT. Início 2026-11-10, duração 5 dias; todo o Amazonas segundo polígono simplificado. BBox de atenção Manaus/Autazes/Careiro: W -61,5, S -4,5, E -58,5, N -2,0.

| Produto NASA | Linhas brutas CSV | Linhas retidas no Amazonas | Registros de 11/11 | SHA-256 CSV |
|---|---:|---:|---:|---|
| MODIS_NRT | 321 | 147 | 17 | caa13ba58a9f00fd3b1bc6ff3cc7f729f4e98a05d7015543540af352744f3301 |
Colunas preservadas de MODIS_NRT: latitude, longitude, brightness, scan, track, acq_date, acq_time, satellite, instrument, confidence, version, bright_t31, frp, daynight.
| VIIRS_NOAA20_NRT | 1420 | 760 | 267 | ed567a392b3ab65d548ec05065da367c574d1ffc8a511bbd7afcd05cd7a96ad1 |
Colunas preservadas de VIIRS_NOAA20_NRT: latitude, longitude, bright_ti4, scan, track, acq_date, acq_time, satellite, instrument, confidence, version, bright_ti5, frp, daynight.

Todas as colunas físicas originais de cada linha dentro do polígono estão em data/test02_observacoes_20261110_14.json como raw_columns; juntamente com UTC, AMT, flag de saturação, área aproximada e identificadores locais. Nenhuma credencial foi salva.

## Dia 11/11/2026: contagem de pixels, NÃO incêndios

| Instrumento | Todas as observações e turnos | Elegíveis diurnas com filtros TEST-01B |
|---|---:|---:|
| MODIS Aqua | 12 | 12 |
| MODIS Terra | 5 | fora do filtro Aqua histórico |
| VIIRS NOAA-20 | 267 | 222 |

Comparação com TEST-01B: NOAA-20 222 e Aqua 12. Reprodução das contagens diurnas: **sim**.
Não há dados aqui que comprovem o pico de fumaça em Manaus nem a origem da poluição.

### MODIS Aqua e Terra em 11/11: dados por observação

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| M-000096 | Aqua | 20:25 | 16:25 | -9.14287 | -68.21483 | 1.00×1.00 | 1.0000 | 317.01 | 294.11 | 8.71 | 73 | — |
| M-000103 | Aqua | 20:25 | 16:25 | -8.93286 | -68.55575 | 1.01×1.01 | 1.0201 | 328.36 | 291.26 | 21.91 | 83 | — |
| M-000104 | Aqua | 20:25 | 16:25 | -8.93157 | -68.54681 | 1.01×1.01 | 1.0201 | 309.43 | 288.67 | 3.97 | 49 | — |
| M-000108 | Aqua | 20:25 | 16:25 | -7.89819 | -63.70957 | 1.57×1.23 | 1.9311 | 323.94 | 294.36 | 30.09 | 79 | — |
| M-000109 | Aqua | 20:25 | 16:25 | -7.89330 | -63.71756 | 1.56×1.23 | 1.9188 | 330.14 | 295.10 | 44.06 | 84 | — |
| M-000110 | Aqua | 20:25 | 16:25 | -7.88742 | -63.71134 | 1.57×1.23 | 1.9311 | 328.73 | 294.19 | 39.34 | 83 | — |
| M-000111 | Aqua | 20:25 | 16:25 | -7.56405 | -64.53294 | 1.39×1.17 | 1.6263 | 310.51 | 292.78 | 6.43 | 46 | — |
| M-000112 | Aqua | 20:25 | 16:25 | -7.56093 | -64.52789 | 1.39×1.17 | 1.6263 | 312.23 | 292.79 | 8.80 | 62 | — |
| M-000113 | Aqua | 20:27 | 16:27 | -6.35624 | -68.25810 | 1.00×1.00 | 1.0000 | 311.22 | 296.82 | 5.29 | 61 | — |
| M-000114 | Aqua | 20:27 | 16:27 | -5.50076 | -60.25204 | 3.26×1.71 | 5.5746 | 313.62 | 290.57 | 37.59 | 56 | — |
| M-000115 | Aqua | 20:27 | 16:27 | -5.50072 | -60.25971 | 3.26×1.71 | 5.5746 | 317.24 | 290.81 | 54.71 | 61 | — |
| M-000116 | Aqua | 20:27 | 16:27 | -3.16802 | -68.06853 | 1.03×1.02 | 1.0506 | 310.44 | 292.26 | 6.52 | 64 | — |
| M-000080 | Terra | 00:45 | 20:45 | -9.03352 | -65.95448 | 1.57×1.24 | 1.9468 | 304.91 | 292.90 | 8.01 | 55 | — |
| M-000081 | Terra | 00:45 | 20:45 | -8.98126 | -67.47237 | 2.06×1.40 | 2.8840 | 303.84 | 292.83 | 9.83 | 49 | — |
| M-000086 | Terra | 00:47 | 20:47 | -3.43877 | -59.61699 | 1.28×1.12 | 1.4336 | 305.36 | 292.26 | 6.71 | 62 | — |
| M-000087 | Terra | 00:47 | 20:47 | -3.41069 | -60.30965 | 1.17×1.08 | 1.2636 | 303.52 | 291.71 | 4.17 | 51 | — |
| M-000089 | Terra | 13:10 | 09:10 | -7.64675 | -67.12971 | 1.22×1.10 | 1.3420 | 310.27 | 290.50 | 7.85 | 46 | — |

### NOAA-20 em 11/11: primeiras 25 linhas; todas no JSON

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000251 | NOAA-20 | 05:03 | 01:03 | -3.44190 | -59.61332 | 0.45×0.47 | 0.2115 | 311.81 | 290.61 | 1.35 | n | — |
| V-000252 | NOAA-20 | 05:03 | 01:03 | -3.43760 | -59.61261 | 0.45×0.47 | 0.2115 | 303.56 | 290.23 | 0.67 | n | — |
| V-000256 | NOAA-20 | 05:03 | 01:03 | -2.41666 | -57.90071 | 0.55×0.43 | 0.2365 | 304.41 | 290.69 | 0.87 | n | — |
| V-000259 | NOAA-20 | 05:03 | 01:03 | -1.44419 | -57.92565 | 0.57×0.43 | 0.2451 | 302.90 | 282.45 | 1.14 | n | — |
| V-000260 | NOAA-20 | 05:03 | 01:03 | -1.44104 | -57.91998 | 0.57×0.43 | 0.2451 | 303.20 | 279.96 | 1.14 | n | — |
| V-000261 | NOAA-20 | 05:03 | 01:03 | -1.44022 | -57.92505 | 0.57×0.43 | 0.2451 | 302.08 | 282.52 | 1.14 | n | — |
| V-000277 | NOAA-20 | 05:05 | 01:05 | -7.99356 | -61.34024 | 0.50×0.49 | 0.2450 | 312.07 | 289.56 | 1.73 | n | — |
| V-000278 | NOAA-20 | 05:05 | 01:05 | -7.96297 | -61.31849 | 0.50×0.49 | 0.2450 | 309.30 | 290.12 | 1.01 | n | — |
| V-000279 | NOAA-20 | 05:05 | 01:05 | -7.92629 | -61.55844 | 0.52×0.50 | 0.2600 | 302.49 | 285.27 | 1.10 | n | — |
| V-000280 | NOAA-20 | 05:05 | 01:05 | -7.80829 | -61.11646 | 0.49×0.48 | 0.2352 | 308.58 | 290.38 | 0.95 | n | — |
| V-000281 | NOAA-20 | 05:05 | 01:05 | -7.80762 | -61.11317 | 0.49×0.48 | 0.2352 | 303.59 | 290.13 | 1.19 | n | — |
| V-000282 | NOAA-20 | 05:05 | 01:05 | -7.80684 | -61.11757 | 0.49×0.48 | 0.2352 | 308.51 | 289.98 | 1.19 | n | — |
| V-000283 | NOAA-20 | 05:05 | 01:05 | -7.80386 | -61.11567 | 0.49×0.48 | 0.2352 | 305.41 | 290.21 | 0.95 | n | — |
| V-000284 | NOAA-20 | 05:05 | 01:05 | -7.70538 | -61.36658 | 0.51×0.49 | 0.2499 | 303.06 | 289.43 | 0.76 | n | — |
| V-000285 | NOAA-20 | 05:05 | 01:05 | -7.70086 | -61.36578 | 0.51×0.49 | 0.2499 | 306.09 | 289.59 | 1.16 | n | — |
| V-000286 | NOAA-20 | 05:05 | 01:05 | -7.62914 | -61.04974 | 0.48×0.48 | 0.2304 | 311.96 | 288.55 | 1.48 | n | — |
| V-000287 | NOAA-20 | 05:05 | 01:05 | -7.62838 | -61.05413 | 0.49×0.48 | 0.2352 | 306.65 | 288.02 | 1.48 | n | — |
| V-000288 | NOAA-20 | 05:05 | 01:05 | -7.33342 | -60.20343 | 0.43×0.46 | 0.1978 | 305.53 | 289.32 | 1.12 | n | — |
| V-000311 | NOAA-20 | 17:41 | 13:41 | -9.46818 | -67.13737 | 0.46×0.47 | 0.2162 | 335.23 | 292.13 | 3.27 | n | — |
| V-000316 | NOAA-20 | 17:41 | 13:41 | -9.38620 | -66.48963 | 0.42×0.45 | 0.1890 | 340.71 | 296.75 | 4.49 | n | — |
| V-000317 | NOAA-20 | 17:41 | 13:41 | -9.38258 | -66.49400 | 0.42×0.45 | 0.1890 | 334.33 | 298.03 | 15.51 | n | — |
| V-000318 | NOAA-20 | 17:41 | 13:41 | -9.38205 | -66.49023 | 0.42×0.45 | 0.1890 | 349.34 | 302.42 | 51.07 | n | — |
| V-000322 | NOAA-20 | 17:41 | 13:41 | -9.37684 | -66.48322 | 0.42×0.45 | 0.1890 | 333.80 | 300.77 | 5.87 | n | — |
| V-000326 | NOAA-20 | 17:41 | 13:41 | -9.25949 | -67.47787 | 0.48×0.48 | 0.2304 | 332.62 | 283.19 | 3.09 | n | — |
| V-000327 | NOAA-20 | 17:41 | 13:41 | -9.23315 | -67.51702 | 0.48×0.48 | 0.2304 | 333.08 | 283.05 | 5.91 | n | — |

Detalhe completo de outras 242 observações no JSON original separado.

## Quatro travas testadas

1. ΔX=|Δlongitude| × 111,32 × cos(latitude média) e ΔY=|Δlatitude| × 110,57, em km; encaixe aproximado se ΔX≤(scan_M+scan_V)/2 e ΔY≤(track_M+track_V)/2.
2. Mesma data e turno D/N; Δt≤120 min classifica vizinhança temporal, >120 min classifica sobreposição defasada. Não existe uma janela orbital universal para todas as passagens.
3. ΔT11=|bright_t31_MODIS−média(bright_ti5_VIIRS)| apenas dos pixels da caixa e janela; 5 K e 8 K usados como análise de sensibilidade.
4. Razão FRP=ΣFRP_VIIRS associados / FRP_MODIS. Usamos intervalo exploratório 0,5–2,0; FRP é potência radiativa instantânea, não energia conservada. Sobreposições entre caixas podem reutilizar o mesmo VIIRS e são sinalizadas.

### Grupos reais MODIS ↔ VIIRS (exemplos por hora e localização)

#### M-000086 / Terra / UTC 2026-11-11T00:47:00Z (AMT 2026-11-10T20:47-04:00)
MODIS: coordenadas (-3.43877, -59.61699), dimensões 1.28×1.12 km (área ~1.434 km²); T4 305.36 K, T11 292.26 K, FRP 6.71 MW.
VIIRS dentro da caixa e ≤120 min: 0; >120 min: 2; TI5 média — K; ΔT11 — K; ΣFRP — MW; razão VIIRS/MODIS —; 4 critérios a 8 K: **não passou**.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000251 | NOAA-20 | 05:03 | 01:03 | -3.44190 | -59.61332 | 0.45×0.47 | 0.2115 | 311.81 | 290.61 | 1.35 | n | — |
| V-000252 | NOAA-20 | 05:03 | 01:03 | -3.43760 | -59.61261 | 0.45×0.47 | 0.2115 | 303.56 | 290.23 | 0.67 | n | — |

#### M-000096 / Aqua / UTC 2026-11-11T20:25:00Z (AMT 2026-11-11T16:25-04:00)
MODIS: coordenadas (-9.14287, -68.21483), dimensões 1.00×1.00 km (área ~1.000 km²); T4 317.01 K, T11 294.11 K, FRP 8.71 MW.
VIIRS dentro da caixa e ≤120 min: 0; >120 min: 1; TI5 média — K; ΔT11 — K; ΣFRP — MW; razão VIIRS/MODIS —; 4 critérios a 8 K: **não passou**.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000338 | NOAA-20 | 17:41 | 13:41 | -9.13899 | -68.21307 | 0.54×0.51 | 0.2754 | 329.99 | 278.14 | 9.23 | n | — |

#### M-000103 / Aqua / UTC 2026-11-11T20:25:00Z (AMT 2026-11-11T16:25-04:00)
MODIS: coordenadas (-8.93286, -68.55575), dimensões 1.01×1.01 km (área ~1.020 km²); T4 328.36 K, T11 291.26 K, FRP 21.91 MW.
VIIRS dentro da caixa e ≤120 min: 0; >120 min: 8; TI5 média — K; ΔT11 — K; ΣFRP — MW; razão VIIRS/MODIS —; 4 critérios a 8 K: **não passou**.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000360 | NOAA-20 | 17:41 | 13:41 | -8.93632 | -68.55603 | 0.56×0.52 | 0.2912 | 341.43 | 280.51 | 22.62 | n | — |
| V-000361 | NOAA-20 | 17:41 | 13:41 | -8.93582 | -68.55853 | 0.56×0.52 | 0.2912 | 330.90 | 280.88 | 7.91 | n | — |
| V-000362 | NOAA-20 | 17:41 | 13:41 | -8.93564 | -68.55086 | 0.56×0.52 | 0.2912 | 327.77 | 278.92 | 22.62 | n | — |
| V-000363 | NOAA-20 | 17:41 | 13:41 | -8.93511 | -68.55339 | 0.56×0.52 | 0.2912 | 349.20 | 280.88 | 22.18 | n | — |
| V-000368 | NOAA-20 | 17:41 | 13:41 | -8.93089 | -68.55150 | 0.56×0.52 | 0.2912 | 350.78 | 285.48 | 22.62 | n | — |
| V-000370 | NOAA-20 | 17:41 | 13:41 | -8.93036 | -68.55401 | 0.56×0.52 | 0.2912 | 343.77 | 283.59 | 22.18 | n | — |
| V-000371 | NOAA-20 | 17:41 | 13:41 | -8.92965 | -68.54889 | 0.56×0.52 | 0.2912 | 340.94 | 280.52 | 22.18 | n | — |
| V-000372 | NOAA-20 | 17:41 | 13:41 | -8.92615 | -68.55219 | 0.56×0.52 | 0.2912 | 330.69 | 279.48 | 4.81 | n | — |

#### M-000104 / Aqua / UTC 2026-11-11T20:25:00Z (AMT 2026-11-11T16:25-04:00)
MODIS: coordenadas (-8.93157, -68.54681), dimensões 1.01×1.01 km (área ~1.020 km²); T4 309.43 K, T11 288.67 K, FRP 3.97 MW.
VIIRS dentro da caixa e ≤120 min: 0; >120 min: 9; TI5 média — K; ΔT11 — K; ΣFRP — MW; razão VIIRS/MODIS —; 4 critérios a 8 K: **não passou**.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000362 | NOAA-20 | 17:41 | 13:41 | -8.93564 | -68.55086 | 0.56×0.52 | 0.2912 | 327.77 | 278.92 | 22.62 | n | — |
| V-000363 | NOAA-20 | 17:41 | 13:41 | -8.93511 | -68.55339 | 0.56×0.52 | 0.2912 | 349.20 | 280.88 | 22.18 | n | — |
| V-000364 | NOAA-20 | 17:41 | 13:41 | -8.93497 | -68.54572 | 0.56×0.52 | 0.2912 | 344.82 | 282.38 | 17.41 | n | — |
| V-000365 | NOAA-20 | 17:41 | 13:41 | -8.93440 | -68.54824 | 0.56×0.52 | 0.2912 | 343.26 | 280.00 | 22.18 | n | — |
| V-000366 | NOAA-20 | 17:41 | 13:41 | -8.93430 | -68.54065 | 0.56×0.52 | 0.2912 | 332.50 | 279.27 | 17.41 | n | — |
| V-000367 | NOAA-20 | 17:41 | 13:41 | -8.93369 | -68.54316 | 0.56×0.52 | 0.2912 | 345.16 | 281.37 | 18.79 | n | — |
| V-000368 | NOAA-20 | 17:41 | 13:41 | -8.93089 | -68.55150 | 0.56×0.52 | 0.2912 | 350.78 | 285.48 | 22.62 | n | — |
| V-000371 | NOAA-20 | 17:41 | 13:41 | -8.92965 | -68.54889 | 0.56×0.52 | 0.2912 | 340.94 | 280.52 | 22.18 | n | — |
| V-000372 | NOAA-20 | 17:41 | 13:41 | -8.92615 | -68.55219 | 0.56×0.52 | 0.2912 | 330.69 | 279.48 | 4.81 | n | — |

#### M-000108 / Aqua / UTC 2026-11-11T20:25:00Z (AMT 2026-11-11T16:25-04:00)
MODIS: coordenadas (-7.89819, -63.70957), dimensões 1.57×1.23 km (área ~1.931 km²); T4 323.94 K, T11 294.36 K, FRP 30.09 MW.
VIIRS dentro da caixa e ≤120 min: 0; >120 min: 0; TI5 média — K; ΔT11 — K; ΣFRP — MW; razão VIIRS/MODIS —; 4 critérios a 8 K: **não passou**.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|

#### M-000109 / Aqua / UTC 2026-11-11T20:25:00Z (AMT 2026-11-11T16:25-04:00)
MODIS: coordenadas (-7.89330, -63.71756), dimensões 1.56×1.23 km (área ~1.919 km²); T4 330.14 K, T11 295.10 K, FRP 44.06 MW.
VIIRS dentro da caixa e ≤120 min: 0; >120 min: 1; TI5 média — K; ΔT11 — K; ΣFRP — MW; razão VIIRS/MODIS —; 4 critérios a 8 K: **não passou**.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000421 | NOAA-20 | 17:41 | 13:41 | -7.88759 | -63.71191 | 0.43×0.38 | 0.1634 | 338.72 | 299.16 | 212.90 | l | — |


### Dois grupos de 10/11 com os quatro critérios exploratórios compatíveis

O dia 11 não teve grupos em até 120 minutos. No dia anterior, os seguintes grupos VIIRS–Aqua são candidatos para verificação posterior com geolocalização Level-2, **não incêndios confirmados**.

**M-000047 / Aqua**: UTC 2026-11-10T19:49:00Z, AMT 2026-11-10T15:49-04:00, coord (-3.44421, -59.61359), scan×track 1.00×1.00 km, FRP MODIS 18.62 MW, T31 297.36 K; VIIRS 2 pixels, ΣFRP 13.09 MW, média TI5 293.98 K, ΔT11 3.38 K, razão 0.703, Δt 107 minutos.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000192 | NOAA-20 | 18:02 | 14:02 | -3.44233 | -59.61069 | 0.57×0.52 | 0.2964 | 332.16 | 294.24 | 6.86 | n | — |
| V-000193 | NOAA-20 | 18:02 | 14:02 | -3.44225 | -59.60994 | 0.57×0.52 | 0.2964 | 332.46 | 293.72 | 6.23 | n | — |

**M-000048 / Aqua**: UTC 2026-11-10T19:49:00Z, AMT 2026-11-10T15:49-04:00, coord (-3.41922, -60.31168), scan×track 1.02×1.01 km, FRP MODIS 4.70 MW, T31 297.60 K; VIIRS 1 pixels, ΣFRP 3.91 MW, média TI5 293.55 K, ΔT11 4.05 K, razão 0.832, Δt 107 minutos.

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000194 | NOAA-20 | 18:02 | 14:02 | -3.41687 | -60.30735 | 0.51×0.50 | 0.2550 | 331.33 | 293.55 | 3.91 | n | — |


### Exemplos de detecções VIIRS distantes das caixas MODIS

| ID | Satélite | Hora UTC | AMT | Lat | Lon | scan × track (km) | Área aprox. km² | T4 K | T11 K | FRP MW | Conf. | Saturação/Folding |
|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| V-000256 | NOAA-20 | 05:03 | 01:03 | -2.41666 | -57.90071 | 0.55×0.43 | 0.2365 | 304.41 | 290.69 | 0.87 | n | — |
| V-000259 | NOAA-20 | 05:03 | 01:03 | -1.44419 | -57.92565 | 0.57×0.43 | 0.2451 | 302.90 | 282.45 | 1.14 | n | — |
| V-000260 | NOAA-20 | 05:03 | 01:03 | -1.44104 | -57.91998 | 0.57×0.43 | 0.2451 | 303.20 | 279.96 | 1.14 | n | — |
| V-000261 | NOAA-20 | 05:03 | 01:03 | -1.44022 | -57.92505 | 0.57×0.43 | 0.2451 | 302.08 | 282.52 | 1.14 | n | — |
| V-000277 | NOAA-20 | 05:05 | 01:05 | -7.99356 | -61.34024 | 0.50×0.49 | 0.2450 | 312.07 | 289.56 | 1.73 | n | — |
| V-000278 | NOAA-20 | 05:05 | 01:05 | -7.96297 | -61.31849 | 0.50×0.49 | 0.2450 | 309.30 | 290.12 | 1.01 | n | — |
| V-000279 | NOAA-20 | 05:05 | 01:05 | -7.92629 | -61.55844 | 0.52×0.50 | 0.2600 | 302.49 | 285.27 | 1.10 | n | — |
| V-000280 | NOAA-20 | 05:05 | 01:05 | -7.80829 | -61.11646 | 0.49×0.48 | 0.2352 | 308.58 | 290.38 | 0.95 | n | — |

## Classificação exclusiva das observações NOAA-20, 11/11

As quatro classes sugeridas foram mantidas como hipóteses, acrescidas da classe de falha/ambiguidade para não forçar classificação indevida. A primeira é CANDIDATA e não significa incêndio confirmado.

| Classe de pixel VIIRS | N | FRP médio MW | Área média aprox. km² | T4 média K | T11 média K | I4=367 | I4<250 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1. Quatro critérios compatíveis (candidato, NÃO confirmado) | 0 | — | — | — | — | 0 | 0 |
| 2. Sobreposição e intervalo >120 min | 19 | 24.81 | 0.259 | 336.00 | 285.25 | 0 | 0 |
| 3. Borda: fora da caixa, até 2,5 km | 1 | 2.02 | 0.291 | 327.23 | 279.18 | 0 | 0 |
| 4. VIIRS isolado (>2,5 km de qualquer caixa MODIS) | 243 | 7.35 | 0.176 | 336.20 | 296.49 | 0 | 0 |
| 5. Ambíguo / critério não atendido | 0 | — | — | — | — | 0 | 0 |
| 5b. Indeterminado | 4 | 8.23 | 0.178 | 343.43 | 295.39 | 0 | 0 |

### Somente NOAA-20 elegível diurno — universo dos 222 pixels do TEST-01B

| Classe VIIRS elegível (n/h, D) | N | FRP médio MW | Área média aprox. km² | T4 média K | T11 média K |
|---|---:|---:|---:|---:|---:|
| 1. Quatro critérios compatíveis (candidato, NÃO confirmado) | 0 | — | — | — | — |
| 2. Sobreposição e intervalo >120 min | 15 | 16.66 | 0.277 | 339.73 | 282.85 |
| 3. Borda: fora da caixa, até 2,5 km | 1 | 2.02 | 0.291 | 327.23 | 279.18 |
| 4. VIIRS isolado (>2,5 km de qualquer caixa MODIS) | 202 | 7.89 | 0.172 | 339.09 | 296.37 |
| 5. Ambíguo / critério não atendido | 0 | — | — | — | — |
| 5b. Indeterminado | 4 | 8.23 | 0.178 | 343.43 | 295.39 |

**Controle:** 222 detecções elegíveis; a soma por classe é True.

### Entorno Manaus / Autazes / Careiro — caixa geográfica solicitada

No dia 11, na BBOX local: 2 pixels MODIS de todas as plataformas/turnos e 35 pixels NOAA-20 de todas as confianças/turnos. Esses números não representam a quantidade de fumaça ou área queimada.

| Classe VIIRS na BBOX local | N | FRP médio MW | T4 média K | T11 média K |
|---|---:|---:|---:|---:|
| 1. Quatro critérios compatíveis (candidato, NÃO confirmado) | 0 | — | — | — |
| 2. Sobreposição e intervalo >120 min | 2 | 1.01 | 307.69 | 290.42 |
| 3. Borda: fora da caixa, até 2,5 km | 0 | — | — | — |
| 4. VIIRS isolado (>2,5 km de qualquer caixa MODIS) | 30 | 7.97 | 339.09 | 297.13 |
| 5. Ambíguo / critério não atendido | 0 | — | — | — |
| 5b. Indeterminado | 3 | 8.00 | 345.82 | 298.71 |

**Controle da área local:** soma de classes = True.

### Pares geométricos por linha — 11/11/2026, sem fusão

Cada linha permite reconstituir a relação centro-a-centro (ΔX, ΔY), intervalo UTC entre passagens e motivo da associação. Inclui pares defasados e de borda mesmo quando nenhuma dupla cumpre as quatro travas.

| MODIS ID / plataforma | VIIRS ID | Δt min | ΔX km | ΔY km | Dist. entre centros km | Fora da borda km | Encaixe | Tipo da associação |
|---|---|---:|---:|---:|---:|---:|---|---|
| M-000086 / Terra | V-000251 | 256.0 | 0.408 | 0.346 | 0.535 | 0.000 | sim | spatial_delayed_candidate |
| M-000086 / Terra | V-000252 | 256.0 | 0.487 | 0.129 | 0.504 | 0.000 | sim | spatial_delayed_candidate |
| M-000096 / Aqua | V-000338 | 164.0 | 0.193 | 0.429 | 0.471 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000360 | 164.0 | 0.031 | 0.383 | 0.384 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000361 | 164.0 | 0.306 | 0.327 | 0.448 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000362 | 164.0 | 0.538 | 0.307 | 0.619 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000363 | 164.0 | 0.260 | 0.249 | 0.359 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000364 | 164.0 | 1.103 | 0.233 | 1.127 | 0.318 | não | near_border_unverified |
| M-000103 / Aqua | V-000365 | 164.0 | 0.826 | 0.170 | 0.843 | 0.041 | não | near_border_unverified |
| M-000103 / Aqua | V-000366 | 164.0 | 1.661 | 0.159 | 1.668 | 0.875 | não | near_border_unverified |
| M-000103 / Aqua | V-000367 | 164.0 | 1.385 | 0.092 | 1.388 | 0.600 | não | near_border_unverified |
| M-000103 / Aqua | V-000368 | 164.0 | 0.467 | 0.218 | 0.516 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000370 | 164.0 | 0.191 | 0.276 | 0.336 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000371 | 164.0 | 0.754 | 0.355 | 0.834 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000372 | 164.0 | 0.392 | 0.742 | 0.839 | 0.000 | sim | spatial_delayed_candidate |
| M-000103 / Aqua | V-000373 | 164.0 | 1.145 | 1.695 | 2.045 | 0.997 | não | near_border_unverified |
| M-000104 / Aqua | V-000360 | 164.0 | 1.014 | 0.525 | 1.142 | 0.229 | não | near_border_unverified |
| M-000104 / Aqua | V-000361 | 164.0 | 1.289 | 0.470 | 1.372 | 0.504 | não | near_border_unverified |
| M-000104 / Aqua | V-000362 | 164.0 | 0.445 | 0.450 | 0.633 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000363 | 164.0 | 0.724 | 0.391 | 0.823 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000364 | 164.0 | 0.120 | 0.376 | 0.395 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000365 | 164.0 | 0.157 | 0.313 | 0.350 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000366 | 164.0 | 0.677 | 0.302 | 0.742 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000367 | 164.0 | 0.401 | 0.234 | 0.465 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000368 | 164.0 | 0.516 | 0.075 | 0.521 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000370 | 164.0 | 0.792 | 0.134 | 0.803 | 0.007 | não | near_border_unverified |
| M-000104 / Aqua | V-000371 | 164.0 | 0.229 | 0.212 | 0.312 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000372 | 164.0 | 0.592 | 0.599 | 0.842 | 0.000 | sim | spatial_delayed_candidate |
| M-000104 / Aqua | V-000373 | 164.0 | 2.128 | 1.552 | 2.634 | 1.557 | não | near_border_unverified |
| M-000108 / Aqua | V-000421 | 164.0 | 0.258 | 1.172 | 1.200 | 0.367 | não | near_border_unverified |
| M-000109 / Aqua | V-000421 | 164.0 | 0.623 | 0.631 | 0.887 | 0.000 | sim | spatial_delayed_candidate |
| M-000110 / Aqua | V-000421 | 164.0 | 0.063 | 0.019 | 0.066 | 0.000 | sim | spatial_delayed_candidate |
| M-000111 / Aqua | V-000437 | 164.0 | 0.212 | 0.814 | 0.841 | 0.034 | não | near_border_unverified |
| M-000111 / Aqua | V-000438 | 164.0 | 0.671 | 0.880 | 1.107 | 0.100 | não | near_border_unverified |
| M-000112 / Aqua | V-000437 | 164.0 | 0.345 | 0.469 | 0.582 | 0.000 | sim | spatial_delayed_candidate |
| M-000112 / Aqua | V-000438 | 164.0 | 0.114 | 0.535 | 0.547 | 0.000 | sim | spatial_delayed_candidate |
| M-000116 / Aqua | V-000588 | 164.0 | 0.659 | 0.238 | 0.701 | 0.000 | sim | spatial_delayed_candidate |

**Exclusividade e soma:** 267 / 267 pixels, conferência: True. Grupos MODIS que passaram nas quatro travas (5 K / 8 K): 0 / 0. Pixels VIIRS associados a múltiplas caixas MODIS: 2 na janela total.
A categoria 4 usa distância >2,5 km da borda das caixas aproximadas MODIS na mesma data, não distância entre centros. Ela NÃO demonstra detecção impossível pelo MODIS, fogo menor, incêndio de sub-bosque ou fumaça originada desse local.

## Comparação da janela completa (10–14/11)

| Data UTC | Aqua | Terra | NOAA-20 total | Aqua diurno | NOAA-20 diurno | Grupos 4 travas (8 K) | VIIRS isolados |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-10 | 16 | 9 | 127 | 16 | 49 | 2 | 112 |
| 2026-11-11 | 12 | 5 | 267 | 12 | 222 | 0 | 243 |
| 2026-11-12 | 47 | 0 | 165 | 43 | 133 | 0 | 143 |
| 2026-11-13 | 32 | 21 | 148 | 29 | 128 | 0 | 102 |
| 2026-11-14 | 3 | 2 | 53 | 3 | 37 | 0 | 52 |

## Ciência, limitações e decisão TEST-02

**Fatos verificáveis:** CSVs de origem com hashes, atributos físicos originais, turnos e horários UTC/AMT, áreas nominais, relações espaciais aproximadas, diferenças térmicas, FRP e grupos de observações.
**Limitações científicas:** caixas não correspondem às geometrias orientadas Level-2; T31 e TI5 são temperaturas de brilho de pixels detectados, não temperaturas puras de fundo não queimado; FRP instantâneo não é energia conservada; saturação/folding I4 exige qualidade/radiância para confirmação; há possível sobreposição e dupla contagem. NASA FIRMS não comprova céu limpo, ausência de incêndio, ar poluído nem causalidade da fumaça.
**Decisão TEST-02 / status:** realizado como ensaio descritivo, identidade de um único incêndio NÃO validada; aprovação científica pendente da sessão principal. Alternativas: fusão direta de contagens pelos quatro critérios (não justificada); estudo dos candidatos com órbitas/footprints Level-2 e máscaras de nuvens (recomendado se aprovado).
**Riscos:** confusão entre pixel e incêndio físico, NRT mutável, geometria estadual simplificada, distância temporal e FRP, diferença de sensores. Validação futura: swaths de órbita, geolocalização real e dados independentes.
**Responsável/data:** Engenharia Stack Manauara, 14/11/2026. Nenhuma alteração em TEST-01/01B/SCI-03 nem no frontend.

## Execução reproduzível

python -m unittest discover -s tests -v
FIRMS_MAP_KEY como variável de ambiente protegida: python -m scripts.test02_fisico
python -m scripts.test02_report
O relatório e os dados separados foram produzidos pelo workflow TEST-02, usando o segredo protegido; a chave não faz parte de nenhum artefato.
