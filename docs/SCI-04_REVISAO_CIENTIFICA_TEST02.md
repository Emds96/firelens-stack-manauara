# SCI-04 — Revisão científica do TEST-02 e auditoria da demo/submissão

**Equipe:** Stack Manauara · **Projeto:** FireLens — Dois Tradutores  
**Data local de revisão:** 14/11/2026 (Manaus, UTC−4)  
**Status:** **PROPOSTA PARA APROVAÇÃO CIENTÍFICA; NÃO INTEGRADA AO SITE; NÃO SUBMETIDA À NASA.**

## 1. Conclusão recomendada

**Pode-se demonstrar que observações MODIS e VIIRS ocorreram próximas no espaço e no tempo e apresentar seus atributos térmicos e radiativos lado a lado. As quatro verificações, porém, identificam apenas grupos candidatos; não comprovam a identidade de um incêndio físico, não constituem harmonização física validada e não autorizam fusão automática de detecções.**

Três níveis que toda comunicação deve distinguir:

- **OBSERVADO:** coordenadas centrais, data/hora UTC/AMT, satélite, dimensões aproximadas do pixel, T4/T11 de brilho e FRP registrado pela FIRMS.
- **ASSOCIAÇÃO CANDIDATA:** encaixe em retângulo aproximado, distância temporal calculada e comparação descritiva de T11/FRP.
- **NÃO DEMONSTRADO:** mesmo incêndio único, fogo sob o dossel, continuidade espacial de frente de fogo, falha de detecção MODIS, origem da fumaça de Manaus, área queimada e validade operacional da harmonização.

## 2. Dados TEST-02 usados nesta revisão — fatos verificados no JSON publicado

Fontes de auditoria:
- [Relatório TEST-02](https://github.com/Emds96/firelens-stack-manauara/blob/main/docs/TEST-02_VISAO_AGUIA.md).
- [Resultados por grupo, dia e proveniência](https://github.com/Emds96/firelens-stack-manauara/blob/main/data/test02_resultados.json).
- [Observações originais NASA e todos os atributos por linha](https://github.com/Emds96/firelens-stack-manauara/blob/main/data/test02_observacoes_20261110_14.json).
- [Execução real NASA, testes e publicação](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662712437).
- [Recomputação independente offline, 47 testes](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662809732).

**Captura:** FIRMS Area API, MODIS_NRT (Aqua e Terra) e VIIRS_NOAA20_NRT, 10–14/11/2026 UTC; 147 pixels MODIS e 760 VIIRS NOAA-20 dentro do polígono simplificado estadual, preservando as colunas NASA. Esses totais incluem noites e confianças distintas.

**Integridade de origem:**
- CSV MODIS_NRT, SHA-256 `caa13ba58a9f00fd3b1bc6ff3cc7f729f4e98a05d7015543540af352744f3301`.
- CSV VIIRS_NOAA20_NRT, SHA-256 `ed567a392b3ab65d548ec05065da367c574d1ffc8a511bbd7afcd05cd7a96ad1`.
- O contorno `data/amazonas_ibge.geojson` é simplificado, de fonte secundária; não está certificado contra a geometria oficial IBGE.

### 2.1 Dia 11/11 — diferença de observação, NÃO quantidade de incêndios

| Recorte estadual | Pixel/detecção |
|---|---:|
| MODIS Aqua, diurno com filtros históricos | **12** |
| MODIS Terra, todos os turnos | **5** |
| NOAA-20, diurno confiança normal/alta | **222** |
| NOAA-20, todas as confianças e turnos | **267** |

Entre **222** pixels VIIRS diurnos elegíveis: **0** compatíveis com todas as quatro condições em até 120 min; **15** com sobreposição espacial aproximada mas defasagem >120 min; **1** próximo da borda; **202** a >2,5 km de qualquer caixa MODIS aproximada no mesmo dia; **4** não resolvidos. A soma é 222. **Não chamar os 202 de incêndios invisíveis ou sub-bosque:** podem ser passagens diferentes, nuvens, capacidades distintas, ausência de observação comparável, fontes não vegetais ou outros fatores não controlados.

Na caixa regional Manaus/Autazes/Careiro (lat −4,5 a −2,0; lon −61,5 a −58,5), o estudo encontrou **2 MODIS Terra e 35 NOAA-20** de todos os turnos/confianças em 11/11; **não** houve MODIS Aqua nessa caixa sob a consulta usada. Não há prova de causa de fumaça.

### 2.2 Dia 10/11 — dois grupos candidatos com medições reais

| MODIS Aqua | NOAA-20 associados | Horários UTC (VIIRS → Aqua) | Intervalo | T31 MODIS / média TI5 VIIRS | FRP MODIS / soma VIIRS | Razão soma VIIRS / MODIS |
|---|---|---|---:|---|---|---:|
| M-000047 (-3,44421; -59,61359) | V-000192, V-000193 | 18:02 → 19:49 | 107 min | 297,36 / 293,98 K (Δ 3,38 K) | 18,62 / 13,09 MW | 0,703 |
| M-000048 (-3,41922; -60,31168) | V-000194 | 18:02 → 19:49 | 107 min | 297,60 / 293,55 K (Δ 4,05 K) | 4,70 / 3,91 MW | 0,832 |

**Interpretação permitida:** proximidade geométrica aproximada, passagem com 107 minutos de diferença e atributos térmicos/radiativos comparáveis nos critérios exploratórios. **Interpretação proibida:** confirmação de dois incêndios ou calibração dos sensores.

A ausência de grupos que satisfaçam todas as condições em 11/11 significa *“nenhum grupo passou nos critérios e janela adotados”*, não *“nenhum dos satélites viu o mesmo evento”*.

## 3. Revisão física — quatro verificações reformuladas

1. **Geometria (dimensões, não pegada exata).** `scan × track` informa dimensões de pixel em quilômetros na FIRMS. A regra ΔX/ΔY emprega retângulos alinhados a latitude/longitude, **não** a orientação real da varredura, geolocalização Level-2 ou polígonos instrumentais. O teste é aproximação espacial que pode dar falso encaixe ou perder encaixes reais.
2. **Tempo (diferença observada, não identificação).** Calcular diferença de `acq_date + acq_time` em UTC e mostrar AMT (UTC−4). O limite de 120 minutos é **parâmetro exploratório**, não intervalo orbital universal nem prova de permanência de um incêndio. Manter mesmo dia UTC e turno como regras do teste, não como verdade física.
3. **Temperatura de brilho (canais não idênticos).** `bright_t31` MODIS e `bright_ti5` VIIRS são temperaturas de brilho de pixels detectados em bandas distintas no infravermelho térmico. **Não são uma medição isolada independente da temperatura de fundo sem fogo.** Comparar ΔT11 de modo descritivo; 5/8 K foram apenas limites de sensibilidade do experimento, **não tolerância universal ou científica validada**.
4. **Potência radiativa (não conservação).** `frp` está em megawatts, é potência radiativa integrada do pixel no instante de observação. Mostrar FRP MODIS e soma dos VIIRS associados, com razão e diferença, mas **não exigir igualdade 1:1 nem chamar “conservação de energia”**. FRP varia com momento, detecção, algoritmo, saturação e geometria; pixels VIIRS podem entrar em mais de uma caixa MODIS.

**Fontes NASA para atributos (consultadas na auditoria):**
- https://firms.modaps.eosdis.nasa.gov/content/descriptions/FIRMS_MODIS_Firehotspots.html
- https://firms.modaps.eosdis.nasa.gov/content/descriptions/FIRMS_VIIRS_Firehotspots.html
- https://firms.modaps.eosdis.nasa.gov/content/active_fire/
- https://www.earthdata.nasa.gov/s3fs-public/2025-06/VIIRS_C2_AF-375m_User_Guide_1.2.pdf (produto Level-2 oferece atributos adicionais, incluindo contexto de temperatura de fundo)

## 4. Proposta de apresentação pública simples (não aplicada)

**Decisão recomendada:** manter **sete slides totais**, sem acrescentar um oitavo, e substituir o atual **slide 5** (“72 validated monthly records”) por um caso SCI-04 claro. Relembrar o calendário histórico com uma frase no slide 3 e preservar os demais conteúdos. Ajustar o slide 7 com limites físicos e eventual crédito de IA. **Não modificar o PDF sem aprovação da sessão principal.**

### Texto inglês proposto para substituir o slide 5 (pronto para revisão humana)

> **Two satellites. Nearby thermal observations. Not a confirmed same fire.**
>
> **10 November 2026 — Amazonas — NASA FIRMS NRT**
>
> VIIRS NOAA-20: 18:02 UTC (14:02 AMT), 2 detected pixels; combined FRP **13.09 MW**.
>
> MODIS Aqua: 19:49 UTC (15:49 AMT), 1 detected pixel; FRP **18.62 MW**.
>
> The observations are **107 minutes apart**, near each other using **approximate pixel dimensions**. MODIS T31: **297.36 K**; mean VIIRS TI5: **293.98 K**. These are brightness temperatures from different channels, not directly equivalent background temperatures.
>
> **One candidate association — not proof of one physical fire.**
>
> On **11 November**, **12 Aqua** and **222 NOAA-20** eligible daytime detections were recorded, but **no group met all four exploratory conditions within 120 minutes**.
>
> *No fire identity, burned area, smoke source or physical sensor correction is established.*

*O exemplo acima é o grupo M-000047 + V-000192/V-000193, não o grupo inteiro de 10/11 nem um pixel identificado por fronteira exata.*

### Texto inglês proposto para reforçar o slide 7

> **Research limits:** Satellite hotspot detections are pixel observations, not confirmed individual fires. `scan × track` gives approximate dimensions, not exact satellite footprints. Time proximity, brightness temperatures and FRP comparisons suggest candidate associations but do not prove physical fire identity. Our 2026 NRT analysis is exploratory and is not integrated into operational predictions or alerts.
>
> **Attribution:** NASA FIRMS provides the original satellite data. Presentation drafting and design were assisted by ChatGPT; scientific decisions and project submission remain with the human team. FireLens is independent and is not endorsed by NASA.

A quantidade de texto do slide 5 acima é **proposta de conteúdo**, não diagramação final. Revisar legibilidade para sete slides e manter os dados originais acessíveis via link/QR sem encurtar ressalvas.

## 5. Auditoria dos textos existentes da demo — PDF de sete páginas efetivamente lido

**Fonte real auditada:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf (PDF público com **7 páginas**, texto extraído durante SCI-04).  
**Página de acesso:** https://emds96.github.io/firelens-stack-manauara/demo/ .

| Slide | Texto/alegação examinada | Auditoria / ajuste proposto |
|---|---|---|
| 1 | “Two sensors. Two translators. One clearer picture.” | Adequado como conceito, não se apresenta como previsão nem identidade física |
| 2 | “The same landscape, different observations”; “one detected hotspot pixel is not one confirmed fire” | **Aprovado cientificamente** como formulação prudente |
| 3 | “Compare original MODIS / VIIRS counts”; baseline e limitações | Manter; adicionar lembrete de calendário se slide 5 for substituído |
| 4 | WAPE de 2023/2024, regiões A/B, erros relativos a MODIS | Correto como piloto histórico; **não** extrapolar esses resultados para Amazonas inteiro/2025/2026 |
| 5 | “72 validated monthly records” | **Ajustar** para “72 processed and checked monthly records”, ou substituir pela explicação SCI-04 proposta acima. “Validated” pode ser interpretado como validação física |
| 6 | “NOAA-20 and NOAA-21: live API integration verified”; 145/243 da captura de 14/11 | Manter apenas com **data da captura visível**; não chamar 388 de incêndios ou estatística sempre atual |
| 7 | “Clearer evidence. Clearer decisions”; limitações do método | Manter como visão educativa; acrescentar que **identidade física de um incêndio e correção sensor-a-sensor não foram validadas** e explicitar uso de IA no PDF |

**Limites da auditoria:** conteúdo textual dos sete slides e metadados de contagem de páginas foram acessíveis; **layout, legibilidade em projetor, vídeo e todas as imagens/elementos gráficos do PDF não foram inspecionados visualmente nesta revisão**. A página HTML da demo já credita ChatGPT no rodapé, mas essa informação não estava presente no texto extraído do próprio PDF.

## 6. Auditoria dos textos existentes da submissão — proposta, não formulário vivo

Fontes efetivamente lidas:
- `docs/PACOTE_SUBMISSAO_FIRELENS_2026-11-14.md`
- `docs/SUBMISSAO_RASCUNHO.md`

**Atenção:** estes são documentos de rascunho e histórico operacional. **Não foi conferida a versão atualmente salva no editor da NASA**, e não houve login/edição/submissão nesta missão.

| Campo/fonte | Estado e risco | Correção recomendada **antes de eventual aprovação** |
|---|---|---|
| F02 — Summary | Formulação de detecções de pixel, baseline histórico e limites é cuidadosa; **não contém TEST-02** | Manter o resumo focado **nas funcionalidades implantadas**. TEST-02 é pesquisa separada, não camada operacional do app |
| F03 — Demo (`SUBMISSAO_RASCUNHO.md`) | Diz “NÃO DISPONÍVEL”; **desatualizado** | Atualizar apenas quando autorizado para URL pública de PDF de **7 slides**; link já publicado na seção 3.4 do pacote |
| F05 — Details | Fala em *12 testes* e apenas resultados 2022–2024; é fotografia antiga | Se atualizar métricas, citar evidência datada: **47 testes** no workflow TEST-02, sem sugerir que equivalem a validação física. Separar história da interface de pesquisa posterior |
| F05 — Física | Não afirma identidade física; falta divulgação explícita do SCI-04 | Se houver espaço, incluir parágrafo experimental em inglês abaixo; **não** chamar de função operativa |
| F06 — AI/SI | `PACOTE` diz que TinyFish foi usado para “read-only browser testing”, mas `SUBMISSAO_RASCUNHO.md` registra **preenchimento e salvamento da revisão do formulário via TinyFish** | Descrever também ajuda no rascunho/preenchimento/salvamento, e assistência de IA na elaboração dos slides. Confirmar com a equipe todos os serviços usados e responsabilidade pela revisão |
| F07 — NASA data | Relaciona anuais 2022–24 e NOAA20/21 NRT | Acrescentar **MODIS_NRT (Terra e Aqua) e VIIRS_NOAA20_NRT 10–14/11/2026** como fontes do experimento **TEST-02, não incorporado ao site** |
| F08 — Credits | Listagem abreviada cita ferramentas de programação, mas **não lista Leaflet, markercluster e OpenStreetMap** | Completar bibliotecas e créditos de dados/cartografia e revisar licenças e autoria de qualquer visual da demo |
| F09/F10 — Terms/originality | Documento registra **seleção inadvertida das duas caixas**, tentativa de desmarcar sem salvamento e persistência não verificada | **Pendência operacional crítica**: revisão humana direta na página NASA. Não autorizar/operar submissão nem afirmar estado atual das caixas sem verificação |
| Pacote seção 3.5 | Detalhes e resultados A/B são válidos **para o contexto e anos especificados** | Não atribuir validação SCI-04 à ferramenta implantada, nem associar fumaça ou risco urbano aos pontos de satélite |

### Parágrafo inglês opcional para F05 — pesquisa separada (pronto para revisão)

> **Experimental observation-level research (not part of the live application).** We separately analyzed NASA FIRMS MODIS NRT (Aqua and Terra) and VIIRS NOAA-20 NRT observations in Amazonas from 10–14 November 2026. Using approximate scan/track dimensions, actual acquisition times, brightness-temperature measurements and pixel-level fire radiative power, we identified two candidate MODIS–VIIRS association groups on 10 November. On 11 November, 12 eligible daytime MODIS Aqua detections and 222 eligible daytime NOAA-20 detections were observed, but no group met all four exploratory conditions within 120 minutes. These comparisons are reproducible observational diagnostics, not proof of unique fire identity, hidden fires, atmospheric smoke sources or validated physical harmonization. We have not integrated the experimental associations into the public application's operational views.

### Correção proposta para F06 — uso de IA / automação (confirmar antes do envio)

> Our team used ChatGPT (OpenAI) to assist with code and test drafting, scientific review, documentation, presentation drafting and design, and communication. TinyFish was used for public website testing and assisted with drafting and saving project form entries; this was not the final project submission. Team members remain responsible for checking scientific results, sources, permissions, claims and the final approval and submission. Original satellite observations were obtained from NASA FIRMS rather than generated by AI. We will review the complete list of tools, assets and credits before final submission.

**Nota:** a frase anterior é proposta de declaração, não comprovação de que todos os membros revisaram ou aceitaram os textos. O incidente envolvendo as caixas de aceite permanece pendente de inspeção humana e não deve ser omitido de controle interno.

### Complemento sugerido a F07/F08 — fontes e créditos

> NASA FIRMS Area API provided the provisional MODIS NRT (Aqua and Terra) and VIIRS NOAA-20 NRT observations used in our separate November 2026 observation-level research. This analysis is experimental and not integrated into the deployed app. The public map uses Leaflet, Leaflet.markercluster and OpenStreetMap map data/tiles with appropriate attribution. We also used a provisional third-party IBGE-based Amazonas boundary, whose official precision has not been independently verified.

## 7. Evidência reproduzível, controles e pendências

**Reproduzir sem baixar os CSVs novamente nem expor chave:**
```bash
python -m unittest discover -s tests -v
python -m scripts.test02_verify
```
A verificação offline recompõe observações, atributos de cada linha, ligações por dia/grupo, classificações exclusivas e fatores de comparação a partir dos JSONs imutáveis versionados no repositório. [Workflow de evidência](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662809732): **47 testes**, resultado `offline_recomputed_exactly`. Prova **reprodutibilidade do cálculo**, não validação física independente.

**Pendências para aprovação SCI-04:**
1. Sessão principal aprovar/rejeitar as mensagens propostas do slide, o vocabulário “associação candidata” e a eventual atualização do PDF **antes de qualquer alteração**.
2. Verificar footprints/orientação por produtos geolocalizados Level-2 ou outra representação instrumentada validada; comparar oportunidades de cobertura, passagens e nuvens.
3. Medir falsos pareamentos e sensibilidade a mudanças dos limites de tempo, distância, ΔT11 e razão FRP; não tratar 120min, 8K ou FRP 0,5–2 como universais.
4. Revisar créditos/IA e a versão efetivamente salva na NASA com o responsável humano; verificar termos/originalidade, sem submeter até autorização explícita.
5. Confirmar qualidade visual e legibilidade do PDF revisado em tela pequena, bem como links públicos.

## 8. Registro rastreável de decisão

- **ID:** SCI-04 / TEST-02 — revisão de linguagem e divulgação científica.
- **Decisão/status:** **PROPOSTA — aguardando aprovação da sessão principal**. Nenhuma integração ao frontend, alteração do PDF ou submissão NASA nesta missão.
- **Motivo:** comunicar resultados observacionais verificáveis sem alegar confirmação de incêndio ou harmonização física que o experimento não valida.
- **Alternativas:** apresentar as quatro travas como prova física (rejeitada cientificamente); ignorar o TEST-02 (desperdiça aprendizado); **apresentar um grupo candidato e suas incertezas** (proposta).
- **Evidências:** JSON e CSVs capturados via FIRMS, relatório do TEST-02, verificações offline, texto extraído do PDF de 7 páginas, rascunhos de submissão e descrições oficiais NASA.
- **Restrições/riscos:** contorno estadual simplificado, retângulos de pixel aproximados, sensores/canais distintos, NRT provisório, cobertura não controlada, prazo e versão real do formulário não inspecionada.
- **Validação:** jurado consegue distinguir três níveis (observado, candidato e não provado), números conferem com JSON, slide revisado tem no máximo sete páginas, links públicos e créditos visíveis, nenhum termo ilegal ou alegação física indevida.
- **Responsável:** engenharia Stack Manauara; **data:** 14/11/2026. Aprovação final: sessão principal, **pendente**.
