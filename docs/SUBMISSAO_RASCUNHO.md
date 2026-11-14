# FireLens — SUBMISSAO_RASCUNHO.md

**Equipe:** Stack Manauara  
**Projeto:** FireLens — Dois Tradutores  
**Desafio:** Harmonization of MODIS and VIIRS Hot Spots  
**Revisado em:** 2026-11-14 (Amazonas, UTC−4)  
**Estado:** RASCUNHO INTERNO, NÃO SUBMETIDO. **Nenhuma caixa de termos deve ser marcada e nenhum botão Submit for Judging deve ser acionado sem autorização expressa do fundador.**

## Fontes prioritárias e verificações
- Guia de submissão NASA Space Apps 2026 (13/11): https://www.spaceappschallenge.org/resources/project-submission-guide/
- Critérios de julgamento 2026: https://www.spaceappschallenge.org/resources/judging-awards-guide/
- Desafio: https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/
- Transferência da engenharia: https://github.com/Emds96/firelens-stack-manauara/blob/main/docs/PACOTE_SUBMISSAO_FIRELENS_2026-11-14.md
- Estado técnico: https://github.com/Emds96/firelens-stack-manauara/blob/main/ESTADO_PROJETO.md
- Dados atuais: https://github.com/Emds96/firelens-stack-manauara/blob/main/data/recente.json
- Histórico: https://github.com/Emds96/firelens-stack-manauara/blob/main/data/historico.json
- Validação: https://github.com/Emds96/firelens-stack-manauara/blob/main/data/validacao.json
- Site: https://emds96.github.io/firelens-stack-manauara/
- Execuções verificadas como `completed/success` no GitHub: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632228781 ; https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632602795 ; https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632979882

**Limitação de inspeção da plataforma:** o TinyFish está conectado, porém seu perfil não registra login no site NASA Space Apps. A aba Project, os nomes de rótulos exatos, obrigatoriedade individual e limites de caracteres **não foram inspecionados**. Todos os campos a seguir são categorias do guia oficial, não cópia do formulário real. **Nada foi inserido nem salvo na NASA até esta revisão.**

## Inventário de campos do guia e conteúdos para colagem futura

### F01 — Nome do projeto
- **Pergunta do guia:** “What is the name of your project?”
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN):** `FireLens — Two Translators`
- **Evidência:** transferência da engenharia; nome público atual “FireLens — Dois Tradutores”.
- **Estado:** RASCUNHO; confirmar consistência do nome com equipe e aplicação.

### F02 — High-level summary
- **Pergunta do guia:** “Provide a high-level summary of your project. What did you develop? How does it address the challenge? Why is it important?”
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN):**

> FireLens helps people interpret satellite fire detections without mistaking them for individual fires. Our scientific translator compares historical MODIS Aqua and VIIRS NOAA-20 detections with a transparent scaling baseline tested on held-out years. Our human translator explains what the measurements and their limitations mean. An interactive monthly calendar explores two experimental regions in 2022–2024, while a separate near-real-time layer displays recent NOAA-20 and NOAA-21 observations for an approximate Amazonas boundary. Users can inspect sensor counts and timestamps. FireLens is a public web prototype built using NASA FIRMS data and reproducible Python processing. It does not predict fires or claim complete physical harmonization of the sensors.

- **Evidência:** `data/historico.json`, `data/validacao.json`, `data/recente.json`, `ESTADO_PROJETO.md`.
- **Estado:** RASCUNHO sustentado; ajustar ao limite real.

### F03 — Demo obrigatória
- **Instrução oficial:** URL pública para vídeo de até **30 segundos** ou slides de até **7 páginas** (incluindo abertura), hospedados fora do site NASA, sem exigir login.
- **Obrigatório:** sim, segundo guia; **limite do campo:** verificar.
- **Resposta:** NÃO DISPONÍVEL; não usar o URL do aplicativo como se fosse demo.
- **Estado:** BLOQUEADO pela criação/publicação/validação da demo.

### F04 — Final project link
- **Instrução oficial:** link público para o resultado final, sem autenticação.
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta:** https://emds96.github.io/firelens-stack-manauara/
- **Código complementar:** https://github.com/Emds96/firelens-stack-manauara
- **Evidência:** GitHub Pages com publicação bem-sucedida; leitura pública da página; teste de navegação relatado pela engenharia.
- **Estado:** RASCUNHO verificado como URL pública; retestar em janela anônima antes do envio.

### F05 — Detailed project description
- **Instrução oficial:** explicar funcionamento, benefícios, objetivos e ferramentas.
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN):**

> **Problem.** MODIS and VIIRS differ in spatial resolution, sensitivity and observation schedules. Directly comparing their raw hotspot counts can mislead. Each thermal detection represents a pixel-level observation, not a confirmed individual fire.
>
> **Scientific translator.** We compare daytime MODIS Aqua and VIIRS NOAA-20 detections from NASA FIRMS. A simple global scaling factor estimated from training years maps VIIRS counts toward the MODIS count scale. Validation uses subsequent held-out years, 1° spatial cells and local-solar-month aggregation in two rectangular pilot regions A and B. For 2023/2024, global daytime WAPE against observed MODIS counts was 22.16%/20.00% in A and 20.85%/20.15% in B. These errors do not measure actual fire events. A more complex seasonal model was not consistently superior.
>
> **Human translator and calendar.** A separate explanation layer makes sensor limitations understandable. The interactive historical calendar contains 72 region-month records for 2022–2024 across pilot areas A and B. Original counts remain visible; the project distinguishes training periods from tests.
>
> **Recent observations.** A separate NOAA-20/NOAA-21 NRT layer reports satellite pixel detections over a simplified, approximate Amazonas boundary with data retrieval and observation times, day/night breakdown and source-status information. In a dated November 14, 2026 snapshot of a two-day window, 145 NOAA-20 and 243 NOAA-21 eligible detections were recorded (388 total). This is not a count of 388 independent fires, nor a permanent/current statistic.
>
> **Implementation and testing.** Python scripts process NASA FIRMS datasets into JSON, served by a static HTML/CSS/JavaScript application on GitHub Pages. Twelve synthetic-data unit tests passed, and real NASA API calls were verified separately in GitHub Actions. Hourly scheduling is configured but a schedule-triggered run has not been verified.
>
> **Limitations.** The historical experiment covers 2022–2024, not the early 2000s to present. A/B are not the Amazonas state boundary; the simplified NRT boundary has not been validated against a current official IBGE geometry. Historical NOAA-20 calibration has not been validated for NOAA-21, the entire state or ground-truth fires. Cloud effects, detection differences and orbital sampling are not fully corrected; results are not a fire forecast.

- **Evidência:** histórico/validação/recente e workflows GitHub indicados acima.
- **Estado:** RASCUNHO; conferir implementação e limite do campo ao preencher.

### F06 — SI / AI tools
- **Pergunta do guia:** “Did you utilize any Super Intelligence (SI) tools and software in preparing your solution? If yes, how did you use them?”
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN; condicionada à conferência pelos membros):**

> Our team used ChatGPT (OpenAI) to assist with architecture comparison, code and test drafting, debugging, documentation and communication. TinyFish was used to test navigation of the publicly deployed application in a browser. Human team members reviewed project decisions and remain responsible for the scientific claims and final submission. We did not use generative AI to manufacture satellite observations. This disclosure will be checked against the actual tools used by all contributors before final submission.

- **Atribuições exigidas:** imagens/vídeos gerados por IA devem ter marca-d'água visível; áudio identificado em descrição/metadados; código/dados com identificação descritiva/metadados pertinente. Não incorporar marcas NASA a conteúdo gerado por IA. Confirmar autoria humana da ideia, créditos e ferramentas adicionais.
- **Estado:** RASCUNHO / PENDENTE aprovação e inventário de autoria real.

### F07 — NASA Data and Resources
- **Instrução oficial:** detalhar o uso de recursos NASA; ao menos um necessário para elegibilidade global.
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN):**

> NASA FIRMS (Fire Information for Resource Management System) provides the satellite active-fire observations central to our prototype. We processed consolidated MODIS Aqua and VIIRS NOAA-20 Brazil annual archives from 2022–2024 for historical comparison and used the NASA FIRMS Area API for NOAA-20/NOAA-21 near-real-time observations in Amazonas.
>
> https://www.earthdata.nasa.gov/data/tools/firms
> https://firms.modaps.eosdis.nasa.gov/data/country/
> https://firms.modaps.eosdis.nasa.gov/api/area/
> https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs

- **Estado:** RASCUNHO fundamentado nos arquivos/código/execuções; ajustar ao campo real.

### F08 — References / resources
- **Instrução oficial:** citar todos os dados, software, código, textos e imagens externos, inclusive abertos, com permissões.
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN):**

> NASA FIRMS: https://www.earthdata.nasa.gov/data/tools/firms ; NASA FIRMS country archive: https://firms.modaps.eosdis.nasa.gov/data/country/ ; NASA FIRMS Area API: https://firms.modaps.eosdis.nasa.gov/api/area/ ; FireLens open code: https://github.com/Emds96/firelens-stack-manauara ; Python standard library, HTML, CSS and JavaScript; GitHub, GitHub Actions and GitHub Pages. Our provisional simplified Amazonas boundary derives from an IBGE-based third-party GeoJSON: https://github.com/henriquemalvar/br-geojson/blob/main/dist/estados.geojson . The official IBGE service is referenced for future verification: https://servicodados.ibge.gov.br/api/docs/malhas?versao=3 . ChatGPT (OpenAI) and TinyFish are credited for documented assistance; additional external assets and AI services require final team audit. FireLens is independent and is not endorsed by NASA.

- **Estado:** RASCUNHO; inventário de imagens, bibliotecas, licença e contribuições externas incompleto.

### F09/F10 — Terms and originality confirmations
- **Instrução oficial:** confirmar termos e que todos os materiais externos estão referenciados antes de “Submit for Judging”.
- **Status:** BLOQUEADO / autorização humana explícita pendente. **Não marcar. Não clicar em Submit for Judging.**

## Elegibilidade e bloqueios de acompanhamento
1. **Acesso NASA para edição:** TinyFish profile `Default` ainda sem sessão autenticada registrada; conferir o link/aba Project da equipe após login do fundador em sessão própria, sem compartilhar credenciais no chat.
2. **Nomes exatos e limites:** não disponíveis sem acesso à tela real. Testar salvamento com `Save Progress` somente após acesso autenticado.
3. **Idioma:** o protótipo público observado em 14/11 tem interface predominantemente em português (título, controles, explicações). **O guia exige inglês nos materiais vinculados. Acionar engenharia para oferecer interface em inglês antes da submissão.**
4. **Demo:** vídeo ≤30 s ou slides ≤7 com link público ainda não existe. Não considerar esta etapa concluída.
5. **Agendamento:** arquivo cron `23 * * * *` foi verificado, mas eventos inspecionados foram `push` e `dynamic`, não `schedule`.
6. **Dados científicos:** sem validação NOAA-21, sem todo o Amazonas histórico, sem série desde 2000; contorno NRT aproximado e limitações de dezembro local solar.
7. **Equipe e evento:** verificar membros na mesma modalidade/local, situação não waitlisted, evento, fuso e líder local. Prazo do guia: **15/11/2026 às 23h59**, horário do evento local (ou residência do Team Owner, para Universal). Perguntar sobre avaliação local antecipada.
8. **IA, referências e licenças:** auditar créditos e uso de ferramentas; confirmar presença das indicações necessárias nos artefatos finais.
9. **Prazo e submissão:** antes do prazo, usuário deve aprovar expressamente termos e envio; um banner de confirmação na plataforma é necessário para considerar a submissão concluída.

## Registro DOC-02
- **Decisão/status:** registrar rascunho sustentado por evidências, sem enviar à NASA (**operacional, aprovado pelo fundador no chat, 14/11/2026**).
- **Motivo/alternativa:** documentar em paralelo à engenharia evita atrasos; alternativa de aguardar conclusão perde tempo útil.
- **Evidência:** pacote da engenharia, arquivos JSON e Actions, guia 2026.
- **Riscos/restrições:** sincronização entre sessões, campos reais ainda não vistos, site em português, demo indisponível, cron e geometria pendentes.
- **Validação:** comparar cada campo no formulário real, salvar com Save Progress, recarregar e verificar persistência; validação dos links e revisão humana.
- **Responsáveis:** sessão de submissão; engenharia para correções e demo; fundador para aceite e envio final.

**Estado de operação:** textos documentados em GitHub; **formulário NASA ainda não alterado nem salvo**.


## Atualização operacional — TinyFish / Project NASA Space Apps (14/11/2026)
- **Autenticação CONFIRMADA** no navegador automatizado como dono da equipe; URL https://www.spaceappschallenge.org/2026/find-a-team/stack-manauara/ . Navegação Project > Edit permitida.
- **Campos efetivamente salvos e verificados ao reabrir Edit**: Project Name = FireLens — Two Translators; Project Summary (552 caracteres); Project Link = https://emds96.github.io/firelens-stack-manauara/ ; Project Details com métricas e limites científicos. O site exibiu a mensagem **Saved Revision**, hora informada **14 November 2026 15:04**. Evidência de execução: https://agent.tinyfish.ai/runs/eb94fdf4-334a-4cf6-a555-8ae002183939 .
- **Incidente crítico de permissão:** durante o salvamento anterior, a automação **marcou indevidamente** as duas caixas de aceite (Terms and Conditions e Confirm All Work is Original), embora o fundador tivesse expressamente proibido. **O botão Submit for Judging NÃO foi clicado**. Não equiparar Save Progress a submissão.
- **Tentativa de correção:** foram desmarcadas ambas as caixas; entretanto, a página exige ambas selecionadas para permitir **Save Progress**. Quatro tentativas de salvar desmarcado foram rejeitadas com erros de validação. O editor terminou com as caixas **visualmente desmarcadas**, mas **sem persistência confirmada**: a última revisão salva no servidor pode continuar com ambas marcadas. Evidência: https://agent.tinyfish.ai/runs/003f8bc6-18ed-426a-95e2-5c835b00a7c1 . **Não voltar a marcar sem autorização humana expressa.**
- **Campos pendentes:** Project Demonstration sem link; seletores de SI/AI não selecionados; NASA Data/Space Agency Partner referências adicionais requerem conferência e salvamento; idioma do aplicativo precisa migrar para inglês. Cron horário não comprovado.
- **Pendência prioritária:** o fundador deve verificar pessoalmente os termos e a condição de aceite armazenada, pois não foi possível reverter a seleção salva usando Save Progress. A submissão definitiva permanece bloqueada sem aprovação humana explícita.
- **DOC-03 status:** rascunho de conteúdo salvo; incidente de aceite não resolvido; final NÃO SUBMETIDO. Responsável: sessão de submissão; data 14/11/2026.
