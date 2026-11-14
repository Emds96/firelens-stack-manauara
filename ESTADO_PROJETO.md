# Estado do projeto — FireLens | Dois Tradutores

**Equipe:** Stack Manauara  
**Atualização:** 14/11/2026  
**Versão:** engenharia 0.1.7 (EN/PT-BR e demo de 7 slides publicados; teste pós-implantação pendente)

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
- **Demo pública:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf (conferir HTTP e visualização após publicação do Pages).
- **Riscos:** descompasso entre termos PT/EN, troca de língua com dados em memória, tela menor, status NRT envelhecido; apresentar como snapshot datado.
- **Validação:** testes em navegador de ambas línguas, calendário, abas e PDF público; revisar precisão com equipe humana. Status: código preparado e publicado; testes pós-implantação ainda pendentes no momento deste registro.
- **Responsável/data:** Engenharia Stack Manauara, 14/11/2026.

## Evidência e testes

**Local inicial: 9 testes aprovados. GitHub Actions #2 (14/11/2026):** `python -m unittest discover -s tests -v` → **12 testes aprovados, 0 falhas**. Incluem testes locais de geometria, filtragem, resposta simulada por sensor, contingência e cálculos. **Os testes unitários usam dados sintéticos; a consulta NASA real foi comprovada separadamente no mesmo workflow.** Teste no navegador, cron e publicação GitHub Pages ainda pendentes.

## Mensagem para a sessão de submissão

> Código, dados NOAA-20/NOAA-21 e séries históricas estão publicados; site público https://emds96.github.io/firelens-stack-manauara/ e navegação das três seções confirmados por teste em navegador. Foram 388 detecções elegíveis na captura de 14/11/2026 (dois dias, contorno simplificado). Histórico tem 72 registros mensais nos recortes A/B e métricas reproduzidas. Cron horário, precisão de fronteira e testes mais completos de acessibilidade/responsividade seguem pendentes. Não confundir pixels detectados com incêndios nem atribuir harmonização validada a NOAA-21.