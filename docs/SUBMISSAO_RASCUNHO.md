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

> FireLens helps people understand NASA FIRMS thermal detections without treating every detected pixel as an individual fire. Its bilingual, map-first web app displays recent NOAA-20/NOAA-21 observations with plain-language explanations and expandable scientific details. A separate historical Eagle's View case shows three real MODIS Aqua/VIIRS NOAA-20 observations from 10 November 2026, 107 minutes apart, as a candidate association—not a confirmed single fire. The app also preserves a 2022–2024 calendar for two experimental pilot regions and independently evaluated count-scale comparisons. FireLens does not predict fires, estimate burned area or claim validated physical harmonization.

- **Evidência:** `data/historico.json`, `data/validacao.json`, `data/recente.json`, `ESTADO_PROJETO.md`.
- **Estado:** RASCUNHO sustentado; ajustar ao limite real.

### F03 — Demo obrigatória
- **Instrução oficial:** URL pública para vídeo de até **30 segundos** ou slides de até **7 páginas** (incluindo abertura), hospedados fora do site NASA, sem exigir login.
- **Obrigatório:** sim, segundo guia; **limite do campo:** verificar.
- **Resposta proposta:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf
- **Estado:** apresentação em inglês com **7 slides**; versão FIN-01 cobre o mapa, o caso científico de 10/11/2026, o histórico e limitações. Confirmar o último deploy público e fazer a revisão humana final antes de qualquer submissão.

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
> **Implementation and testing.** Python scripts process NASA FIRMS datasets into versioned JSON, served by an HTML/CSS/JavaScript application on GitHub Pages. A GitHub Actions regression run passed **47 Python tests** and browser checks for desktop/mobile, the bilingual map, archived Eagle's View case, calendar and failure handling. The TEST-02 research measurements are reproducible offline, but passing tests does not validate identity of physical fires. Hourly scheduling is configured; a schedule-triggered production run requires separate confirmation.
>
> **Limitations.** The historical experiment covers 2022–2024, not the early 2000s to present. A/B are not the Amazonas state boundary; the simplified NRT boundary has not been validated against a current official IBGE geometry. Historical NOAA-20 calibration has not been validated for NOAA-21, the entire state or ground-truth fires. Cloud effects, detection differences and orbital sampling are not fully corrected; results are not a fire forecast.

- **Evidência:** histórico/validação/recente e workflows GitHub indicados acima.
- **Estado:** RASCUNHO; conferir implementação e limite do campo ao preencher.

### F06 — SI / AI tools
- **Pergunta do guia:** “Did you utilize any Super Intelligence (SI) tools and software in preparing your solution? If yes, how did you use them?”
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN; condicionada à conferência pelos membros):**

> Our team used ChatGPT (OpenAI) to assist with architecture and code review, code/test drafting, debugging, scientific communication, documentation and the design/text of the project demonstration. TinyFish supported public-browser testing and assisted with drafting/saving project form entries; the final project submission was not made by these actions. NASA FIRMS supplied the original satellite measurements; generative AI did not manufacture observations. Human team members remain responsible for checking claims, source attribution, permissions and approving any final submission. This statement still requires the team's final complete AI/tool inventory.

- **Atribuições exigidas:** imagens/vídeos gerados por IA devem ter marca-d'água visível; áudio identificado em descrição/metadados; código/dados com identificação descritiva/metadados pertinente. Não incorporar marcas NASA a conteúdo gerado por IA. Confirmar autoria humana da ideia, créditos e ferramentas adicionais.
- **Estado:** RASCUNHO / PENDENTE aprovação e inventário de autoria real.

### F07 — NASA Data and Resources
- **Instrução oficial:** detalhar o uso de recursos NASA; ao menos um necessário para elegibilidade global.
- **Obrigatório/limite:** verificar no formulário.
- **Resposta proposta (EN):**

> NASA FIRMS (Fire Information for Resource Management System) supplies the satellite thermal-anomaly observations central to our prototype. Annual Brazil country files (MODIS Aqua and VIIRS NOAA-20, 2022–2024) support its public historical pilot calendar. The Area API supplies the public map's recent NOAA-20/NOAA-21 NRT detections. In separate TEST-02 observation-level research, we retrieved MODIS_NRT (Aqua/Terra) and VIIRS_NOAA20_NRT for 10–14 November 2026, verified original attributes and explored spatial-temporal candidate associations. This does not establish a physical identity match or validated sensor harmonization.
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

> NASA FIRMS: https://www.earthdata.nasa.gov/data/tools/firms ; NASA FIRMS country archive: https://firms.modaps.eosdis.nasa.gov/data/country/ ; NASA FIRMS Area API: https://firms.modaps.eosdis.nasa.gov/api/area/ ; FireLens source: https://github.com/Emds96/firelens-stack-manauara ; Python, HTML, CSS, JavaScript, GitHub Pages and Actions; Leaflet (BSD-2-Clause), Leaflet.markercluster (MIT) and © OpenStreetMap contributors for the map. The provisional simplified Amazonas boundary derives from an IBGE-based third-party GeoJSON: https://github.com/henriquemalvar/br-geojson/blob/main/dist/estados.geojson ; precision has not been confirmed using the official IBGE service. ChatGPT and TinyFish assisted as disclosed; external assets and additional AI tools must be audited by the team before final submission. Independent project; not endorsed by NASA.

- **Estado:** RASCUNHO; inventário de imagens, bibliotecas, licença e contribuições externas incompleto.

### F09/F10 — Terms and originality confirmations
- **Instrução oficial:** confirmar termos e que todos os materiais externos estão referenciados antes de “Submit for Judging”.
- **Status:** BLOQUEADO / autorização humana explícita pendente. **Não marcar. Não clicar em Submit for Judging.**

## Elegibilidade e bloqueios de acompanhamento — registro histórico anterior a FIN-01

> **Atenção:** os itens abaixo registram o estado de uma revisão preliminar. Alguns estavam pendentes àquela data e foram superados pelos artefatos FIN-01/UX-03 e pelo evento `schedule` comprovado em 14/11 às 22:44 AMT. Para a situação atual, usar a seção “Atualização FIN-01 / UX-03” ao final deste documento. O incidente de aceites ainda requer revisão humana.
1. **Acesso NASA para edição:** TinyFish profile `Default` ainda sem sessão autenticada registrada; conferir o link/aba Project da equipe após login do fundador em sessão própria, sem compartilhar credenciais no chat.
2. **Nomes exatos e limites:** não disponíveis sem acesso à tela real. Testar salvamento com `Save Progress` somente após acesso autenticado.
3. **Idioma:** o protótipo público observado em 14/11 tem interface predominantemente em português (título, controles, explicações). **O guia exige inglês nos materiais vinculados. Acionar engenharia para oferecer interface em inglês antes da submissão.**
4. **Demo:** vídeo ≤30 s ou slides ≤7 com link público ainda não existe. Não considerar esta etapa concluída.
5. **Agendamento, no momento da revisão inicial:** havia somente `push`/`dynamic`. **Atualização verificada:** o evento `schedule` ocorreu e foi bem-sucedido em 14/11/2026 às 22:44 AMT: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669211275 .
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


## Atualização FIN-01 / UX-03 — revisão de engenharia (14/11/2026)

- **Software público:** três áreas bilíngues: **Map / History / Understand the data**; mapa 2D recente NOAA-20/NOAA-21, seleções explicadas em linguagem simples e medições em seção expansível; informações estatísticas secundárias recolhidas sem exclusão.
- **Pesquisa separada no mapa:** caso arquivado de 10/11/2026 (M-000047, V-000192, V-000193). Intervalo de **107 minutos**, FRP MODIS **18,62 MW** e soma VIIRS **13,09 MW**; é uma **associação candidata**, não comprovação de um incêndio único. Dados versionados em `data/caso_visao_aguia_20261110.json`, extraídos dos JSONs reais do TEST-02.
- **Histórico:** calendário de 72 registros mensais 2022–2024 dos recortes experimentais A/B preservado; análise separada TEST-01B indica piora do WAPE de **23,11% em 2024** para **50,73% em 2025** (recorte Amazonas experimental). Não transferir ajuste aos dados NOAA-21 NRT.
- **Evidências:** [GitHub Actions validação de interface](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43668744952): 47 testes Python e verificações em navegador (idiomas, filtros, caso histórico, calendário, desktop/celular e indisponibilidade de dados). [Pesquisa TEST-02](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662809732): reprodução offline dos pares e dados fonte; 47 testes Python. Esses testes não provam harmonização física.
- **Demonstração:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf — sete páginas em inglês, atualizadas com capturas reais do app e limites explícitos. Conferir deploy e revisão humana final.
- **Limites:** nenhum pareamento comprova incêndio único, fogo de sub-bosque, fumaça de Manaus, área queimada, recuperação de detecções ocultas ou previsão. `scan × track` aproxima dimensões sem representar footprint orbital exato; T31/TI5 vêm de canais distintos; FRP é potência e não energia conservada.
- **Não foi feito:** nenhuma edição do formulário real da NASA Space Apps, dos aceites de termos/originalidade ou do botão Submit for Judging por esta missão. Persistência dos aceites anteriores continua pendente de verificação humana.
- **Responsável:** engenharia Stack Manauara. **Status:** texto atualizado em GitHub, **não submetido**. Ainda exige conferência humana de links, créditos, conteúdo final e estado dos campos reais na NASA.
