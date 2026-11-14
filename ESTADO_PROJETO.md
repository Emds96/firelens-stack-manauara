# Estado do projeto — FireLens | Dois Tradutores

**Equipe:** Stack Manauara  
**Atualização:** 14/11/2026  
**Versão:** engenharia 0.1.4 (integração NRT autenticada comprovada; site público e calendário histórico ainda pendentes)

## Decisões e requisitos

- **ARQ-01 — aprovada conforme confirmação do fundador nesta conversa:** Python + JSON estático + HTML/CSS/JavaScript + GitHub Pages + GitHub Actions. Responsável: sessão principal/equipe. Data: 14/11/2026. Motivo: velocidade, experiência visual e simplicidade. Risco: falhas de integração ou agendamento. Validação: testes locais, dados reais e publicação verificável.
- **REQ-01 — obrigatório:** ingestão NOAA-20/NOAA-21 NRT Amazonas, consulta periódica, datas, indisponibilidade e contingência. Alternativa: somente histórico (superada pela decisão do fundador). Evidência: contrato público da Area API. Risco: credencial/serviço/esquema/recorte. Validação: execução autenticada comprovada por sensor, JSON produzido, agendamento executado e falhas testadas. Responsável: engenharia. Data: 14/11/2026.
- **VAL-TRAD-02 — validação exploratória fornecida:** NOAA-20/Aqua 2022-24 A/B. WAPE global diurno para 2023/2024 demonstrado na pesquisa; não avalia NOAA-21 NRT nem Amazonas inteiro. Responsável: pesquisa. Data: 14/11/2026.
- **DOC-01 — organização paralela:** submissão examina campos e registra alegações baseadas em evidências. Responsável: sessão de submissão. Validação: comparação documentação↔artefatos e revisão humana.

## Artefatos realmente criados nesta entrega

- Código frontend estático: `index.html`, `style.css`, `app.js`.
- Código NRT: `scripts/firms_nrt.py` (NASA NOAA-20 e NOAA-21 consultados com MAP_KEY protegida na execução Actions #2).
- Exportador histórico: `scripts/build_historical.py` (ainda sem os CSVs necessários para a extração real).
- Arquivo de agendamento GitHub Actions: `.github/workflows/atualizar-firms.yml` (execução manual #1 e disparo por push #2 comprovados; cron horário ainda não observado).
- Scripts de testes: `tests/` (detalhes abaixo).
- Dados científicos anteriores, fornecidos pela pesquisa, preservados em `data/validacao.json` e `docs/research/`.
- Estado NRT `data/recente.json` agora contém resposta NASA real com status=ok e 388 detecções elegíveis em 2 dias; dados gerados por execução Actions #2.
- Estado calendário `data/historico.json` indica extração pendente; **não inclui contagens inventadas**.

## Pendências prioritárias

1. **Repositório criado e verificado:** https://github.com/Emds96/firelens-stack-manauara (público, branch `main`). README, código da aplicação, scripts, dados não sensíveis e testes enviados e verificados no GitHub em 14/11/2026 (commit `943d897beec55d9d6b6d1d379ddafd3fce5beeae`).
2. Segredo `FIRMS_MAP_KEY` configurado e teste de consulta real concluído em execução #2.
3. Revisar cientificamente a geometria simplificada vs. IBGE oficial e o comportamento do estado de desatualização no navegador.
4. Acompanhar uma execução automática por cron para validar periodicidade real; já houve execução manual e disparo por push.
5. Obter CSVs anuais oficiais de 2022-24, rodar exportador, verificar WAPE e gerar calendário real.
6. Publicar site e verificar a experiência em navegador sem autenticação.
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


## Evidência e testes

**Local inicial: 9 testes aprovados. GitHub Actions #2 (14/11/2026):** `python -m unittest discover -s tests -v` → **12 testes aprovados, 0 falhas**. Incluem testes locais de geometria, filtragem, resposta simulada por sensor, contingência e cálculos. **Os testes unitários usam dados sintéticos; a consulta NASA real foi comprovada separadamente no mesmo workflow.** Teste no navegador, cron e publicação GitHub Pages ainda pendentes.

## Mensagem para a sessão de submissão

> Código, testes e execução NOAA-20/NOAA-21 NRT estão publicados e comprovados, com 388 detecções elegíveis no JSON da execução #2. O site público ainda não foi confirmado, o cron horário não foi observado e o calendário mensal histórico não está pronto. O contorno do Amazonas é simplificado e requer validação contra geometria oficial. Não afirmar que 388 detecções correspondem a 388 incêndios, nem que a harmonização foi validada para NOAA-21.