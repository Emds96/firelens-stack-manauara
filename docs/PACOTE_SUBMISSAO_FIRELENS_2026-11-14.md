# FIRELENS — PACOTE DE TRANSFERÊNCIA PARA SUBMISSÃO
**NASA Space Apps Challenge 2026 | Equipe Stack Manauara | 14/11/2026**

> **Uso:** entregar à sessão especializada em Submissão. Documento operacional preparado pela Engenharia, não equivale à submissão final. Texto destinado aos jurados está em inglês. Confirmar os nomes dos campos e limites na página **Project** da equipe antes de preencher.

## 1. Missão e situação comprovada

- **Projeto público:** FireLens — Dois Tradutores.
- **Equipe:** Stack Manauara.
- **Desafio:** Harmonization of MODIS and VIIRS Hot Spots.
- **Ideia:** Tradutor 1 (científico: comparação MODIS Aqua × VIIRS NOAA-20, com estimativas na escala MODIS e testes históricos) + Tradutor 2 (humano: explicações acessíveis e ressalvas). Um calendário histórico e uma camada de observações recentes complementam a proposta.
- **Aplicação online verificada em navegador:** https://emds96.github.io/firelens-stack-manauara/
- **Código e documentação públicos:** https://github.com/Emds96/firelens-stack-manauara
- **Estado de engenharia:** https://github.com/Emds96/firelens-stack-manauara/blob/main/ESTADO_PROJETO.md
- **Última verificação funcional de navegador:** 14/11/2026, teste TinyFish de navegação sem autenticação; as três abas funcionaram sem erro observado. Evidência: https://agent.tinyfish.ai/runs/b3f9aecf-ee8e-4601-be45-e9d2ca268f75 (histórico pode exigir login).
- **GitHub Pages:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632979882
- **Autorização:** fundador confirmou ARQ-01, REQ-01 obrigatória e organização DOC-01 paralela. A equipe humana deve conferir e autorizar a submissão definitiva.

### Confirmado na aplicação em 14/11
1. Ingestão NASA FIRMS autenticada de NOAA-20 e NOAA-21 NRT: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632228781 e https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632461532
2. JSON NRT: https://github.com/Emds96/firelens-stack-manauara/blob/main/data/recente.json — consulta bem-sucedida em **2026-11-14 19:30:39 UTC** (15:30:39 em Manaus), última observação recebida **2026-11-14 05:48 UTC** (01:48 em Manaus), **388 detecções elegíveis em janela de 2 dias** no recorte simplificado do Amazonas: **145 NOAA-20 e 243 NOAA-21**, confiança normal ou alta, dia/noite descritos separadamente. **São pixels detectados, não 388 incêndios.** Valores são um retrato datado, não uma contagem permanente.
3. Séries mensais verificadas: https://github.com/Emds96/firelens-stack-manauara/blob/main/data/historico.json — **72 registros** (regiões experimentais A/B × 2022–2024 × 12 meses); extração a partir de seis CSVs anuais Brasil NASA FIRMS e comparação automática das métricas WAPE: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632602795
4. Testes: **12 testes unitários aprovados** no GitHub Actions (dados sintéticos para filtros, geometria, datas, fallback e matemática). A consulta externa foi verificada **separadamente** na execução do workflow.
5. Site: abas Observações Recentes, Tradutor Científico e Calendário Histórico navegáveis; resultados científicos, contagens por sensor, detalhes de meses e recortes A/B apresentados.

### Pendente / NÃO alegar como concluído
- Execução periódica horária por **cron**: arquivo GitHub Actions configurado para `:23` de cada hora, mas ainda não foi observada uma execução disparada por `schedule`; execuções por acionamento manual e `push` foram comprovadas.
- A malha NRT do Amazonas é uma **geometria simplificada secundária baseada em IBGE**; precisão da fronteira **não foi validada contra malha oficial atualizada**. Fonte e risco: https://github.com/Emds96/firelens-stack-manauara/blob/main/docs/GEOMETRIA_AMAZONAS.md
- Os recortes históricos A/B **não são as fronteiras do estado do Amazonas**. O teste dos fatores históricos **não foi validado para NOAA-21, toda a Amazônia ou incêndios no terreno**.
- Série histórica desde o início dos anos 2000 não implementada; o MVP tem **2022–2024**.
- Dezembro pode estar incompleto na normalização do mês por hora solar local; o site sinaliza.
- Não existe validação de qualidade do ar de Manaus, previsão de incêndios, correção de nuvens, intervalos de incerteza calibrados, nem auditoria formal de acessibilidade/múltiplos dispositivos.
- **Link obrigatório de DEMO (vídeo de até 30 segundos ou apresentação de até 7 slides): AINDA NÃO FORNECIDO.** Não usar o site como substituto automático da demo.

## 2. Inventário da submissão oficial (guia publicado em 13/11/2026)

Guia vigente: https://www.spaceappschallenge.org/resources/project-submission-guide/

**Campos e conteúdos descritos pelo guia (conferir texto exato e limites no formulário autenticado):**
- Project Name / Title → seção 3.1.
- High-Level Project Summary → seção 3.2.
- Link to Project Demo → PENDENTE, seção 3.4.
- Link to Final Project → seção 3.3.
- Detailed Project Description → seção 3.5.
- SI/AI tools and how used → seção 3.6 (confirmar autoria/uso real com a equipe).
- NASA Data and Resources → seção 3.7.
- All data, code, text, image resources and tools → seção 3.8.
- Termos e condições / envio → **somente após autorização humana explícita.**

**Regras verificadas no guia 2026:**
- Página da submissão e materiais vinculados: **inglês**; vídeo pode ser falado em português **com legendas em inglês**; slides em inglês.
- Demo pública obrigatória, **vídeo de no máximo 30 segundos OU até sete slides incluindo título/introdução**. O site NASA não aceita upload de vídeos/documentos diretamente: anexar link público.
- A página permite imagens JPG/PNG/GIF até 10 MB; vídeos/docs exigem links externos acessíveis sem login.
- Salvar frequentemente em **Save Progress**; recurso de **Lock** para evitar edições simultâneas. A plataforma orienta testar links em janela privada.
- Prazo: **15/11/2026 às 23h59 no fuso do evento local**; para Universal Event, fuso da residência do dono da equipe. Confirmar evento/fuso antes de enviar.
- O guia de 2026 exige declarar uso de SI/IA, inclusive nos metadados/descrições pertinentes. Conteúdo visual gerado por IA deve ter **marca-d'água visível**; áudio gerado, identificação na descrição/metadados; código/dados gerados, identificação em texto/metadados. **Não usar elementos de marca NASA em conteúdo gerado por IA.**
- Critérios citados no guia: **Impact, Creativity, Validity, Relevance, Presentation**. A equipe deve garantir correspondência entre texto, demonstração e evidências.

## 3. Textos em inglês prontos para RASCUNHO (revisar limites no formulário)

### 3.1 Project Title
**FireLens — Two Translators**

Nome público também pode aparecer como **FireLens | Dois Tradutores**, desde que a equipe confirme consistência com os materiais.

### 3.2 High-Level Project Summary (draft)
**FireLens helps people interpret satellite fire detections without mistaking them for individual fires. Our first translator compares historical MODIS Aqua and VIIRS NOAA-20 detections using a transparent, out-of-sample-tested scaling baseline. Our second translator explains what the measurements and their uncertainties actually mean. An interactive monthly calendar explores two experimental regions during 2022–2024, while a separate near-real-time layer displays recently retrieved NOAA-20 and NOAA-21 observations for an approximate Amazonas state boundary. Users can inspect original counts, the historical comparison and observation timestamps. FireLens is a public web prototype built with NASA FIRMS data and reproducible Python processing; it does not claim to predict fires or fully harmonize the physical properties of these sensors.**

### 3.3 Link to Final Project (confirmed)
**https://emds96.github.io/firelens-stack-manauara/**

**Supplementary source code:** https://github.com/Emds96/firelens-stack-manauara

Both URLs were verified as public. Recheck them in an incognito/private session immediately before final submission.

### 3.4 Link to Project Demo (BLOCKED)
**PENDENTE — NÃO INSERIR LINK INVENTADO.**

Criar material de demonstração público: vídeo ≤30 segundos ou slides ≤7, usando o site real e explicações corretas. Verificar acessibilidade sem login. Não substituir este campo pelo endereço do aplicativo sem confirmar que o formulário aceita essa interpretação (o guia pede link de demo separado do link do projeto).

### 3.5 Detailed Project Description (draft)
**The problem.** MODIS and VIIRS active-fire products differ in spatial resolution, acquisition characteristics, sensitivity and observation opportunities. Directly comparing their raw counts can be misleading. Moreover, a thermal detection is an observed pixel-level signal, not a confirmed individual fire event.

**Our approach: two translators.** The scientific translator presents native MODIS Aqua and VIIRS NOAA-20 hotspot counts and an interpretable global daytime scaling factor, estimated only from preceding training years. We evaluate it using held-out years, spatial cells of 1° × 1° and local-solar-month aggregation. The human translator describes the meaning of those comparisons with accessible explanations and explicit limitations, rather than hiding uncertainty behind a single score.

**Evidence.** We analyzed consolidated NASA FIRMS Brazil files from 2022–2024 in two rectangular experimental regions, A and B. Daytime global-scaling WAPE (weighted absolute percentage error, relative to observed MODIS counts) was 22.16% and 20.00% in region A for the 2023 and 2024 test years, and 20.85% and 20.15% in region B. Seasonal alternatives were not consistently better. These are errors against MODIS observations, not against actual fire counts or ground truth. The processing workflow checks that the recorded baseline metrics are reproduced before publishing the monthly data.

**What users see.** Our public static web application contains: (1) recent detections from NASA FIRMS NOAA-20/NOAA-21 near-real-time feeds; (2) a scientific validation view comparing scaling methods; and (3) a clickable 2022–2024 calendar for the two pilot regions. The recent layer shows distinct observation and update timestamps, counts by sensor and explanations about latency. The historical calendar preserves original counts and distinguishes calibrated comparisons from training periods.

**Implementation.** Python (standard library) retrieves and processes NASA FIRMS data, exports traceable JSON and runs in GitHub Actions. HTML, CSS and JavaScript render the interface through GitHub Pages. The NOAA-20/NOAA-21 API integration and the website were tested on November 14, 2026. A scheduled hourly workflow is configured but its schedule-triggered execution has not yet been verified.

**Limits and next steps.** The current historical analysis covers only 2022–2024, and the pilot rectangles are not the state's administrative boundary. Near-real-time observations are shown separately; our historical NOAA-20 scaling is not presented as validated for NOAA-21. Amazonas near-real-time filtering currently uses a simplified state outline whose boundary accuracy is pending official verification. Weather/cloud effects, orbital coverage and differences in detection capabilities remain important. We aim to strengthen geographic validation, test the schedule and extend historical coverage in future iterations.

### 3.6 AI / Super Intelligence declaration (draft — confirm with team)
**We used ChatGPT (OpenAI) to assist with architecture comparison, code and test generation, debugging, documentation and communication drafts. TinyFish was used to perform read-only browser testing of the publicly deployed prototype. Team members reviewed and approved major decisions and are responsible for scientific claims, code, presentation and final submission. The project does not rely on generative AI to invent scientific observations. We have not represented AI-generated content as NASA-approved material. This disclosure will be updated to include every additional AI/SI tool actually used by the team.**

**Atenção:** o guia exige identificação nos materiais em que IA foi usada (incluindo código/dados, imagens/vídeos/áudio conforme o caso). A sessão de submissão deve verificar autoria humana da ideia e TODOS os serviços de IA empregados nas demais sessões.

### 3.7 NASA Data and Resources (draft)
- NASA FIRMS (Fire Information for Resource Management System): https://www.earthdata.nasa.gov/data/tools/firms
- FIRMS annual Brazil country CSV archive, 2022–2024: https://firms.modaps.eosdis.nasa.gov/data/country/
- FIRMS Area API, VIIRS NOAA-20 NRT and NOAA-21 NRT: https://firms.modaps.eosdis.nasa.gov/api/area/
- FIRMS active fire data attributes (MODIS/VIIRS): https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs
- Challenge page: https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/

### 3.8 Other resources, code and tools (draft, confirm completeness)
- Open-source programming tools: Python standard library; HTML; CSS; JavaScript.
- Hosting and workflows: GitHub repository, GitHub Pages, GitHub Actions.
- Simplified state boundary compiled from IBGE-based geodata by a third party: https://github.com/henriquemalvar/br-geojson/blob/main/dist/estados.geojson
- Official IBGE geodata service for future boundary confirmation: https://servicodados.ibge.gov.br/api/docs/malhas?versao=3
- ChatGPT / OpenAI for assistance; TinyFish for read-only browser QA. Record use of additional tools/visual assets, licenses and acknowledgments after consulting all team members.
- The site is independent and **not endorsed or certified by NASA**.

## 4. Checklist operacional para a sessão de submissão

1. Confirmar equipe, evento local, proprietário da equipe, data/hora do encerramento segundo o evento e os **campos realmente visíveis** na aba Project.
2. Conferir comprimento máximo de cada campo antes de colar texto. Encurtar sem perder ressalvas.
3. Preencher em inglês título, resumo, descrição, link público do aplicativo, fontes NASA e recursos adicionais. Salvar com **Save Progress**. Usar Lock durante edição.
4. Marcar link de demo como **bloqueado**; pedir à sessão principal ou à equipe material final público e revisar se vídeo/slide cumpre prazo, idioma e requisitos de IA.
5. Confirmar lista de ferramentas de IA com os membros e aplicar identificação/atribuições exigidas para conteúdos realmente gerados.
6. Conferir links externos sem login e consistência com `ESTADO_PROJETO.md`; atualizar estatísticas NRT se o snapshot mudar.
7. **Não clicar em Submit final, aceitar termos legais ou afirmar submissão concluída sem autorização expressa do fundador.**
8. Reportar à sessão principal: URL da página de equipe, campos existentes, rascunhos salvos, itens bloqueados, demo pública, fontes, termos pendentes, restrições de prazo e evidência de salvamento.

## 5. Entrega e alinhamento entre sessões

**ENG-04 / DOC-01 — Transferência preparada.** Status: **documentação pronta para preenchimento parcial e revisão**, não submetida.

**Motivo:** evitar perda de contexto e claims não respaldados; alternativa: preencher só após finalizar o software (maior risco de atraso).

**Evidências:** links do GitHub, Pages, Actions, arquivos JSON, teste de navegador e guia NASA 2026 citados aqui.

**Riscos e restrições:** desatualização do NRT, geometria simplificada, cron ainda não validado, demo inexistente, campos/limites dependentes de formulário autenticado.

**Critério de validação:** sessão de submissão conferir formulário, salvar rascunhos com confirmação, referenciar dados atuais, comprovar demo/links públicos e obter aprovação humana do envio.

**Responsável:** engenharia prepara a transferência; sessão de submissão preenche e revisa; fundador/sessão principal aprova. **Data:** 14/11/2026.

> **Próxima missão da submissão:** abrir a página Project da equipe via TinyFish, preencher e salvar somente os campos respaldados por este pacote; levantar os bloqueios. Não enviar definitivamente.
