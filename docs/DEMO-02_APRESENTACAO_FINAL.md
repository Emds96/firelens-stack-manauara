# DEMO-02 — Apresentação final do FireLens (sete slides)

**Projeto:** FireLens — Stack Manauara  
**Desafio:** NASA Space Apps Challenge 2026 — Harmonization of MODIS and VIIRS Hot Spots  
**Data:** 14/11/2026 (America/Manaus)  
**Estado:** gerador atualizado; PDF produzido, testado e **publicado**. Revisão final humana de comunicação/submissão ainda pendente; **não submetido à NASA**.

## 1. Artefato publicado

- **PDF público (sem autenticação):** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf
- **Arquivo versionado:** `demo/FireLens_7_Slide_Demo_2026.pdf` — 1.658.875 bytes; Git blob SHA `ee9dc63eeba7b661c8a71508049f6184b8c5963f`.
- **Commit de publicação do PDF:** https://github.com/Emds96/firelens-stack-manauara/commit/cc69c6035bd8ce87e3251b5a51dc05f72b1bb671
- **Gerador mantido, não refeito do zero:** `scripts/build_final_demo.py`. Paleta escura, laranja/turquesa, tipografia e estrutura de sete slides preservadas.
- **Capturas reais da aplicação:** `scripts/capture_demo_map.cjs`, obtidas em navegador Chromium do FireLens servido a partir do código público versionado. A captura de Histórico seleciona o **HIST-02 estadual principal** (e não a visualização A/B oculta), verifica 40 células mensais disponíveis e oito indisponíveis para o sensor selecionado, `2026 PARTIAL` e o registro **MODIS Aqua setembro/2026 = 3.518 pixels / NRT**. O screenshot é de software real; não é uma imagem criada para simular observação de satélite.

## 2. Sumário dos sete slides

1. **FireLens:** desafio oficial e equipe completa, sem cargos inventados. O título é somente FireLens.
2. **Map:** captura real do mapa NOAA-20/NOAA-21 NRT, explicação curta e detalhes consultáveis.
3. **Eagle's View:** captura real do caso 10/11/2026, um MODIS Aqua e dois VIIRS NOAA-20, 107 minutos de diferença; comparação FRP **18,62 vs 13,09 MW**, com rótulo explícito de associação **candidata**, nunca incêndio confirmado.
4. **Method:** dimensões `scan × track` apenas aproximadas, horário real, temperaturas T31/TI5 em canais diferentes, FRP como potência (não energia conservada). Os quatro aspectos não são quatro provas físicas.
5. **History — HIST-02:** **Amazonas janeiro–outubro 2023–2026 como principal**; cada satélite selecionado independentemente, novembro/dezembro indisponíveis nesta série, 2026 parcial e SP/NRT por mês. **Pilotos A/B 2022–2024 citados separadamente**, sem agregar as séries.
6. **Evidence:** dois grupos candidatos no dia 10/11; em 11/11, **12 Aqua e 222 NOAA-20** diurnos elegíveis, com zero grupos que passaram todos os critérios exploratórios em até 120 minutos; fator global histórico com WAPE independente **23,11% (2024) → 50,73% (2025)**.
7. **Limits and impact:** usos permitidos da ferramenta, resultados observados x candidatos x não demonstrados; link do site; créditos **NASA FIRMS, OpenStreetMap, assistência ChatGPT** e declaração de projeto independente, não endossado pela NASA.

Todos os slides estão em inglês, exceto nomes próprios e marcas/termos técnicos.

## 3. Integrantes no primeiro slide — conferência exata

A extração automática do PDF produzido confirmou todos os nomes, com caracteres Unicode e acentos corretos:

1. Crhystopher Ferreira de Aguiar
2. Eder Magalhães dos Santos
3. Leonardo de Souza Pinheiro
4. Luís Henrique da Silva Carvalho
5. Mirna do Amaral Maquiné Nascimento
6. Paulo Elias Cajado Pinto

Não foram atribuídos cargos ou responsabilidades individuais. Uma fonte Unicode embutida garante a representação dos acentos. A inspeção visual dos slides renderizados verificou distribuição em duas colunas, legibilidade e ausência de corte.

## 4. Evidências de geração, testes e publicação

- **Geração + teste PDF:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43674081194 — **sucesso**. Verificou exatamente **7 páginas**, seis nomes extraídos corretamente da página inicial, desafio e identidade, conteúdo HIST-02, números TEST-02 e WAPE, créditos e avisos científicos, três screenshots, PDF visualmente renderizável e coordenadas de texto dentro das páginas.
- **HIST-02 e funcionalidades existentes:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43671284780 — **14 testes Node**, **47 testes Python**, navegador Chromium em desktop e celular, sensor, idiomas e modo piloto/estado.
- **Deploy do commit com PDF final:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43674137685 — `completed/success`, commit `cc69c6035bd8ce87e3251b5a51dc05f72b1bb671`.
- **Acesso público comprovado:** requisição sem login ao PDF respondeu **HTTP 200**, com **7 páginas** e texto extraído incluindo seis nomes e HIST-02; a página inicial respondeu HTTP 200 e contém link público para o PDF exatamente no caminho preservado.
- **Revisão visual:** sete páginas renderizadas pelo pipeline; os slides 1, 3 e 5 foram inspecionados também como imagens geradas a partir do PDF real, verificando texto acentuado, carregamento de tiles da captura do mapa e legibilidade do calendário.

**Limite dos testes:** comprovam integridade do PDF, exibição e reprodutibilidade do conteúdo versionado; não equivalem à avaliação de jurados nem validam cientificamente o vínculo físico entre detecções.

## 5. Modificações e proteção do escopo

Arquivos modificados pelo DEMO-02:
- `scripts/capture_demo_map.cjs` — captura do calendário HIST-02, conferência da opção estadual como padrão e tempo de carregamento do mapa histórico.
- `scripts/build_final_demo.py` — seis integrantes, fontes Unicode, título/desafio, conteúdo estadual HIST-02 e ressalvas de WAPE/testes.
- `.github/workflows/build-final-demo.yml` — verificações das sete páginas, nomes acentuados, captura recente, renderização e publicação de binário sem conflito.
- `demo/FireLens_7_Slide_Demo_2026.pdf` — mesmo caminho de publicação.
- `docs/DEMO-02_APRESENTACAO_FINAL.md` e `ESTADO_PROJETO.md` — documentação e rastreabilidade.

**Sem alteração:** interface do site, código de sensores, arquivos NASA FIRMS, métodos TEST-01/01B/SCI-03/TEST-02, `data/sci03_agregados.json`, calendário operacional e campos/aceites no site da NASA.

## 6. Pendências / registro de decisão

**DEMO-02 — execução técnica concluída; revisão de apresentação pelo fundador/equipe humana pendente.**

- **Motivo:** alinhar o PDF público com a versão final implementada do HIST-02 e com a equipe de seis pessoas.
- **Alternativas:** recriar a apresentação (rejeitada); alterar somente a fonte do screenshot e as declarações mantendo os sete slides (aprovada pelo escopo).
- **Evidência:** SCI-03/HIST-02 original, TEST-02, JSON do caso de 10/11, CI, PDF público acessível.
- **Restrições/riscos:** snapshots datados, NRT provisório, diferença SP/NRT, região Amazonas aproximada, status de submissão NASA não consultado. O PDF é inglês; aplicação permanece bilíngue.
- **Validação:** 7 páginas, seis nomes completos, screenshot HIST-02 real, linguagem cientificamente defensável, URL pública e CI verde.
- **Responsável:** engenharia Stack Manauara; **data:** 14/11/2026.
- **Próxima ação prioritária:** revisão humana do PDF e do rascunho da submissão para consistência; somente o fundador autoriza posteriormente `Submit for Judging`.

Não foram marcadas caixas de termos/originalidade nem realizada submissão.
