# FIN-01 + UX-03 — Entrega de engenharia do FireLens

**Equipe:** Stack Manauara  
**Projeto:** FireLens — Dois Tradutores  
**Data:** 14/11/2026 (Manaus, UTC−4)  
**Status:** escopo funcional aprovado pelo fundador e **implementado/testado**. Aprovação humana do conteúdo final da submissão NASA permanece pendente. **Não submetido.**

## 1. Resultado publicável

**Aplicação:** https://emds96.github.io/firelens-stack-manauara/  
**Idioma inglês:** https://emds96.github.io/firelens-stack-manauara/?lang=en  
**Idioma português:** https://emds96.github.io/firelens-stack-manauara/?lang=pt-BR  
**Demo pública de sete slides:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf

A experiência passou a ter três áreas: **Mapa → Histórico → Entenda os dados**, com cabeçalho compacto e prioridade ao mapa em computadores e celulares.

- **Mapa:** pontos geográficos reais de NOAA-20/NOAA-21 da camada NRT existente, filtros e agrupamento. Ao selecionar um ponto, aparece **uma explicação simples**; atributos de sensor, data, coordenadas, confiança e turno estão em uma seção expansível. Estatísticas agregadas também permanecem acessíveis em `details`, fora da leitura principal.
- **Visão da Águia:** botão específico substitui temporariamente os pontos NRT por **um caso histórico distinto e datado de 10/11/2026**. Três marcadores NASA FIRMS reais: Aqua M-000047 e NOAA-20 V-000192/V-000193; botão retorna à camada recente, preservando o uso normal do mapa. O caso histórico não é apresentado como atualização ao vivo.
- **Histórico:** calendário de **72 registros mensais de 2022–2024**, apenas regiões-piloto **A/B**, com seleção de mês, valores de ambos sensores e explicitação de dezembro possivelmente incompleto. Não é um calendário estadual/municipal completo.
- **Entenda os dados:** interpretação unificada, distinção entre contagens estatísticas e medições físicas, WAPE separado no Amazonas de **23,11% (2024)** para **50,73% (2025)**, métodos e referências técnicas expansíveis.
- **Idiomas:** EN/PT-BR preservados, incluindo caso, filtros, referências e dados científicos.

## 2. Caso real exibido (TEST-02) — verificação científica

Fonte isolada: `data/caso_visao_aguia_20261110.json`, gerada exclusivamente dos dados existentes `data/test02_observacoes_20261110_14.json` e `data/test02_resultados.json`. Registros originais e identificadores foram preservados.

| Medição | MODIS Aqua M-000047 | VIIRS NOAA-20 V-000192 | VIIRS NOAA-20 V-000193 |
|---|---:|---:|---:|
| UTC | 19:49 | 18:02 | 18:02 |
| Hora de Manaus (UTC−4) | 15:49 | 14:02 | 14:02 |
| Latitude | -3.44421 | -3.44233 | -3.44225 |
| Longitude | -59.61359 | -59.61069 | -59.60994 |
| scan × track (km) | 1.00 × 1.00 | 0.57 × 0.52 | 0.57 × 0.52 |
| Temperatura de brilho T4 (K) | 326.32 | 332.16 | 332.46 |
| Temperatura de brilho T31/TI5 (K) | 297.36 | 294.24 | 293.72 |
| FRP (MW) | 18.62 | 6.86 | 6.23 |

**Diferença temporal real:** 107 minutos. **FRP MODIS:** 18,62 MW; **soma FRP VIIRS:** 13,09 MW; **diferença:** 5,53 MW; **razão:** 0,703.

A geometria `scan × track` é **aproximada**, não o footprint orbital georreferenciado. T31/TI5 provêm de **canais distintos** e não equivalem automaticamente à temperatura de fundo da paisagem. FRP é **potência radiativa**, não energia conservada entre passagens. Proximidade espacial/temporal e semelhanças de medição não demonstram identidade de um único incêndio.

No mesmo TEST-02, **dois grupos candidatos** foram encontrados em 10/11. Em **11/11**, houve **12 Aqua** e **222 NOAA-20** diurnos elegíveis no Amazonas simplificado, mas **nenhum grupo satisfez todas as quatro condições exploratórias** em até 120 minutos. Nenhuma observação é uma previsão, área queimada, classificação de sub-bosque ou fonte de fumaça confirmada.

## 3. Arquivos alterados / criados

**Código/UI:** `index.html`, `app.js`, `map-ui.js`, `style.css`; módulo anterior `map-data.js` preservado.

**Dados novos (não operacionais):** `data/caso_visao_aguia_20261110.json`. Arquivos `data/test02_resultados.json`, `data/test02_observacoes_20261110_14.json`, `data/historico.json`, `data/test01b_resultados.json` e `data/sci03_resultados.json` **não foram modificados por FIN-01**.

**Testes:** `tests/test_map_browser.cjs` atualizado; `tests/test_case.cjs` criado, com comparação célula a célula contra registros NASA originais e checagem dos resultados TEST-02.

**Demonstração:** `scripts/capture_demo_map.cjs`, `scripts/build_final_demo.py`, `.github/workflows/build-final-demo.yml`, `demo/FireLens_7_Slide_Demo_2026.pdf` refeito a partir de screenshots reais do aplicativo. PDF **exatamente sete páginas**, em inglês, incluindo créditos da assistência ChatGPT.

**Documentação:** `README.md`, `docs/SUBMISSAO_RASCUNHO.md`, `docs/PACOTE_SUBMISSAO_FIRELENS_2026-11-14.md`, este relatório e `ESTADO_PROJETO.md`.

## 4. Evidências de validação

- **Mapa/desktop/celular, idiomas, case switch, retorno ao NRT, filtros, calendário, métodos e falha de API:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669321931 — **47 testes Python + 9 testes Node** (5 MAP-01 anteriores, 4 de proveniência do caso) e testes completos em Chrome 1280×900 e 390×844, sem exceções JavaScript.
- **Geração da demonstração:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669280189 — screenshots reais do mapa, da Visão da Águia e do calendário, PDF gerado/verificado em **sete páginas** e publicação via commit após sincronização da branch.
- **TEST-02 original reprodutível:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43662809732 — 47 testes Python e recálculo offline exato a partir das observações NASA arquivadas. Testes não constituem confirmação física.
- **Agendamento NRT observado:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669211275 — evento **schedule**, concluído com sucesso em 15/11/2026 02:44 UTC (14/11 22:44 AMT); consultou NOAA-20/NOAA-21 e publicou `data/recente.json` com `last_success_utc=2026-11-15T02:45:02Z`, `status=ok`, `count=172`. Isto demonstra pelo menos uma execução agendada, não disponibilidade garantida futura.

### Validação complementar na URL pública (sem login)

- **Execução externa de navegador:** https://agent.tinyfish.ai/runs/d45055e0-2b2d-4294-b2b9-c63e24650894 — concluída sem erros reportados. Página pública EN/PT-BR, mapa recente com 172 pontos do snapshot de 14/11 às 22:45 AMT (NOAA-20: 48; NOAA-21: 124), separação entre última consulta e observação, filtros por sensor, calendário A/B, seção “Entenda os dados” com WAPE 2025 de 50,73% e PDF público de 7 páginas foram conferidos.
- **Precisão sobre o alcance:** essa execução externa confirmou o botão Visão da Águia e a descrição do caso na demo, **mas não documentou uma interação direta completa com os três marcadores na camada histórica pública**. Esse caminho foi testado diretamente e sem erros no Chromium de CI https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669321931. Não confundir um teste com o outro.
- **Publicação comprovada:** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43669617287 — GitHub Pages deploy `completed/success` do mesmo commit `d0f48ff6f5fcc3826521c6fe1539ac73dc524706` que estava na branch `main` durante esta conferência.

## 5. Riscos e pendências — sem omissões

1. **Revisão final humana** da interface e dos sete slides, títulos, números, créditos e licenças. Revisão técnica e execução automática foram realizadas; não equivalem a aprovação científica ou jurídica final.
2. **Geometria:** contorno estadual simplificado derivado de fonte secundária, ainda não comparado de modo completo à malha oficial do IBGE.
3. **Física:** sem geolocalização dos footprints Level-2, máscaras de nuvens/opportunidades de observação, taxa de falsos pareamentos ou validação externa da identidade dos incêndios; sem previsão de fogo ou atribuição de fumaça.
4. **NRT:** dados provisórios, atualizações dependentes de acesso NASA/GitHub e rede; uma captura antiga deve continuar identificada como antiga.
5. **Submissão NASA:** nenhum clique em **Submit for Judging**, nenhuma alteração nesta missão nas caixas de aceite. Em `docs/SUBMISSAO_RASCUNHO.md` existe registro de um incidente anterior de aceite com persistência não verificada, exigindo inspeção direta pelo responsável. Campos efetivamente salvos e direitos de imagens/bibliotecas devem ser conferidos.
6. **Cobertura complementar:** o acesso público sem login e a leitura do conteúdo foram conferidos com TinyFish após deploy; permanece desejável revisão manual em mais dispositivos reais, inclusive legibilidade visual dos sete slides e atalhos do teclado.

## 6. Registro de decisões e aceitação

**FIN-01 — APROVADA pelo fundador, EXECUTADA pela engenharia, 14/11/2026.** Motivo: incorporar caso real sem extrapolar inferência científica e preservar calendário, mapa e metodologia. Alternativa rejeitada: reconstrução integral e aplicação da harmonização física como verdade operacional. Validação: fonte do caso conferida contra NASA, CI e demo.

**UX-03 — APROVADA pelo fundador, EXECUTADA pela engenharia, 14/11/2026.** Motivo: reduzir ruído visual e comunicar interpretação antes dos detalhes. Alternativas: manter painéis estatísticos e dois tradutores separados (rejeitada); abandonar dados técnicos (rejeitada); solução aprovada: leitura unificada e expansão opcional. Validação: fluxo em Chromium desktop/mobile e idiomas.

**Decisão científica pendente:** aprovação humana final da redação pública e da demonstração, **não** uma afirmação de harmonização física validada. A NASA não aprovou nem endossou o FireLens.
