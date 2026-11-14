# Estado do projeto — FireLens | Dois Tradutores

**Equipe:** Stack Manauara  
**Atualização:** 14/11/2026  
**Versão:** engenharia 0.1.2 (código e testes publicados; integração NASA NRT e site público ainda pendentes)

## Decisões e requisitos

- **ARQ-01 — aprovada conforme confirmação do fundador nesta conversa:** Python + JSON estático + HTML/CSS/JavaScript + GitHub Pages + GitHub Actions. Responsável: sessão principal/equipe. Data: 14/11/2026. Motivo: velocidade, experiência visual e simplicidade. Risco: falhas de integração ou agendamento. Validação: testes locais, dados reais e publicação verificável.
- **REQ-01 — obrigatório:** ingestão NOAA-20/NOAA-21 NRT Amazonas, consulta periódica, datas, indisponibilidade e contingência. Alternativa: somente histórico (superada pela decisão do fundador). Evidência: contrato público da Area API. Risco: credencial/serviço/esquema/recorte. Validação: execução autenticada comprovada por sensor, JSON produzido, agendamento executado e falhas testadas. Responsável: engenharia. Data: 14/11/2026.
- **VAL-TRAD-02 — validação exploratória fornecida:** NOAA-20/Aqua 2022-24 A/B. WAPE global diurno para 2023/2024 demonstrado na pesquisa; não avalia NOAA-21 NRT nem Amazonas inteiro. Responsável: pesquisa. Data: 14/11/2026.
- **DOC-01 — organização paralela:** submissão examina campos e registra alegações baseadas em evidências. Responsável: sessão de submissão. Validação: comparação documentação↔artefatos e revisão humana.

## Artefatos realmente criados nesta entrega

- Código frontend estático: `index.html`, `style.css`, `app.js`.
- Código NRT: `scripts/firms_nrt.py` (não consultou NASA com MAP_KEY real nesta execução).
- Exportador histórico: `scripts/build_historical.py` (ainda sem os CSVs necessários para a extração real).
- Arquivo de agendamento GitHub Actions: `.github/workflows/atualizar-firms.yml` (não executado na plataforma).
- Scripts de testes: `tests/` (detalhes abaixo).
- Dados científicos anteriores, fornecidos pela pesquisa, preservados em `data/validacao.json` e `docs/research/`.
- Estado NRT `data/recente.json` indica indisponibilidade; **não inclui dados fictícios**.
- Estado calendário `data/historico.json` indica extração pendente; **não inclui contagens inventadas**.

## Pendências prioritárias

1. **Repositório criado e verificado:** https://github.com/Emds96/firelens-stack-manauara (público, branch `main`). README, código da aplicação, scripts, dados não sensíveis e testes enviados e verificados no GitHub em 14/11/2026 (commit `943d897beec55d9d6b6d1d379ddafd3fce5beeae`).
2. Criar e configurar segredo `FIRMS_MAP_KEY` com o titular, sem compartilhar a chave em chat.
3. Executar consulta NASA NRT autenticada NOAA-20 e NOAA-21; conferir esquema e recorte IBGE Amazonas.
4. Executar manualmente o workflow e depois verificar disparo automático e atualização verdadeira do JSON.
5. Obter CSVs anuais oficiais de 2022-24, rodar exportador, verificar WAPE e gerar calendário real.
6. Publicar site e verificar a experiência em navegador sem autenticação.
7. Testar Tradutor 2 com pessoas, inclusive linguagem sobre zero detecções.

## Limitações e alertas

- Não há integração externa autenticada demonstrada nesta sessão.
- Não existe série 2000–2026, mapa nacional nem avaliação física de incêndios.
- NASA FIRMS NRT depende de latência de publicação, órbitas, nuvens e qualidade dos sensores.
- As regiões A/B científicas não correspondem às fronteiras do Amazonas.
- Usar o relatório `data/validacao.json` somente como evidência de exploração; não reivindicar validação de NOAA-21 ou da camada recente.

## Evidência e testes

**Executado nesta sessão (14/11/2026):** `python -m unittest discover -s tests -v` → **9 testes aprovados, 0 falhas**. Incluem testes locais de geometria, filtragem, resposta simulada por sensor, contingência e cálculos. **Não são testes com API NASA real, não validam o site em navegador nem uma execução GitHub Actions.** Execução autenticada e teste de publicação continuam pendentes.

## Mensagem para a sessão de submissão

> Há um protótipo local estático e código de ingestão programada preparado, e o repositório público https://github.com/Emds96/firelens-stack-manauara contém protótipo e testes publicados, mas ainda não há site público verificado, sem consulta NOAA-20/NOAA-21 autenticada e sem atualização automática comprovada. Os quatro WAPEs da pesquisa foram mantidos; as séries mensais reais ainda precisam ser geradas. Não descrever NRT ou calendário como operacionais até evidência atualizada.