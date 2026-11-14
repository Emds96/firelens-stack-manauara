# TEST-01 — Padrões históricos da atividade do fogo no Amazonas

**Data da execução:** 2026-11-14T22:09:52.151665+00:00
**Status recomendado à sessão principal:** PARCIALMENTE APROVADO para histórico exploratório 2023–2025; NÃO aprovado para comparação 2026
**Status de processamento:** historical_evaluated_2026_unverified

## Pergunta
O que o histórico de detecções térmicas desta região nos ensina?
Registros mensais e células de 1 grau permitem observar recorrência e meses mais ativos somente quando os arquivos são temporalmente comparáveis. Não comprovam incêndios distintos ou área queimada.

## Fonte e arquivos realmente examinados
NASA FIRMS Country Annual CSV: https://firms.modaps.eosdis.nasa.gov/data/country/
Download anual direto, com hash SHA-256, contagem e período máximo/mínimo dos pixels retidos. HTTP 404 é registrado de modo diferente de falhas de rede.

| Ano | Sensor | Resultado | Pixels retidos | Primeiro UTC | Último UTC | SHA-256 prefixo |
|---|---|---|---:|---|---|---|
| 2023 | modis | processed | 18246 | 2023-01-01T18:10:00+00:00 | 2023-12-30T18:19:00+00:00 | 659ce5160d96fb2f82 |
| 2023 | viirs-jpss1 | processed | 74740 | 2023-01-01T16:58:00+00:00 | 2023-12-31T18:12:00+00:00 | aa1344aaeedf4fd147 |
| 2024 | modis | processed | 23009 | 2024-01-01T18:05:00+00:00 | 2024-12-30T18:50:00+00:00 | b617f757e2b1279802 |
| 2024 | viirs-jpss1 | processed | 90746 | 2024-01-01T17:55:00+00:00 | 2024-12-31T18:23:00+00:00 | 219e933850ceef9145 |
| 2025 | modis | processed | 4306 | 2025-01-01T18:32:00+00:00 | 2025-12-30T19:34:00+00:00 | 1da12d96d12dc23d72 |
| 2025 | viirs-jpss1 | processed | 21382 | 2025-01-01T18:05:00+00:00 | 2025-12-30T18:01:00+00:00 | 01a4ea954a97ea85ac |
| 2026 | modis | not_found | — | — | — | — |
| 2026 | viirs-jpss1 | not_found | — | — | — | — |

## Região e método
**Geometria utilizada:** simplified third-party IBGE-based outline; NOT official verified precision
**Fonte do contorno:** data/amazonas_ibge.geojson
**Hash do contorno:** e357e40a24547f0d58198cfa4ef4313b53d3cc448c1d4225078e91968583a767
**Tentativa IBGE oficial:** {"url": "https://servicodados.ibge.gov.br/api/v3/malhas/estados/13?formato=application/vnd.geo%2Bjson", "status": "failed", "error_type": "URLError"}

MODIS Aqua, confidence >=30; VIIRS NOAA-20, confidence n/h; type=0 quando disponível; apenas D (diurno); pontos dentro do polígono; células espaciais de 1 grau; mês UTC.
Diferença justificada do VAL-TRAD-02: uso de mês UTC em vez de solar local para evitar ano solar truncado sem arquivos adjacentes. Os WAPEs deste estudo não devem ser comparados diretamente aos dos recortes retangulares A/B.
Fator global = soma MODIS em anos de treino / soma NOAA-20 nos mesmos anos. Validações temporais: 2023→2024 e 2023+2024→2025, **sem utilizar o ano de avaliação para calibrar**.
WAPE = soma dos erros absolutos por célula mensal / soma de pixels MODIS Aqua. Não é erro contra incêndios físicos.

## Meses com mais e menos detecções (NOAA-20, diurno)
- 2023: máximo mensal NOAA-20 9 (25364 pixels); mínimo 2 (46 pixels).
- 2024: máximo mensal NOAA-20 8 (35942 pixels); mínimo 4 (100 pixels).
- 2025: máximo mensal NOAA-20 8 (7534 pixels); mínimo 2 (45 pixels).

## Escala das contagens: teste independente
| Treino | Teste | Fator global | WAPE bruto | WAPE ajustado | Células-mês ativas / status |
|---|---|---:|---:|---:|---|
| 2023 | 2024 | 0.24412630 | 295.53% | 23.11% | 1003 |
| 2023,2024 | 2025 | 0.24929601 | 398.79% | 50.73% | 814 |

## Células recorrentes de 1 grau (NOAA-20)
Recorrência significa pixels detectados em >=2 anos, não o mesmo incêndio.
| Latitude sul da célula | Longitude oeste da célula | Anos | Pixels NOAA-20 |
|---|---|---|---:|
| -7 | -60 | 2023,2024,2025 | 15896 |
| -10 | -66 | 2023,2024,2025 | 11148 |
| -8 | -62 | 2023,2024,2025 | 8784 |
| -4 | -60 | 2023,2024,2025 | 8580 |
| -8 | -64 | 2023,2024,2025 | 7296 |
| -7 | -59 | 2023,2024,2025 | 7006 |
| -8 | -61 | 2023,2024,2025 | 6973 |
| -10 | -68 | 2023,2024,2025 | 6881 |
| -8 | -60 | 2023,2024,2025 | 6524 |
| -9 | -67 | 2023,2024,2025 | 6164 |

## Comparação com 2026
**Resultado:** not_comparable
**Justificativa:** 2026 annual snapshot missing for MODIS Aqua or NOAA-20
A consulta atual NRT de dois dias não preenche a lacuna janeiro–novembro. Mesmo que exista arquivo anual parcial 2026, é necessário recortar novembro dos outros anos até o mesmo dia antes de comparar; o presente pipeline não atribui anomalias 2026 sem esse teste.
2026 não é automaticamente padrão de ciência consolidado: https://firms.modaps.eosdis.nasa.gov/download/

## Observações
- 2023–2025 independent historical holdouts computed for Amazonas with source-year audit.
- Maximum observed NOAA-20 monthly pixel count in complete-source years: 2024-08 (35942).
- Minimum observed NOAA-20 monthly pixel count in complete-source years: 2025-02 (45).
## Interpretações e hipóteses (não observações comprovadas)
- Interpretação: Repeated observations within 1-degree cells warrant closer investigation; they cannot establish repeated individual fires or underlying causes.

## Limitações
- pixel detections != individual fires or burned area
- different sensor resolutions, sensitivities, orbit timing and cloud effects
- hotspot CSV has no clear-sky denominator or uncertainty intervals
- three years do not constitute long-term climatology
- historical A/B calibration is NOT applied to Amazonas
- 2026 files, when present, are not automatically science-quality consolidated
- Dados ausentes não significam zero deteccões nem ausência de fogo.
- Sem ajuste NOAA-20→NOAA-21; sem validação de qualidade do ar ou causa de fogo.

## Rastreabilidade e decisão
**ID:** TEST-01. **Status:** revisão científica pendente da sessão principal.
**Responsável/data:** engenharia Stack Manauara, 14/11/2026.
**Motivo:** testar calendário do Amazonas sem transferir coeficientes experimentais A/B.
**Alternativas:** reutilizar A/B (rejeitado), anual por país (adotado), NRT isolado (não serve para histórico completo).
**Riscos:** sensibilidade e passagem dos sensores, nuvens, polígono simplificado, arquivos 2026 incompletos, somente 3 anos históricos.
**Validação:** dados com proveniência e hashes, WAPE em anos separados, testes automatizados e período equivalente.
**TEST-02:** não iniciar. Detecção sem registro no período analisado não é incêndio novo nem prova ausência anterior.

## Reprodução
python -m unittest discover -s tests -v
python -m scripts.test01_historico --output data/test01_historico_amazonas.json
python -m scripts.test01_report --input data/test01_historico_amazonas.json --output docs/TEST-01_HISTORICO.md
Arquivos do site e data/historico.json permanecem inalterados.
