# HIST-02 — Calendário estadual do Amazonas e experimento A/B separado

**Projeto:** FireLens — Stack Manauara · **Data de trabalho:** 14/11/2026 (Manaus)  
**Decisão:** HIST-02 aprovada pelo fundador; implementação de visualização, **sem alterar a ciência**, a interface de submissão ou os arquivos de dados originais.

## Escopo implementado

A aba **Histórico** abre por padrão o calendário estadual derivado **diretamente de** `data/sci03_agregados.json`, usando seus 4.434 registros por célula geográfica de **1° × mês UTC**, para 2023–2026. Somente os meses **janeiro–outubro** fazem parte deste arquivo. O usuário escolhe **MODIS Aqua** ou **VIIRS NOAA-20**; não existe fator de correção aplicado aos totais nem fusão de sensores.

Os registros SCI-03 têm colunas `year,month,sensor,cell_south_lat,cell_west_lon,pixels`. `history-state.js` valida estritamente os campos, rejeita duplicatas e agrega os pixels por **ano, mês e sensor**. A tela mostra o número original de pixels com detecção, a classificação da fonte e mais detalhes ao selecionar o mês. Se um mês não estiver representado, sua célula apresenta **“— / indisponível”**, sem exibir zero; a interface não afirma ausência de fogo.

A opção **Regiões-piloto A/B · 2022–2024** abre o calendário existente em `data/historico.json`, preservando o algoritmo e a seleção A/B da implementação anterior, em uma área separada. A série do Amazonas não reutiliza contagens, filtros, recortes ou coeficientes desses pilotos.

## Evidências quantitativas: soma reprodutível dos pixels dos dez meses (sem correção)

| Ano | MODIS Aqua | VIIRS NOAA-20 | Origem |
|---|---:|---:|---|
| 2023 | 17.468 | 70.276 | Arquivos anuais NASA FIRMS Brasil |
| 2024 | 22.300 | 87.776 | Arquivos anuais NASA FIRMS Brasil |
| 2025 | 3.941 | 19.017 | Arquivos anuais NASA FIRMS Brasil |
| 2026 | 8.002 | 42.636 | FIRMS Area API; SP/NRT conforme mês e sensor |

Números verificados pela soma dos campos `pixels` de `data/sci03_agregados.json`, sem afirmar incêndios únicos, área queimada, cobertura observacional uniforme ou confiabilidade de comparar as magnitudes de sensores distintos. A precisão do contorno estadual simplificado continua pendente de avaliação contra o IBGE oficial.

**Exemplo auditável — setembro/2026:** MODIS Aqua **3.518** pixels e NOAA-20 **16.489** pixels; cada sensor aparece isoladamente na visualização, ambos rotulados NRT. Novembro e dezembro são **indisponíveis neste conjunto 2023–2026**. Há arquivos FIRMS de outros escopos para alguns desses meses; a ausência aqui **não** significa ausência de observação em toda a NASA.

## Processamento por período (proveniência SCI-03)

| Período | MODIS Aqua | VIIRS NOAA-20 | Observação |
|---|---|---|---|
| 2023–2025, janeiro–outubro | Arquivo anual Brasil | Arquivo anual Brasil | Não atribuir automaticamente a etiqueta SP a um arquivo anual |
| 2026, janeiro–julho | SP | SP | Produtos processados em nível padrão |
| 2026, agosto | SP | NRT | Fontes diferentes no mesmo mês |
| 2026, setembro–outubro | NRT | NRT | Dados provisórios, sujeitos a revisão |
| Novembro–dezembro (2023–2026) | Indisponível nesta série | Indisponível nesta série | Não inferir contagem igual a zero |

A classificação de processamento foi documentada no **SCI-03** ([relatório de pesquisa](SCI-03_HARMONIZACAO_PADROES.md), [proveniência detalhada](../data/sci03_resultados.json)). Os dados de 2026 NRT diferem do SP em atributos disponíveis, como a ausência observada do campo `type` em consultas NRT: isso limita comparações quantitativas. Janeiro–outubro são meses UTC completos da janela analisada em SCI-03; **2026 permanece uma série anual parcial**. O calendário não é previsão, taxa de risco nem ferramenta operacional de incêndios.

## Execução de testes e publicação — evidência real

- **GitHub Actions (sucesso):** https://github.com/Emds96/firelens-stack-manauara/actions/runs/43671123377 — **14 testes Node aprovados, 47 testes Python aprovados** e aceitação em navegador Chromium sem erros. O teste de navegador verificou 40 meses disponíveis para o satélite selecionado, oito meses indisponíveis (novembro/dezembro dos quatro anos), totais de agosto e setembro de 2026, rótulos SP/NRT, 2026 parcial, EN/PT-BR, modo piloto A/B e o retorno ao modo estadual.
- **Regressões preservadas:** o mesmo workflow verificou o mapa NOAA-20/NOAA-21, camada separada Visão da Águia, filtros, idiomas, carregamento, detalhes técnicos, histórico A/B e layout móvel 390×844.
- **Alcance do teste:** reproduz lógica e navegação com dados SCI-03 reais versionados, mas não certifica contorno estadual IBGE, completude instrumental das passagens, precisão física de incêndios nem equivalência SP/NRT.

## Arquitetura, testes e decisões

**Arquivos de interface:** `index.html`, `style.css`; novos `history-state.js`, `history-ui.js`. O módulo legado de calendário em `app.js` e os dados do calendário A/B foram preservados; novos componentes independentes escutam o evento de troca de idioma existente.

**Testes:** `tests/test_history_state.cjs` valida os oito totais por sensor/ano, 40 meses disponíveis por sensor, valores reais de agosto/setembro, faltas, duplicações e integridade da fonte. `tests/test_map_browser.cjs` verifica a visualização padrão, sensor Aqua/NOAA20, SP/NRT agosto e setembro, EN/PT-BR, indisponibilidade de novembro/dezembro e acesso à opção A/B; mantém também testes anteriores de mapa, Eagle case, métodos e celular. Workflow `.github/workflows/validate-map.yml` executa testes Node, Python e Puppeteer.

**Reproduzir:**
```bash
node --test tests/test_history_state.cjs tests/test_map.cjs tests/test_case.cjs
python -m unittest discover -s tests -v
# O workflow GitHub inclui ainda navegador Chromium com servidor estático.
```

**Registro de decisão HIST-02 — status:** aprovada pelo fundador; implementada como **visualização de dados SCI-03**, não nova validação de harmonização. **Motivo:** ampliar o histórico visível para Amazonas e manter o piloto A/B isolado. **Alternativas:** substituir o piloto ou fundir contagens estaduais e piloto (rejeitadas). **Evidência:** SCI-03, JSON original, somatórios e testes de UI. **Riscos:** diferenças SP/NRT, geografia simplificada, indisponibilidades, ausência de denominador de oportunidade de observação. **Validação:** totais idênticos aos originais, grupos separados, idioma e responsividade, testes e deploy. **Responsável/data:** engenharia Stack Manauara, 14/11/2026; revisão científica final humana pendente.

**Submissão NASA:** nenhum aceite modificado e nenhum Submit for Judging realizado. O arquivo original SCI-03 e os artefatos TEST-01/01B/SCI-03/TEST-02 não foram editados nesta missão.
