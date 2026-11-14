# TEST-01B — Diagnóstico 2025 e levantamento 2026

Engenharia Stack Manauara · 2026-11-14T22:44:52.475398+00:00 · Aprovação científica pendente da sessão principal.
Interface, dados já publicados e arquivos TEST-01 permanecem sem alteração; TEST-02 não iniciado.

## A. Por que o WAPE aumentou em 2025?
WAPE é erro absoluto agregado por célula-mês de 1 grau, dividido pelo total MODIS Aqua. Não representa erro contra incêndios confirmados.
Os números abaixo reproduzem os holdouts TEST-01 sem usar o ano avaliado no treino.

| Treino | Avaliação | Fator | MODIS | NOAA-20 | Previsto | Erro absoluto | WAPE bruto | WAPE ajustado | Viés predito-MODIS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 2024 | 0.24412630 | 23009 | 90746 | 22153.5 | 5317.3 | 295.53% | 23.11% | -855.5 |
| 2023,2024 | 2025 | 0.24929601 | 4306 | 21382 | 5330.4 | 2184.5 | 398.79% | 50.73% | +1024.4 |

### Efeito do denominador e estabilidade
- Denominador MODIS 2024 = 23009; 2025 = 4306; queda 81.29%.
- Erro absoluto 2024 = 5317.264; 2025 = 2184.467; variação -58.92%.
- A redução do denominador torna o WAPE relativo maior mesmo quando o erro absoluto diminui; não atribuir causalidade física sem dados de observação.
- Viés positivo indica superestimação frente ao MODIS; viés negativo, subestimação.

| Ano | MODIS/NOAA-20 observado (não calibrado para previsão) |
|---|---:|
| 2023 | 0.2441263 |
| 2024 | 0.2535539 |
| 2025 | 0.2013843 |

### Diagnóstico de erros por mês — 2024
| Mês UTC | MODIS | NOAA-20 | Previsto | Erro absoluto | Contribuição WAPE (p.p.) | Parcela erro (%) | Viés |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 134 | 598 | 145.99 | 91.44 | 0.397 | 1.72 | +11.99 |
| 2 | 120 | 416 | 101.56 | 82.57 | 0.359 | 1.55 | -18.44 |
| 3 | 35 | 171 | 41.75 | 56.15 | 0.244 | 1.06 | +6.75 |
| 4 | 25 | 100 | 24.41 | 29.35 | 0.128 | 0.55 | -0.59 |
| 5 | 30 | 184 | 44.92 | 33.15 | 0.144 | 0.62 | +14.92 |
| 6 | 229 | 1109 | 270.74 | 103.69 | 0.451 | 1.95 | +41.74 |
| 7 | 3927 | 15117 | 3690.46 | 637.43 | 2.770 | 11.99 | -236.54 |
| 8 | 9120 | 35942 | 8774.39 | 1821.20 | 7.915 | 34.25 | -345.61 |
| 9 | 6406 | 24300 | 5932.27 | 1364.98 | 5.932 | 25.67 | -473.73 |
| 10 | 2274 | 9839 | 2401.96 | 719.41 | 3.127 | 13.53 | +127.96 |
| 11 | 550 | 2442 | 596.16 | 262.81 | 1.142 | 4.94 | +46.16 |
| 12 | 159 | 528 | 128.90 | 115.09 | 0.500 | 2.17 | -30.10 |

### Células com maior erro — 2024
| Latitude 1° | Longitude 1° | Erro absoluto |
|---:|---:|---:|
| -7 | -59 | 376.97 |
| -7 | -60 | 295.82 |
| -10 | -68 | 257.55 |
| -8 | -62 | 203.3 |
| -8 | -64 | 183.27 |
| -9 | -68 | 181.76 |
| -8 | -61 | 151.2 |
| -3 | -58 | 135.32 |
| -4 | -61 | 135.07 |
| -9 | -65 | 131.28 |
| -9 | -67 | 129.76 |
| -4 | -60 | 125.87 |
Três meses concentram 73.451% do erro; dez células concentram 38.583%.

### Diagnóstico de erros por mês — 2025
| Mês UTC | MODIS | NOAA-20 | Previsto | Erro absoluto | Contribuição WAPE (p.p.) | Parcela erro (%) | Viés |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 50 | 287 | 71.55 | 53.17 | 1.235 | 2.43 | +21.55 |
| 2 | 8 | 45 | 11.22 | 15.23 | 0.354 | 0.70 | +3.22 |
| 3 | 15 | 155 | 38.64 | 40.15 | 0.932 | 1.84 | +23.64 |
| 4 | 10 | 84 | 20.94 | 21.95 | 0.510 | 1.00 | +10.94 |
| 5 | 22 | 139 | 34.65 | 22.67 | 0.527 | 1.04 | +12.65 |
| 6 | 87 | 341 | 85.01 | 34.89 | 0.810 | 1.60 | -1.99 |
| 7 | 268 | 1219 | 303.89 | 156.94 | 3.645 | 7.18 | +35.89 |
| 8 | 1765 | 7534 | 1878.20 | 450.40 | 10.460 | 20.62 | +113.20 |
| 9 | 891 | 4401 | 1097.15 | 434.37 | 10.088 | 19.88 | +206.15 |
| 10 | 825 | 4812 | 1199.61 | 622.14 | 14.448 | 28.48 | +374.61 |
| 11 | 255 | 1508 | 375.94 | 201.66 | 4.683 | 9.23 | +120.94 |
| 12 | 110 | 857 | 213.65 | 130.89 | 3.040 | 5.99 | +103.65 |

### Células com maior erro — 2025
| Latitude 1° | Longitude 1° | Erro absoluto |
|---:|---:|---:|
| -4 | -65 | 132.24 |
| -10 | -66 | 101.03 |
| -8 | -64 | 98.71 |
| -4 | -58 | 79.82 |
| -4 | -60 | 79.81 |
| -8 | -61 | 73.4 |
| -10 | -68 | 65.51 |
| -7 | -60 | 61.74 |
| -8 | -71 | 60.49 |
| -4 | -66 | 55.35 |
| -4 | -59 | 54.68 |
| -3 | -58 | 50.21 |
Três meses concentram 68.983% do erro; dez células concentram 36.993%.

## Auditoria da fonte histórica
Arquivos públicos oficiais NASA FIRMS Brasil 2023–2025 recuperados novamente, cada hash SHA-256 conferido com TEST-01. Filtros diurnos MODIS Aqua >=30 e NOAA20 n/h, type=0 se disponível, mesma geometria simplificada do Amazonas.
| Ano | Sensor | Pixels válidos | SHA-256 | Intervalo dos registros retidos UTC |
|---|---|---:|---|---|
| 2023 | modis | 18246 | 659ce5160d96fb2f82491efe4464eb30a0fc8fbbaa373f2962187b7069ae48b2 | 2023-01-01T18:10:00+00:00 até 2023-12-30T18:19:00+00:00 |
| 2023 | viirs-jpss1 | 74740 | aa1344aaeedf4fd1475baddb2f505f9a902c7f976b38af5ee1144fcdd3ad95c6 | 2023-01-01T16:58:00+00:00 até 2023-12-31T18:12:00+00:00 |
| 2024 | modis | 23009 | b617f757e2b1279802412e71cd457f26a3714e21045fce2aaf25fee908a0c305 | 2024-01-01T18:05:00+00:00 até 2024-12-30T18:50:00+00:00 |
| 2024 | viirs-jpss1 | 90746 | 219e933850ceef91452f0d7722b6a0595edd52730674815a6c3fd695d03ebb46 | 2024-01-01T17:55:00+00:00 até 2024-12-31T18:23:00+00:00 |
| 2025 | modis | 4306 | 1da12d96d12dc23d72026f638b9e09085a5a61d174def0e9899385af45d67b62 | 2025-01-01T18:32:00+00:00 até 2025-12-30T19:34:00+00:00 |
| 2025 | viirs-jpss1 | 21382 | 01a4ea954a97ea85ac43450682a87a3de4dbbcb5dff54b997d9da57370f3d8d9 | 2025-01-01T18:05:00+00:00 até 2025-12-30T18:01:00+00:00 |

## B. Recuperação de dados 2026
Fontes oficiais: https://firms.modaps.eosdis.nasa.gov/download/ ; https://firms.modaps.eosdis.nasa.gov/api/data_availability/ ; https://firms.modaps.eosdis.nasa.gov/api/area/ ; https://nrt3.modaps.eosdis.nasa.gov/help/ .
Archive Download por intervalo requer autenticação Earthdata ou e-mail/código e envia instruções posteriores. Nenhum pedido interativo foi falsamente registrado. Arquivo NRT nrt3 exige token Earthdata diferente da MAP_KEY.
Area API foi consultada com segredo FIRMS_MAP_KEY protegido. Consultas limitadas a 5 dias, preferência por SP, NRT somente para dias sem SP, sem mistura na mesma data.
**Estado:** all_requested_days_queried

| Produto | Disponível de | Até |
|---|---|---|
| MODIS_SP | 2000-11-01 | 2026-08-31 |
| MODIS_NRT | 2026-09-01 | 2026-11-14 |
| VIIRS_NOAA20_SP | 2018-04-01 | 2026-07-31 |
| VIIRS_NOAA20_NRT | 2026-08-01 | 2026-11-14 |

| Sensor | Dias consultados sem erro | Dias sem fonte na API | Janelas falhas | Pixels válidos obtidos | Processamento |
|---|---:|---:|---:|---:|---|
| MODIS_AQUA | 318 | 0 | 0 | 8356 | {"standard": 2417, "nrt": 5939} |
| NOAA20 | 318 | 0 | 0 | 44243 | {"standard": 2098, "nrt": 42145} |

Manifests de cada requisição (URL sem chave, datas, versão SP/NRT, hash do corpo, esquema CSV, contagens e erros) estão preservados no JSON. Consultar o último dia não garante que todas as órbitas já passaram.

### Comparação por período equivalente
Séries históricas foram recortadas em 1º de janeiro–14 de novembro, mesmos dias do calendário, com os mesmos filtros e contorno.
| Ano | MODIS Aqua bruto | NOAA-20 bruto | Origem |
|---|---:|---:|---|
| 2023 | 17809 | 72042 | CSV anual NASA |
| 2024 | 22644 | 89207 | CSV anual NASA |
| 2025 | 4128 | 20049 | CSV anual NASA |
| 2026 | 8356 | 44243 | SP/NRT conforme intervalo, dados provisórios onde NRT |

**Conclusão sobre comparação 2026:** PARCIALMENTE, como contagens descritivas por mesmos dias. Diferenças SP/NRT e passagens não aferidas impedem afirmações de anomalias ou de tendência.

## Fatos, hipóteses e limites
**Fato matemático:** os erros brutos, ajustados e assinados são reproduzidos sobre as mesmas células e anos de avaliação.
**Hipóteses não demonstradas:** causas climáticas, mudança da ocorrência real de incêndios, nuvens, horários de passagem e características instrumentais específicas de 2025.
**Incertezas:** contorno estadual simplificado não auditado contra IBGE oficial; ausência de cobertura clear-sky, diferença entre SP e NRT, latência de disponibilidade e possível mudança de arquivos NRT.
Para o público, só exibir detecções originais com satélite, data, cobertura/versão e ressalvas. Harmonização é exploratória; não afirmar número real de incêndios, risco, previsão ou causa.

## Decisão TEST-01B e TEST-02
**Status:** relatório técnico produzido; aprovação científica da sessão principal pendente.
**Motivo:** investigar instabilidade em 2025 e recuperar 2026 sem extrapolar dados; aceita-se incerteza em vez de melhorar artificialmente WAPE.
**Evidência:** arquivos NASA com hash, análises temporais por célula/mês, inventário 2026 e execução de testes unitários.
**Riscos:** fontes NRT provisórias, fronteira simplificada, recortes NRT/SP, lacunas de órbita e tempo limitado.
**Próxima validação:** obter geometria IBGE, examinar cobertura de passagens, revisar SP/NRT e repetir métricas independentes.
**Responsável/data:** engenharia Stack Manauara, 14/11/2026.
**TEST-02:** NÃO iniciado; autorização permanece com a sessão principal.

## Reproduzir
- python -m unittest discover -s tests -v
- python -m scripts.test01b_diagnose --output /tmp/test01b-a.json
- FIRMS_MAP_KEY como segredo de ambiente: python -m scripts.test01b_2026 --output /tmp/test01b-b.json
- python -m scripts.test01b_report --a /tmp/test01b-a.json --b /tmp/test01b-b.json
Nunca registrar chaves ou URLs autenticadas em logs/JSON.
