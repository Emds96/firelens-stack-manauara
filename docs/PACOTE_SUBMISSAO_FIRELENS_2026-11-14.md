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
- **Demo verificada e pública:** apresentação em inglês com sete slides em https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf (teste de abertura sem login e contagem de 7 slides em 14/11/2026). Não confundir o app com a demonstração.

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
**FireLens is a bilingual, map-first educational tool that helps people interpret NASA FIRMS thermal detections without treating every pixel as an individual fire. Visitors explore recent NOAA-20/NOAA-21 observations, read one plain-language explanation per point, and expand technical measurements when needed. A separate archived Eagle's View case shows a real MODIS Aqua pixel and two VIIRS NOAA-20 pixels observed 107 minutes apart on 10 November 2026: a candidate association, not a confirmed shared fire. A 2022–2024 calendar covers two experimental pilot regions A/B, alongside independently evaluated count-scale comparisons. FireLens does not predict fires or claim validated physical harmonization.**

### 3.3 Link to Final Project (confirmed)
**https://emds96.github.io/firelens-stack-manauara/**

**Supplementary source code:** https://github.com/Emds96/firelens-stack-manauara

Both URLs were verified as public. Recheck them in an incognito/private session immediately before final submission.

### 3.4 Link to Project Demo (7 slides, English)

**https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf**

A apresentação foi criada com 7 slides em inglês, com números verificados e avisos científicos. **URL pública e 7 páginas confirmadas** por navegador sem login. A revisão humana final e declaração de uso de IA seguem necessárias antes da submissão definitiva.

### 3.5 Detailed Project Description (draft)
**The problem.** MODIS and VIIRS active-fire products differ in spatial resolution, acquisition characteristics, sensitivity and observation opportunities. Directly comparing their raw counts can be misleading. Moreover, a thermal detection is an observed pixel-level signal, not a confirmed individual fire event.

**Our approach: two translators.** The scientific translator presents native MODIS Aqua and VIIRS NOAA-20 hotspot counts and an interpretable global daytime scaling factor, estimated only from preceding training years. We evaluate it using held-out years, spatial cells of 1° × 1° and local-solar-month aggregation. The human translator describes the meaning of those comparisons with accessible explanations and explicit limitations, rather than hiding uncertainty behind a single score.

**Evidence.** We analyzed consolidated NASA FIRMS Brazil files from 2022–2024 in two rectangular experimental regions, A and B. Daytime global-scaling WAPE (weighted absolute percentage error, relative to observed MODIS counts) was 22.16% and 20.00% in region A for the 2023 and 2024 test years, and 20.85% and 20.15% in region B. Seasonal alternatives were not consistently better. These are errors against MODIS observations, not against actual fire counts or ground truth. The processing workflow checks that the recorded baseline metrics are reproduced before publishing the monthly data.

**What users see.** The bilingual public application now organizes three areas: (1) **Map**, showing real recent NASA FIRMS NOAA-20/NOAA-21 detections with a single accessible explanation and collapsible original attributes; (2) **History**, a clickable 2022–2024 calendar for pilot rectangles A/B, not an Amazonas municipality inventory; and (3) **Understand the data**, which explains different sensor characteristics, historical statistics and limitations. The map also has an explicitly archived Eagle's View case (10 November 2026), showing one MODIS Aqua and two VIIRS NOAA-20 observations; it never mixes these older records with current NRT points. Statistics, methods and source links remain available in expandable sections.

**Implementation.** Python (standard library) retrieves and processes NASA FIRMS data, exports traceable JSON and runs in GitHub Actions. HTML, CSS and JavaScript render the interface through GitHub Pages. The NOAA-20/NOAA-21 API integration and the website were tested on November 14, 2026. A scheduled hourly workflow is configured but its schedule-triggered execution has not yet been verified.

**Limits and next steps.** The current historical analysis covers only 2022–2024, and the pilot rectangles are not the state's administrative boundary. Near-real-time observations are shown separately; our historical NOAA-20 scaling is not presented as validated for NOAA-21. Amazonas near-real-time filtering currently uses a simplified state outline whose boundary accuracy is pending official verification. Weather/cloud effects, orbital coverage and differences in detection capabilities remain important. We aim to strengthen geographic validation, test the schedule and extend historical coverage in future iterations.

### 3.6 AI / Super Intelligence declaration (draft — confirm with team)
**We used ChatGPT (OpenAI) to assist with architecture, code and tests, debugging, scientific review, documentation, communication and project-demo text/design. TinyFish was used to test browser navigation and to assist with drafting/saving project-form entries; these actions were not a final project submission. Satellite measurements were obtained from NASA FIRMS, not generated by AI. Human team members remain responsible for source accuracy, credit/licensing, scientific claims and explicitly approving the final submission. The complete inventory of tools and materials must be reviewed by the team before submitting.**

**Atenção:** o guia exige identificação nos materiais em que IA foi usada (incluindo código/dados, imagens/vídeos/áudio conforme o caso). A sessão de submissão deve verificar autoria humana da ideia e TODOS os serviços de IA empregados nas demais sessões, inclusive geração do layout e conteúdo do PDF de demonstração.

### 3.7 NASA Data and Resources (draft)
- NASA FIRMS (Fire Information for Resource Management System): https://www.earthdata.nasa.gov/data/tools/firms
- FIRMS annual Brazil country CSV archive, 2022–2024: https://firms.modaps.eosdis.nasa.gov/data/country/
- FIRMS Area API: NOAA-20/NOAA-21 NRT for the public map; separately MODIS_NRT Aqua/Terra and VIIRS_NOAA20_NRT for TEST-02 (10–14/11/2026; not an operational map layer): https://firms.modaps.eosdis.nasa.gov/api/area/
- FIRMS active fire data attributes (MODIS/VIIRS): https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs
- Challenge page: https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/

### 3.8 Other resources, code and tools (draft, confirm completeness)
- Open-source tools: Python standard library; HTML; CSS; JavaScript; Leaflet 1.9.4 (BSD-2-Clause); Leaflet.markercluster 1.5.3 (MIT); © OpenStreetMap contributors and OSM tiles. Verify final tile attribution and license compliance.
- Hosting and workflows: GitHub repository, GitHub Pages, GitHub Actions.
- Simplified state boundary compiled from IBGE-based geodata by a third party: https://github.com/henriquemalvar/br-geojson/blob/main/dist/estados.geojson
- Official IBGE geodata service for future boundary confirmation: https://servicodados.ibge.gov.br/api/docs/malhas?versao=3
- ChatGPT / OpenAI for assistance; TinyFish for read-only browser QA. Record use of additional tools/visual assets, licenses and acknowledgments after consulting all team members.
- The site is independent and **not endorsed or certified by NASA**.

## 4. Checklist operacional para a sessão de submissão

1. Confirmar equipe, evento local, proprietário da equipe, data/hora do encerramento segundo o evento e os **campos realmente visíveis** na aba Project.
2. Conferir comprimento máximo de cada campo antes de colar texto. Encurtar sem perder ressalvas.
3. Preencher em inglês título, resumo, descrição, link público do aplicativo, fontes NASA e recursos adicionais. Salvar com **Save Progress**. Usar Lock durante edição.
4. Conferir o PDF com 7 slides em inglês no link da seção 3.4, revisar com a equipe e registrar o aceite humano antes de enviá-lo; aplicar declaração de IA conforme guia.
5. Confirmar lista de ferramentas de IA com os membros e aplicar identificação/atribuições exigidas para conteúdos realmente gerados.
6. Conferir links externos sem login e consistência com `ESTADO_PROJETO.md`; atualizar estatísticas NRT se o snapshot mudar.
7. **Não clicar em Submit final, aceitar termos legais ou afirmar submissão concluída sem autorização expressa do fundador.**
8. Reportar à sessão principal: URL da página de equipe, campos existentes, rascunhos salvos, itens bloqueados, demo pública, fontes, termos pendentes, restrições de prazo e evidência de salvamento.

## 5. Entrega e alinhamento entre sessões

**ENG-04 / DOC-01 — Transferência preparada.** Status: **documentação pronta para preenchimento parcial e revisão**, não submetida.

**Motivo:** evitar perda de contexto e claims não respaldados; alternativa: preencher só após finalizar o software (maior risco de atraso).

**Evidências:** links do GitHub, Pages, Actions, arquivos JSON, teste de navegador e guia NASA 2026 citados aqui.

**Riscos e restrições:** desatualização do NRT, geometria simplificada, cron ainda não validado, demo pública disponível mas aguardando revisão humana, campos/limites dependentes de formulário autenticado.

**Critério de validação:** sessão de submissão conferir formulário, salvar rascunhos com confirmação, referenciar dados atuais, comprovar demo/links públicos e obter aprovação humana do envio.

**Responsável:** engenharia prepara a transferência; sessão de submissão preenche e revisa; fundador/sessão principal aprova. **Data:** 14/11/2026.

> **Próxima missão da submissão:** abrir a página Project da equipe via TinyFish, preencher e salvar somente os campos respaldados por este pacote; levantar os bloqueios. Não enviar definitivamente.

## 6. Atualização de engenharia ENG-04 — 14/11/2026

- **Idiomas implementados e testados:** https://emds96.github.io/firelens-stack-manauara/?lang=en e https://emds96.github.io/firelens-stack-manauara/?lang=pt-BR. English é padrão; PT-BR é selecionável no cabeçalho; formatação de datas, métricas, gráficos e calendário foi testada.
- **Demonstração exigida, entregue e verificada publicamente:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf — **7 slides em inglês, acesso sem login**. Não enviar sem revisão e aprovação humanas.
- **Evidência de QA no navegador:** https://agent.tinyfish.ai/runs/1c6d33da-b39b-4150-9461-4d192ef130ae ; poderá exigir login para ver o histórico do agente, mas a demo e o app são públicos.
- **GitHub Pages build:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43637716718 — sucesso.
- **Disclosure de IA:** o PDF possui rodapé visível de assistência por IA; incluir declaração completa na submissão, conferir alterações feitas por outras ferramentas/sessões e atribuir dados NASA FIRMS.
- **Não alegar:** cron hourly independentemente validado, previsão, validação NRT NOAA-21 do ajuste histórico, precisão cartográfica IBGE oficial ou incêndios físicos individuais.


## 7. Atualização MAP-01 — mapa interativo concluído no MVP 2D

**Nova funcionalidade comprovada em teste Chrome:** o FireLens agora apresenta um mapa interativo 2D com coordenadas reais das detecções recentes NASA FIRMS NOAA-20/NOAA-21, filtros por satélite, agrupamento, lista acessível para seleção de pixels e painel de atributos com dois tradutores em EN/PT-BR.

**Prova técnica:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43641760032 — seleção dos pontos e dois tradutores, filtros, idiomas, layout 390x844 e contingência simulada aprovados. **Documentação:** https://github.com/Emds96/firelens-stack-manauara/blob/main/docs/MAP-01.md

**English paragraph for project description (insert only after checking field limits):**

> Our prototype also includes an interactive 2D map of recent NASA FIRMS NOAA-20 and NOAA-21 thermal-anomaly detections in Amazonas. Visitors can zoom, filter by satellite, select a real coordinate from the map or an accessible list, and inspect observation time, location, confidence class, day/night status, and a scientific and plain-language explanation. An observation represents a detected thermal pixel, not an individual fire or the burned area. The near-real-time layer is separate from our historical MODIS/VIIRS count-scale comparison. Source and observation timestamps, stale-data warnings, and limitations of the simplified state boundary are disclosed.

**Restrições de submissão:** o globo 3D continua **não implementado**. O PDF da demo com sete slides foi criado antes do mapa 2D e ainda não foi atualizado para demonstrá-lo; considerar revisão da apresentação mediante autorização da sessão principal, sem retirar as limitações científicas. Não afirmar cobertura global, incêndios confirmados nem harmonização NRT NOAA-21.


## 8. FIN-01 / UX-03 — versão pronta para conferência humana (14/11/2026)

**Decisão:** fundador aprovou a finalização de três áreas (Mapa / Histórico / Entenda os dados), com o caso real TEST-02 incorporado como **camada histórica separada** e a interpretação unificada por ponto. Sem alteração dos dados originais TEST-01, TEST-01B, SCI-03, TEST-02.

**Artefatos:** `index.html`, `app.js`, `map-ui.js`, `style.css`, `data/caso_visao_aguia_20261110.json`, testes de navegador e nova demo de sete slides com capturas reais. Aplicativo: https://emds96.github.io/firelens-stack-manauara/?lang=en ; alternativa PT-BR: https://emds96.github.io/firelens-stack-manauara/?lang=pt-BR .

**Caso documentado:** MODIS Aqua M-000047, VIIRS NOAA-20 V-000192/V-000193, dia 10/11/2026, 18:02→19:49 UTC (**107 min**); FRP MODIS **18,62 MW**, soma VIIRS **13,09 MW**, diferença **5,53 MW**. O centro dos pixels e `scan × track` fazem apenas aproximação geométrica. T31/TI5 são temperaturas de brilho em canais diferentes. A FRP não é energia conservada nem exige igualdade 1:1. **Não** confirmar incêndio único, sub-bosque, origem de fumaça ou harmonização física.

**Transparência:** em 11/11/2026, 12 Aqua e 222 NOAA-20 diurnos elegíveis foram observados, mas nenhum grupo passou nos quatro limites exploratórios dentro de 120 minutos. O fator global histórico teve WAPE de 23,11% em 2024 e 50,73% em 2025 na avaliação separada Amazonas TEST-01B; isso não demonstra incêndios físicos nem valida aplicação do coeficiente ao NOAA-21.

**QA:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43668744952 — 47 testes Python e fluxo de navegador validado: idioma EN/PT-BR, desktop/celular, pontos, filtros, caso histórico, retorno à camada recente, histórico A/B e falhas simuladas de API. **Demo:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf (até 7 slides, inglês), gerada com capturas reais e validada em GitHub Actions; a revisão final visual e humana continua necessária.

**Submissão NASA:** o formulário real, os aceites de termos/originalidade e Submit for Judging **não foram manipulados** por esta entrega. O histórico `docs/SUBMISSAO_RASCUNHO.md` registra incidente anterior de aceites com persistência não confirmada, que exige avaliação humana. A versão efetivamente salva do formulário também precisa ser conferida antes de qualquer envio.
