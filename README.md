# FireLens — Dois Tradutores | Stack Manauara

NASA Space Apps Challenge 2026 · **Harmonization of MODIS and VIIRS Hot Spots**.

**Status atual:** código e dados no GitHub e **GitHub Pages publicado e testado** em https://emds96.github.io/firelens-stack-manauara/. **NASA NRT NOAA-20/NOAA-21 comprovado em 14/11/2026 nas execuções #2 e #3**. **HIST-02:** calendário estadual do Amazonas de janeiro–outubro 2023–2026 para MODIS Aqua e NOAA-20, baseado no SCI-03, com SP/NRT e meses indisponíveis sinalizados; o calendário A/B 2022–2024 permanece como opção separada. Execução automática agendada por **schedule** observada e concluída com sucesso em 14/11/2026 22:44 AMT (execução [43669211275](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669211275)); isso não garante disponibilidade contínua futura.

## Limites do recorte geográfico

O arquivo versionado `data/amazonas_ibge.geojson` é **uma geometria estadual simplificada de fonte secundária baseada em IBGE**, e não uma verificação direta de malha oficial atualizada. Veja `docs/GEOMETRIA_AMAZONAS.md`. O contorno pode produzir erros junto às fronteiras.

## Languages and public project demo (ENG-04)

- **English is the default** for judging, with a prominent **EN / PT-BR** toggle. Selection is remembered in the browser and shareable via `?lang=en` or `?lang=pt-BR`.
- Interface translations include scientific caveats, live-data status, time/date formatting, WAPE labels, and calendar month detail.
- **English seven-slide presentation:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf
- **Presentation landing page:** https://emds96.github.io/firelens-stack-manauara/demo/
- The demo was prepared with AI assistance and its seven-slide PDF and bilingual UI were browser-tested on 14/11/2026; the team remains responsible for review and final approval.

## MAP-01: Interactive geographic hotspot viewer

- The **Map** is the main entry point: a real NASA FIRMS NOAA-20/NOAA-21 2D Leaflet viewer, clustered points, satellite filters and keyboard-accessible list. Selecting a point displays **one plain-language interpretation first**; observed attributes are available in an expandable technical panel (EN/PT-BR).
- The current observation and retrieval timestamps are distinct; stale or failed snapshots are labelled instead of presented as current. Pixel detections are not individual confirmed fires or burned-area outlines.
- Verified in Chrome CI: [MAP-01 browser test and scientific regressions](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43641760032). Includes mobile viewport 390x844 and unavailable JSON case.
- Libraries: Leaflet 1.9.4, Leaflet.markercluster 1.5.3. Base map: © OpenStreetMap contributors. Browser network access needed. Details: [docs/MAP-01.md](docs/MAP-01.md).
- 3D globe is not part of this MVP and is not approved.

## FIN-01 / UX-03 — Map-first final experience (14 Nov 2026)

The app is organized into **Map / History / Understand the data**, with a compact header, simplified navigation and expandable supporting measurements. The original 2022–2024 experimental calendar (regions A/B) and historical WAPE charts remain accessible.

- **Eagle's View:** On the Map, use “Explore a real case / Explorar um caso real” to switch from recent NOAA-20/NOAA-21 points to a completely separate **archived 10 November 2026** observation example. Its three source-verified pixels are MODIS Aqua M-000047 and VIIRS NOAA-20 V-000192/V-000193. VIIRS was observed at **18:02 UTC**, Aqua at **19:49 UTC** (107 minutes apart); FRP MODIS **18.62 MW** and summed VIIRS **13.09 MW**. These are **candidate associations, not evidence of one confirmed physical fire**.
- **Scientific cautions:** `scan × track` approximates pixel dimensions, not exact orbital footprints; MODIS T31 and VIIRS TI5 are brightness temperatures in different channels; FRP is radiative power, not conserved energy. No evidence establishes an understory fire, burned-area polygon, smoke origin, or that a missing MODIS point implies no fire.
- **Archived case source:** [data/caso_visao_aguia_20261110.json](data/caso_visao_aguia_20261110.json), derived **without changing** [TEST-02 observations](data/test02_observacoes_20261110_14.json) or [TEST-02 analysis](data/test02_resultados.json).
- **Historical limitations:** pilot calendar A/B ≠ the whole Amazonas state or a municipal history; separate Amazonas TEST-01B holdout WAPE worsened from **23.11% (2024)** to **50.73% (2025)**, showing that the factor is not a universal correction.
- **Seven-slide English demo:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf — actual application screenshots, dated observational evidence, distinct processing/data coverage and explicit limitations; generated with ChatGPT assistance and validated for seven pages.
- **Regression evidence:** [47 Python tests and full browser QA](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669321931); [actual browser screenshots and seven-slide PDF build](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669280189).
- **Release documentation:** [docs/FIN-01_UX-03_ENTREGA.md](docs/FIN-01_UX-03_ENTREGA.md). NASA project submission remains **NOT submitted** without explicit human authorization.

## HIST-02 — Statewide historical calendar (14 Nov 2026)

The default **History** view now reads **4,434 original 1° × UTC-month SCI-03 cell records** from [data/sci03_agregados.json](data/sci03_agregados.json). The calendar covers **January–October 2023–2026**, with separate **MODIS Aqua / VIIRS NOAA-20** selection. All counts are original detected pixels (no sensor harmonization correction, no physical fire events). November/December are shown as **unavailable**, never zero fires; **2026 is partial**. For 2026, Jan–Jul is SP/SP, August SP Aqua / NRT NOAA-20, and September–October NRT/NRT. NRT is provisional and processing and attribute differences limit comparability.

The existing **2022–2024 pilot A/B** calendar remains a separate option, with its original `data/historico.json`, original geography and distinct scientific methodology. The two histories are not mixed.

- New isolated modules: [history-state.js](history-state.js) (strict original-source projection, fails closed on absent months) and [history-ui.js](history-ui.js) (EN/PT-BR calendar, two sensor controls, original A/B toggle).
- [HIST-02 report and provenance](docs/HIST-02_CALENDARIO.md) and [SCI-03 study](docs/SCI-03_HARMONIZACAO_PADROES.md).
- [CI success — 14 Node tests, 47 Python tests plus desktop/mobile browser acceptance](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43671123377). The browser checked real 2026 SP/NRT labels, missing months, language and preservation of A/B.
- No changes were made to the original TEST-01/01B/SCI-03/TEST-02 datasets or scientific methodology. NASA submission and acceptance checkboxes remain untouched.

## Rodar localmente

Requisitos: **Python 3.11+**, sem dependências externas.

```bash
cd firelens-stack-manauara
python -m http.server 8000
```

Acesse `http://localhost:8000/`. Abrir `index.html` diretamente por `file://` pode bloquear a leitura dos arquivos JSON.

### Testar a engenharia

```bash
python -m unittest discover -s tests -v
```

### Dados recentes NOAA-20 e NOAA-21

A [Area API NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/api/area/) usa fonte `VIIRS_NOAA20_NRT` / `VIIRS_NOAA21_NRT`, `MAP_KEY` e bbox oeste,sul,leste,norte. A [MAP_KEY gratuita](https://firms.modaps.eosdis.nasa.gov/api/map_key/) é enviada ao email cadastrado.

**Segurança:** configure a variável de ambiente `FIRMS_MAP_KEY` localmente ou o segredo GitHub Actions `FIRMS_MAP_KEY`. **Não cole a chave em conversa, frontend ou commits.**

```bash
# Linux/macOS, em ambiente local autorizado:
read -s FIRMS_MAP_KEY && export FIRMS_MAP_KEY
python scripts/firms_nrt.py
```

No Windows PowerShell, forneça a variável via mecanismo seguro de segredo/ambiente disponível; não registre a chave em scripts versionados.

O script usa a geometria versionada (simplificada, compilada a partir de dados IBGE); se o arquivo local não existir, tenta baixar a malha oficial do IBGE; usa a geometria para recortar os pixels no estado do Amazonas (a API só filtra por caixa envolvente). Consulta os dois sensores para os dois dias mais recentes, aplica confiança `n/h`, preserva dia/noite, registra hora UTC da observação e da consulta e grava `data/recente.json`. A interface exibe em Manaus (UTC−4). Não há aplicação do fator histórico a NOAA-21 ou ao NRT.

Se um sensor falhar, **todo o lote é marcado indisponível** e a última captura bem-sucedida é preservada com aviso; não se inventa um zero de ocorrências. A atualização agendada do GitHub Actions é proposta para `:23` de cada hora; horários reais podem variar. A execução manual #1 falhou por indisponibilidade na obtenção da malha; a execução por push #2 comprovou a API e o JSON; uma execução adicional com evento **schedule** em 14/11 às 22:44 AMT foi bem-sucedida ([evidência](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669211275)), embora a pontualidade futura não seja garantida.

### Dados históricos e calendário

Os experimentos independentes disponíveis estão em `data/validacao.json` e `docs/research/` (artefatos fornecidos pela pesquisa).

**Séries já geradas e verificadas no GitHub em 14/11/2026** por [workflow histórico](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632602795). Para reproduzir localmente, obtenha os 6 CSVs anuais do Brasil de 2022–24 da [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/data/country/) e armazene em `firms_cache/` com os nomes exatos utilizados pelo script científico original. Depois:

```bash
python -m scripts.build_historical --cache firms_cache
```

Esse exportador usa os **mesmos filtros, células e método** do arquivo científico original e compara os 4 resultados de WAPE (global diurno) com `data/validacao.json`, abortando se divergirem. O arquivo `data/historico.json` encontra-se `ready` após conferência dos quatro WAPEs globais diurnos; a interface pode apresentar os 72 registros mensais sem dados fabricados.

**Limite:** por usar arquivos por ano UTC sem os dados de 2025, dezembro do calendário solar local pode estar incompleto. Ele é identificado como incompleto, e a versão não alega série 2000–2026 nem limites oficiais do Amazonas para as regiões de validação A/B.

## Organização do repositório

- `index.html`, `style.css`, `app.js`: frontend estático, dois tradutores, camada NRT e calendário.
- `scripts/firms_nrt.py`: API NASA + geometria IBGE + estado de falha e fallback.
- `scripts/build_historical.py`: gerador de séries históricas, validado contra WAPE original.
- `data/recente.json`: somente resultados NRT verdadeiros ou estado indisponível.
- `data/historico.json`: 72 séries mensais de A/B × 2022–2024, geradas com validação WAPE comprovada.
- `data/validacao.json`: resultados experimentais fornecidos pela pesquisa.
- `.github/workflows/atualizar-firms.yml`: rotina NRT horária e publicação de JSON (evento schedule comprovado em 14/11/2026).
- `.github/workflows/construir-historico.yml`: workflow de extração 2022–2024, com WAPE reproduzido e JSON histórico publicado.
- `tests/`: testes sintéticos para lógica, não testes de integração NASA.
- `ESTADO_PROJETO.md`: transferência e status para submissão.

## Fontes e limites científicos

- [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms)
- [NASA FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- [NASA FIRMS atributos de dados](https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs)
- [IBGE Malhas](https://servicodados.ibge.gov.br/api/docs/malhas?versao=3)

Contagens são **detecções de pixels de anomalia térmica**, não incêndios confirmados, área queimada ou concentração de poluentes. O modelo histórico ajusta escala de contagens de NOAA-20 para MODIS Aqua; não corrige nuvens nem garante comparabilidade física. Não é um produto oficial da NASA nem tem seu endosso.

## Publicação (repositório já criado)

1. Repositório público confirmado: https://github.com/Emds96/firelens-stack-manauara — **código publicado e verificado no GitHub**.
2. Código, testes, documentação e workflow já enviados; confira o commit do protótipo `943d897beec55d9d6b6d1d379ddafd3fce5beeae`.
3. Segredo `FIRMS_MAP_KEY` já configurado e verificado pela execução #2; não expor o valor.
4. Execução #2 comprovada: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632228781 ; NOAA-20=145, NOAA-21=243 detecções elegíveis em janela de 2 dias, 388 no total (contagens de pixels, não incêndios).
5. **GitHub Pages publicado e testado** em https://emds96.github.io/firelens-stack-manauara/ ; ver registro ENG-03 em `ESTADO_PROJETO.md`.
6. Se o Actions não conseguir enviar commits, verificar Settings → Actions → General → Workflow permissions: Read and write.

Para a sessão de submissão: usar somente URLs realmente criadas e verificadas; não copiar endereços hipotéticos.

## Uso de IA

O ChatGPT auxiliou na revisão de arquitetura e na criação inicial do código, testes e interface. Os testes locais não constituem validação de dados NRT. Registrar também outras ferramentas usadas de fato antes da submissão.