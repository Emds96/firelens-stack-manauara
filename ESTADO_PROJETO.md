# Estado do projeto — FireLens | Dois Tradutores

**Equipe:** Stack Manauara  
**Atualização:** 14/11/2026  
**Versão:** engenharia 0.2.4 (TEST-02 físico-espacial 10–14/11/2026 executado, dados NASA reais, nenhuma fusão ou alteração da interface)

## Decisões e requisitos

- **ARQ-01 — aprovada conforme confirmação do fundador nesta conversa:** Python + JSON estático + HTML/CSS/JavaScript + GitHub Pages + GitHub Actions. Responsável: sessão principal/equipe. Data: 14/11/2026. Motivo: velocidade, experiência visual e simplicidade. Risco: falhas de integração ou agendamento. Validação: testes locais, dados reais e publicação verificável.
- **REQ-01 — obrigatório:** ingestão NOAA-20/NOAA-21 NRT Amazonas, consulta periódica, datas, indisponibilidade e contingência. Alternativa: somente histórico (superada pela decisão do fundador). Evidência: contrato público da Area API. Risco: credencial/serviço/esquema/recorte. Validação: execução autenticada comprovada por sensor, JSON produzido, agendamento executado e falhas testadas. Responsável: engenharia. Data: 14/11/2026.
- **VAL-TRAD-02 — validação exploratória fornecida:** NOAA-20/Aqua 2022-24 A/B. WAPE global diurno para 2023/2024 demonstrado na pesquisa; não avalia NOAA-21 NRT nem Amazonas inteiro. Responsável: pesquisa. Data: 14/11/2026.
- **DOC-01 — organização paralela:** submissão examina campos e registra alegações baseadas em evidências. Responsável: sessão de submissão. Validação: comparação documentação↔artefatos e revisão humana.

## Artefatos realmente criados nesta entrega

- Código frontend estático: `index.html`, `style.css`, `app.js`.
- Código NRT: `scripts/firms_nrt.py` (NASA NOAA-20 e NOAA-21 consultados com MAP_KEY protegida na execução Actions #2).
- Exportador histórico: `scripts/build_historical.py` (executado em GitHub Actions; seis CSVs NASA FIRMS 2022–2024 processados e métricas WAPE comparadas com a validação).
- Arquivo de agendamento GitHub Actions: `.github/workflows/atualizar-firms.yml` (execução manual #1 e disparo por push #2 comprovados; cron horário ainda não observado).
- Scripts de testes: `tests/` (detalhes abaixo).
- Dados científicos anteriores, fornecidos pela pesquisa, preservados em `data/validacao.json` e `docs/research/`.
- Estado NRT `data/recente.json` agora contém resposta NASA real com status=ok e 388 detecções elegíveis em 2 dias; dados gerados por execução Actions #2.
- Estado calendário `data/historico.json` contém **72 registros mensais verificados** (2022–2024, recortes A/B); dezembro sinalizado incompleto para cruzamento UTC/solar.

## Pendências prioritárias

1. **Repositório criado e verificado:** https://github.com/Emds96/firelens-stack-manauara (público, branch `main`). README, código da aplicação, scripts, dados não sensíveis e testes enviados e verificados no GitHub em 14/11/2026 (commit `943d897beec55d9d6b6d1d379ddafd3fce5beeae`).
2. Segredo `FIRMS_MAP_KEY` configurado e teste de consulta real concluído em execução #2.
3. Revisar cientificamente a geometria simplificada vs. IBGE oficial e o comportamento do estado de desatualização no navegador.
4. Acompanhar uma execução automática por cron para validar periodicidade real; já houve execução manual e disparo por push.
5. Geração histórica concluída em Actions #1 do workflow histórico; conferir experiência do calendário no site e investigar expansão temporal futura.
6. **Concluído parcialmente:** site publicado no GitHub Pages e navegação principal verificada sem login; ainda faltam verificação específica em dispositivos pequenos e auditoria de acessibilidade.
7. Testar Tradutor 2 com pessoas, inclusive linguagem sobre zero detecções.

## Limitações e alertas

- Integração NASA NRT autenticada demonstrada pela execução #2, mas o recorte geográfico simplificado ainda exige validação científica de precisão.
- Não existe série 2000–2026, mapa nacional nem avaliação física de incêndios.
- NASA FIRMS NRT depende de latência de publicação, órbitas, nuvens e qualidade dos sensores.
- As regiões A/B científicas não correspondem às fronteiras do Amazonas.
- Usar o relatório `data/validacao.json` somente como evidência de exploração; não reivindicar validação de NOAA-21 ou da camada recente.

## Diagnóstico GitHub Actions #1 e correção ENG-02

- Execução oficial do workflow #1: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43631724021 — terminou verde, mas `data/recente.json` registrou `status=unavailable`, `last_success_utc=null`, `detections=[]`, erro `URLError` antes da consulta NASA.
- O segredo `FIRMS_MAP_KEY` estava presente no ambiente (mas seu valor não foi exposto).
- Correção técnica publicada: geometria simplificada do Amazonas versionada (`data/amazonas_ibge.geojson`, fonte secundária baseada no IBGE), permitindo não requisitar a geometria a cada execução; limitações em `docs/GEOMETRIA_AMAZONAS.md`.
- O workflow foi ajustado para **falhar de fato** se a ingestão não concluir, ainda preservando o JSON de estado e executando testes antes da consulta. Incluiu gatilho de push limitado ao código/configuração, sem laço para commits de dados.
- **Situação:** correção validada na execução #2 de 14/11/2026; sensores NOAA-20/21 retornaram dados elegíveis reais. O teste não comprova ciclo horário cron nem precisão oficial dos limites.

## Resultado verificável NASA FIRMS NRT — execução #2

- Execução: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632228781 — `status=completed`, `conclusion=success`.
- 12 testes unitários passaram; consulta a ambos sensores concluída, segredos protegidos.
- `data/recente.json`: `status=ok`, `last_success_utc=2026-11-14T19:28:03Z`, `last_observation_utc=2026-11-14T05:48:00Z`, `count=388`.
- NOAA-20: **145** (128 dia, 17 noite); NOAA-21: **243** (139 dia, 104 noite); janela dois dias, confiança n/h, contorno simplificado do Amazonas.
- Erros de fronteira ainda possíveis; são detecções de pixels, não incêndios individuais. Última observação retornada precede a consulta por mais de 13 horas.
- Próximos marcos: testar visualização em navegador, publicação GitHub Pages, cron e séries mensais históricas.


## Resultado histórico reproduzido — calendário 2022–2024

- Execução: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632602795 — concluída com sucesso.
- Seis CSVs oficiais Brasil, MODIS Aqua e VIIRS NOAA-20 (2022, 2023, 2024), foram ingeridos; 72 registros de região × ano × mês publicados.
- O código interromperia a publicação se qualquer um dos quatro WAPE globais diurnos divergissem da validação de entrada; execução passou.
- `data/historico.json` status `ready`, preserva métodos, contagens de pixels, fonte e limitações. Fator é treinado com anos anteriores, sem vazamento no ano de teste.
- Contagens mensais não são incêndios distintos nem representam cobertura histórica de 2000–2026; dezembro tem alerta de incompletude local solar.

## Publicação e teste público do aplicativo — ENG-03

- **Status:** publicação GitHub Pages verificada e teste funcional em navegador **aprovado para o percurso principal**, não equivalente a validação científica completa.
- **URL pública:** https://emds96.github.io/firelens-stack-manauara/
- **GitHub Pages build:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632979882 — execução concluída com sucesso em 14/11/2026.
- **Teste de navegador TinyFish (somente leitura):** https://agent.tinyfish.ai/runs/b3f9aecf-ee8e-4601-be45-e9d2ca268f75 ; a ferramenta pode exigir conta para abrir o histórico de execução.
- **Verificações realizadas no navegador:** navegação entre as três abas; NOAA-20=145, NOAA-21=243, total=388; horário da última captura e última observação exibidos; quatro resultados de validação; calendário 2022–2024 (36 células por região); seleção A/B; clique em mês e detalhe textual; nenhuma mensagem de erro ou travamento relatado no percurso.
- **Ressalva:** o teste não constituiu auditoria formal de acessibilidade, teste multirresolução ou análise de performance; não prova que o agendamento por cron ocorreu.
- **Limites científicos preservados:** recortes A/B não correspondem a Amazonas inteiro; contorno NRT simplificado; observações NRT não são incêndios individuais e não validam a calibração NOAA-21.
- **Decisão operacional ENG-03 / implementada:** manter publicação estática GitHub Pages, sem dependência de autenticação do visitante. Motivo: demonstração rápida, ampla acessibilidade e independência de servidor próprio. Alternativas: Streamlit/servidor de aplicação (mais custo operacional). Evidência: execução de Pages e teste funcional em navegador. Risco: cache ou atualizações NRT com latência e dependência de Actions, proteção da chave no backend. Validação: inspeção de site público, arquivos JSON disponíveis, navegação de dados. Responsável: engenharia Stack Manauara, data 14/11/2026.

## ENG-04 — Idiomas EN/PT-BR e demonstração pública

- **Decisão implementada (pedido do fundador):** interface bilingue com apenas English (padrão para jurados) e Português (Brasil), com troca rápida no cabeçalho, preferência local e links com idioma na URL.
- **Motivo:** atender a exigência da submissão em inglês preservando usabilidade em português. Alternativas: traduzir só documentação (insuficiente para jurados), serviço de tradução externo (dependência e risco de terminologia).
- **Evidência de publicação do código:** arquivos `index.html`, `app.js`, `style.css` versionados; apresentação de 7 páginas PDF inglês em `demo/FireLens_7_Slide_Demo_2026.pdf`; landing page `demo/index.html`.
- **Demo pública:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf (**verificada sem login, 7 slides**).
- **Riscos:** descompasso entre termos PT/EN, troca de língua com dados em memória, tela menor, status NRT envelhecido; apresentar como snapshot datado.
- **Validação:** testes em navegador de ambas línguas, calendário, abas e PDF público; revisar precisão com equipe humana. Status: **testes pós-implantação aprovados** no navegador; precisão cartográfica e cron ainda pendentes.
- **Responsável/data:** Engenharia Stack Manauara, 14/11/2026.

## ENG-04 — Confirmação de publicação e QA bilíngue

- **GitHub Pages:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43637716718 — concluído com sucesso em 14/11/2026, head `dc6c7e6f05c98ba62e1cbe8f4254a41cc0265528`.
- **QA navegador (TinyFish, somente leitura):** https://agent.tinyfish.ai/runs/1c6d33da-b39b-4150-9461-4d192ef130ae — execução concluída, sem autenticação e sem alterações em dados.
- **Verificados:** modo inglês inicial; troca EN → PT-BR → EN; navegação entre três abas; datas AMT; painel NOAA-20/NOAA-21; quatro WAPEs; 36 meses por região A/B; mês SET/2024 em português e inglês, com formatação de números; mês selecionado preservado após trocar idioma; documento PDF público aberto com 7 slides sem login.
- **Demonstração pública (link para submissão):** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf ; alternativa de visualização: https://emds96.github.io/firelens-stack-manauara/demo/
- **Limites:** a apresentação inclui um calendário esquemático explicitamente identificado como ilustrativo; os números reais constam no site. A revisão humana final da apresentação continua necessária antes do envio oficial. Não houve auditoria formal de acessibilidade completa nem testes em todas as resoluções.

## Evidência e testes

**Local inicial: 9 testes aprovados. GitHub Actions #2 (14/11/2026):** `python -m unittest discover -s tests -v` → **12 testes aprovados, 0 falhas**. Incluem testes locais de geometria, filtragem, resposta simulada por sensor, contingência e cálculos. **Os testes unitários usam dados sintéticos; a consulta NASA real foi comprovada separadamente no mesmo workflow.** Teste no navegador, cron e publicação GitHub Pages ainda pendentes.

## Mensagem para a sessão de submissão

> Código, dados NOAA-20/NOAA-21 e séries históricas estão publicados; site público https://emds96.github.io/firelens-stack-manauara/ e navegação das três seções confirmados por teste em navegador. Foram 388 detecções elegíveis na captura de 14/11/2026 (dois dias, contorno simplificado). Histórico tem 72 registros mensais nos recortes A/B e métricas reproduzidas. Cron horário, precisão de fronteira e testes mais completos de acessibilidade/responsividade seguem pendentes. Não confundir pixels detectados com incêndios nem atribuir harmonização validada a NOAA-21.
## MAP-01 — Mapa interativo 2D entregue e validado em navegador

**Status:** implementado e testado por automação Chrome; globo 3D **não autorizado**.

- **Decisão/ID:** MAP-01. Adotar Leaflet 1.9.4 e Leaflet.markercluster 1.5.3 sobre arquitetura estática ARQ-01, com agrupamento opcional e lista paginada acessível de 8 detecções reais. Alternativas: MapLibre GL, SVG Canvas próprio, globo 3D (rejeitado para esta fase).
- **Motivo:** facilidade de explorar localização e atributos por ponto com pouco custo técnico; a lista mantém acesso aos dados mesmo quando os marcadores estão agrupados.
- **Evidências:** workflow Chrome https://github.com/Emds96/firelens-stack-manauara/actions/runs/43641760032 ; 5 testes Node de coordenadas/filtros/falhas, 12 testes Python históricos/NRT e teste Chrome com selecionador de pontos, filtros NOAA-20/21, idioma EN/PT-BR, celular virtual de 390x844 e falha simulada da fonte. Nenhum erro JavaScript não capturado na execução aprovada. Código em map-data.js, map-ui.js, tests/test_map_browser.cjs, tests/test_map.cjs e docs/MAP-01.md.
- **Publicação:** integração no website público https://emds96.github.io/firelens-stack-manauara/ (seção Observações Recentes); build GitHub Pages atual mais recente deve ser conferido antes de alegar revisão visual de cada dispositivo.
- **Riscos/limites:** geometria do Amazonas simplificada, OSM tiles e bibliotecas via CDN dependem de terceiros; o teste móvel Chrome não substitui inspeção manual em vários aparelhos. Detecções não são incêndios, áreas queimadas ou estimativa do MODIS. Capturas >4 h são sinalizadas como desatualizadas; sem dados não se inventa zero.
- **Validação:** cobertura das interações principais e de estados indisponíveis confirmada em Chrome; revisão visual humana do mapa e de telas móveis ainda recomendável.
- **Responsável/data:** engenharia Stack Manauara, 14/11/2026.
- **Pendências fora da missão:** cron horário real, malha IBGE oficial e qualquer globo 3D. Demonstração PDF de sete slides criada antes do MAP-01; a sessão principal pode pedir atualização dela para incluir mapa, se houver prazo.


## TEST-01 — História de atividade do fogo no Amazonas (14/11/2026)

- **Decisão e status:** TEST-01, **parcialmente aprovado como análise exploratória histórica**, sob revisão científica da sessão principal. Nenhuma interface alterada; TEST-02 não iniciado.
- **Evidência:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43646531478 — **20 testes Python passaram**. Six CSVs oficiais NASA FIRMS Brasil (MODIS Aqua e VIIRS NOAA-20, 2023–2025) recuperados, auditados por hash e filtrados por contorno simplificado Amazonas.
- **Relatório auditável:** `docs/TEST-01_HISTORICO.md`. **Dados separados:** `data/test01_historico_amazonas.json`. **Código:** `scripts/test01_historico.py`, `scripts/test01_report.py`. **Testes:** `tests/test_test01_historico.py`.
- **Resultados observados:** MODIS Aqua 18.246/23.009/4.306 e NOAA-20 74.740/90.746/21.382 pixels elegíveis diurnos em 2023/2024/2025. Pico mensal NOAA-20: setembro 2023, agosto 2024, agosto 2025. Células espaciais de 1° recorrentes identificadas e listadas no relatório.
- **Validação independente:** fator global treinado 2023→2024 gerou WAPE 23,109%; fator treinado 2023–2024→2025 gerou WAPE **50,731%**. **Não assumir coeficiente estável** nem equivalência física.
- **Bloqueios:** CSVs anuais 2026 dos dois sensores retornaram HTTP 404; a API do IBGE retornou URLError e foi utilizada geometria secundária simplificada. Sem comparação 2026 equivalente; não interpretar registros ausentes como ausência de fogo.
- **Alternativas consideradas:** transferir coeficientes A/B (rejeitado), método mais complexo sem evidência (não adotado), fator global basal testado (adotado experimentalmente), NRT de 48 h em lugar de série anual (não comparável).
- **Riscos e validação futura:** nuvens, diferenças de resolução/horário de passagem, contorno, período curto e erro alto em 2025; testar geometria IBGE oficial, ampliar anos, conferir janelas 2026 equivalentes e revalidar qualquer ajuste antes de uso na interface.
- **Responsável/data:** engenharia Stack Manauara, 14/11/2026. **Aprovação científica final:** sessão principal, pendente.


## TEST-01B — Investigação 2025 / Recuperação 2026 (14/11/2026)

- **ID / decisão / status:** TEST-01B, execução técnica concluída; validação científica final **pendente da sessão principal**. Não substituir TEST-01. Não iniciar TEST-02.
- **Motivo:** esclarecer WAPE elevado em 2025 e recuperar 2026 sem presumir CSVs anuais. Alternativas: aceitar coeficiente global sem revisão (rejeitada), solicitar arquivo histórico por formulário autenticado (identificado, não realizado), consultar SP/NRT por intervalo e auditar cada resposta (adotado).
- **Evidência real:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43649496639 — jobs diagnóstico 2025, coleta NASA 2026 e publicação concluídos com sucesso; os testes existentes e os sete testes TEST-01B passaram. `docs/TEST-01B_INVESTIGACAO.md`, `data/test01b_resultados.json`, `scripts/test01b_diagnose.py`, `scripts/test01b_2026.py`, `scripts/test01b_report.py`, `tests/test_test01b.py`.
- **TEST-01 preservado / conferido:** os seis arquivos anuais 2023–2025 foram novamente baixados; seus hashes SHA-256 e contagens foram comparados aos originais do TEST-01 e os WAPEs foram reproduzidos.
- **2025:** 2024 teve WAPE ajustado 23,109% e 2025 teve 50,731%. Os pixels MODIS diminuíram 81,29%; erro absoluto ajustado diminuiu 58,92%. O ajuste **superestimou o MODIS em 1.024,447 pixels** em 2025 (viés positivo de 23,79% da referência), contra viés negativo de 855,514 em 2024. **Outubro, agosto e setembro de 2025 somaram 68,983% do erro absoluto**. Os dez locais em células de 1° com maior erro responderam por 36,993%. São associações matemáticas, **não explicações físicas causais**.
- **2026 recuperado:** 1º/01–14/11/2026, 318 dias de calendário consultados para cada sensor pela NASA FIRMS Area API: MODIS Aqua 8.356 pixels elegíveis diurnos (**2.417 SP + 5.939 NRT**, 64 janelas); NOAA-20 44.243 (**2.098 SP + 42.145 NRT**, 65 janelas). Todas as 129 janelas responderam com sucesso; nenhum dia careceu de fonte reportada na disponibilidade da API. Status de consulta completa **não comprova cada passagem orbital ou céu sem nuvens**.
- **Fontes e cortes de processamento verificados:** MODIS SP até 31/08/2026 e NRT a partir 01/09; NOAA-20 SP até 31/07 e NRT a partir 01/08, conforme disponibilidade recuperada em 14/11. NRT não traz o campo `type` nos CSVs consultados; SP o traz. Não equiparar classes de processamento nem deduzir tendência física.
- **Comparação exploratória com mesmas datas:** 2023 Aqua 17.809 / NOAA-20 72.042; 2024 22.644 / 89.207; 2025 4.128 / 20.049; 2026 8.356 / 44.243. Todos até 14 de novembro UTC. **Comparação apenas descritiva e provisória:** fontes históricas consolidadas e SP/NRT 2026 não têm cobertura/qualidade instrumental perfeitamente equivalente, e 14/11 pode estar incompleto. Não aplicar fator histórico a NOAA-21; nem afirmar anomalias, risco ou tendências de incêndios.
- **Fonte e limites:** https://firms.modaps.eosdis.nasa.gov/api/area/ ; https://firms.modaps.eosdis.nasa.gov/api/data_availability/ . A FIRMS Archive Download oficial foi identificada, mas exige Earthdata/e-mail para solicitar período; não foi falsamente registrada como solicitação feita. Arquivo direto nrt3 também requer token Earthdata próprio. A chave FIRMS_MAP_KEY já protegida foi usada apenas no runner; manifests públicos não a contêm.
- **Riscos:** geometria Amazonense simplificada ainda não confrontada com IBGE oficial, amostragem por órbita/nuvem, atraso e eventual substituição NRT, diferença de esquema (`type`), curva de validação instável, último dia parcial.
- **Validação futura:** revisar SP/NRT por sensor, ausência de passagens, polígono IBGE oficial, comparabilidade temporal/espacial e reavaliar qualquer calibração em período independente. **Responsável/data:** engenharia Stack Manauara, 14/11/2026; aprovação final: sessão principal.


## SCI-03 — Harmonização por padrões de atividade relativa (14/11/2026)

- **ID e decisão / status:** SCI-03 — **experimento executado e documentado; proposta de aplicação pendente de aprovação científica pela sessão principal**. Não substituir harmonização TEST-01 ou aplicar ao site sem nova decisão. TEST-02 não iniciado.
- **Motivo e alternativas:** comparar se sensores concordam sobre meses e células mais ativos usando porcentagens por sensor, sem depender de escala absoluta; alternativas: apenas contagens globais, fator global (controle já testado) e modelos mais complexos (não justificados pelo prazo/evidência).
- **Evidência:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43653164498 — **35 testes Python aprovados**, seis arquivos anuais oficiais 2023–2025 novamente confrontados por SHA-256 e contagens contra TEST-01; **124 janelas** NASA FIRMS 2026 (jan-out UTC) consultadas com sucesso. Análise calculada por células de 1° e meses UTC: `scripts/sci03_sources.py`, `scripts/sci03_compare.py`, `scripts/sci03_report.py`, `tests/test_sci03.py`. Relatório: `docs/SCI-03_HARMONIZACAO_PADROES.md`. Dados não operacionais: `data/sci03_resultados.json` (métricas, esquema, janelas/hashes) e `data/sci03_agregados.json` (4.434 registros agregados e contagens originais de pixels).
- **Verificação offline de reprodutibilidade:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43653579596 — 35 testes unitários e recálculo exato das métricas a partir dos **4.434 registros de célula-mês** de `data/sci03_agregados.json`, sem internet, nova consulta NRT ou uso da MAP_KEY. `scripts/sci03_verify.py` reavalia comparações de 2023–2026, baselines e controle de invariância; resultado `offline_verified`.
- **Resultado de 2026 (janeiro–outubro completo):** MODIS Aqua **8.002**, NOAA-20 **42.636** pixels elegíveis; correlação Spearman mensal **0,948** e espacial **0,925**; distância TV mensal **0,0768** e espacial **0,1131**; **8 das 10 células** mais ativas em comum. Setembro é o mês com mais registros em ambos os sensores. **Dados combinam SP/NRT e não provam equivalência física ou incêndios individuais.**
- **SP/NRT estratificado (2026):** janeiro–julho ambos SP, 264 MODIS / 2.098 NOAA20; concordância espacial Spearman **0,628**, TV **0,333**, 6/10 células mais ativas em comum; agosto MODIS SP/NOAA20 NRT; setembro–outubro ambos NRT (Spearman espacial **0,921**). Diferença por faixa pode resultar de muitos fatores não isolados; a menor contagem de pixels MODIS no primeiro período é limitação da estabilidade das métricas.
- **2025:** Spearman mensal **0,976** e espacial **0,918**, TV espacial **0,139**, 8/10 células mais ativas em comum. Isso não elimina WAPE absoluto de 50,73% obtido no TEST-01 (ano inteiro). Controle absoluto para jan-out teve WAPE de **22,09%** em 2024 (treino 2023) e **47,49%** em 2025 (treino 2023–2024); períodos diferentes dos resultados anuais originais.
- **Fato matemático:** normalizar contagens para participação (%) não muda rankings nem distribuição de um sensor em relação à simples multiplicação por fator global positivo; por si só **não melhora o método de harmonização física**. É útil para explicar concentração temporal e geográfica observada, mas deve manter ambos sensores, informações originais e ressalvas.
- **Restrições e riscos:** sensibilidade, resolução, nuvens e órbitas diferentes; sem denominador de oportunidades observacionais; geometria estadual simplificada não validada oficialmente; 2026 SP/NRT, NRT sem `type` e sujeito a revisões; 1° pode esconder padrões locais; desempenho em períodos de poucos registros pode variar.
- **Validação e próximo passo:** revisar métricas e fontes por produto/período, testar com malha IBGE oficial, considerar cobertura orbital e qualidade; nenhum uso operacional antes de aprovação da sessão principal.
- **Responsável/data:** Engenharia Stack Manauara, 14/11/2026.


## TEST-02 — Visão da Águia: análise físico-espacial (10–14/11/2026)

- **ID / decisão / status:** TEST-02, experimento observacional autorizado e executado, **aprovação científica pendente da sessão principal**. O método não demonstrou identidade única de incêndios nem foi integrado à operação. Alternativas: fundir registros pelas 4 travas (rejeitada sem validação independente) e manter pares candidatos com incertezas (implementada).
- **Fontes e evidências:** NASA FIRMS Area API, MODIS_NRT (Terra/Aqua) e VIIRS_NOAA20_NRT, com FIRMS_MAP_KEY somente como segredo GitHub. Consulta de 10/11/2026 (5 dias) recortada pelo polígono Amazonas simplificado, com atenção a Manaus/Autazes/Careiro (lon −61,5 a −58,5, lat −4,5 a −2,0). CSVs originais 321 linhas MODIS (147 dentro de AM) e 1.420 linhas VIIRS (760 dentro); hashes e todas as colunas fonte preservadas nos dados separados.
- **11/11/2026:** 12 MODIS Aqua, 5 MODIS Terra, 267 VIIRS NOAA-20 de todas as confianças e turnos; filtros diurnos elegíveis reproduzem exatamente **12 Aqua e 222 NOAA-20 do TEST-01B**. Dentro da BBOX Manaus/Autazes/Careiro: 2 MODIS e 35 NOAA-20 totais. Nenhuma dupla MODIS–VIIRS encaixada em mesma data/turno com defasagem ≤120 min; **zero grupos de quatro travas compatíveis** no dia.
- **Categorias em 11/11 — somente os 222 VIIRS elegíveis:** 0 compatíveis com as quatro travas; 15 sobreposição geométrica mas >120min; 1 borda ≤2,5km; **202 isolados espacialmente >2,5km de uma caixa aproximada MODIS** (FRP médio 7,8863 MW, área nominal média 0,1722 km², T4 média 339,0872 K e T11 média 296,3736 K); 4 não resolvidos. **Esses 202 não são automaticamente incêndios invisíveis ao MODIS, de sub-bosque, nem causa de fumaça.**
- **Categorias para 267 VIIRS de todos turnos/confianças:** 0 diretos, 19 defasados, 1 borda, 243 isolados, 4 não resolvidos. No dia 11, zero I4=367 K ou I4<250 K; em toda janela, cinco VIIRS registraram I4=367 K e nenhum I4<250 K.
- **10/11/2026 — dois grupos candidatos, não incêndios confirmados:** M-000047 Aqua / V-000192, V-000193 (Δt 107min, ΔT11 3,38K, ΣFRP 13,09 MW vs Aqua 18,62 MW, razão 0,703) e M-000048 Aqua / V-000194 (107min, 4,05K, 3,91 MW vs 4,70 MW, razão 0,832); perto do entorno focal. Critérios exploratórios 5K/8K e FRP 0,5–2,0 **não validados pela NASA como teste de identidade**.
- **Limitações físicas:** valores scan×track descrevem dimensões aproximadas, não footprints orientados Level-2; T31 e TI5 são temperaturas de brilho de pixels detectados, não fundo não queimado independente; FRP é potência instantânea, não energia conservada; sobreposições podem multiplicar associações; NRT provisório, polígono estadual simplificado; sem máscaras de nuvens, cobertura de passagens ou evidência independente sobre fumaça em Manaus ou sub-bosque.
- **Artefatos separados:** `scripts/test02_fisico.py`, `scripts/test02_report.py`, `scripts/test02_verify.py`, `tests/test_test02_fisico.py`; `data/test02_observacoes_20261110_14.json` (todas as colunas da fonte para cada pixel no recorte), `data/test02_resultados.json`, `docs/TEST-02_VISAO_AGUIA.md`.
- **Validação:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662712437 — ingestão autenticada real, 47 testes, 5 dias e categorias checadas; https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662809732 — reprocessamento offline idêntico de cada atributo e par, sem credencial/rede, 47 testes.
- **Responsável/data:** engenharia Stack Manauara, 14/11/2026. **Próximo passo científico proposto:** estudar footprints Level-2 e oportunidades de observação/cobertura sob autorização da sessão principal, antes de afirmar harmonização físico-espacial.
