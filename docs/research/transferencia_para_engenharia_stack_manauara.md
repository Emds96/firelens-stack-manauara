# STACK MANAUARA — TRANSFERÊNCIA DE CONTEXTO PARA ENGENHARIA
**NASA Space Apps Challenge 2026 | 14/11/2026 | Sessão principal: pesquisa e decisões**

## Missão e fase
Desafio oficial: https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/
Objetivo: desenvolver uma aplicação web com calendário histórico de atividade do fogo a partir da harmonização MODIS–VIIRS. A proposta da equipe, **IDEIA-01: Dois Tradutores**, envolve (1) tradução científica/comparabilidade entre sensores e (2) comunicação dos achados, limites e incertezas para usuários não especialistas. O calendário é a interface histórica, não o principal diferencial científico. **Fase atual:** validação exploratória executada; pronto para propor *entrada condicionada* em engenharia, sujeita à aprovação humana e delimitação rigorosa das alegações.

## Evidência científica realmente produzida
FIRMS, CSV anuais de Brasil de 2022–2024; recortes espaciais A (-65,-9,-58,-2) e B (-58,-9,-51,-2), coordenadas [lon oeste, lat sul, lon leste, lat norte], não coincidem com limites do estado Amazonas. MODIS Aqua, `confidence>=30`, tipo vegetação `type=0`; VIIRS S-NPP ou NOAA-20 (`viirs-jpss1`), `confidence in {n,h}`, tipo 0. Observações diurnas e noturnas separadas, dados agregados por célula de 1° × 1° e mês. O alvo das previsões é **contagem observada pelo MODIS**, não verdade física ou incêndios individuais.

**Resultados NOAA-20 diurnos, WAPE em período de teste (menor é melhor):**
| Recorte | Treino | Teste | Global | Sazonal regularizado |
|---|---|---|---:|---:|
| A | 2022 | 2023 | 22,16% | 22,72% |
| A | 2022–2023 | 2024 | 20,00% | 20,42% |
| B | 2022 | 2023 | 20,85% | 21,23% |
| B | 2022–2023 | 2024 | 20,15% | 19,31% |

**Resultado anterior S-NPP diurno, recorte A:** treino 2022–23/teste 2024, fator global 25,61% WAPE, fator mensal 24,04%; treino 2022/teste 2023, global 27,36%, mensal 39,85%. O modelo mensal não apresentou superioridade consistente.
**NOAA-20 noturno:** global WAPE A2023 39,47%, A2024 23,47%, B2023 34,27%, B2024 24,16%. Não misturar dia e noite no MVP.

**Insights:** fatores globais são uma linha de base mais simples e robusta nestes testes; modelos sazonais mais complexos não melhoraram de forma consistente. Apresentar tanto o valor nativo VIIRS quanto a estimativa na escala MODIS, e divergências entre tendências. O teste não mostrou validação de uma série completa 2000–2026 nem equivalência física.

## Informações e fontes públicas verificadas
- Enunciado: https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/
- NASA FIRMS: https://www.earthdata.nasa.gov/data/tools/firms
- FAQ FIRMS: https://www.earthdata.nasa.gov/data/tools/firms/faq
- Atributos e diferenças NRT vs Standard: https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs
- Manifesto de arquivos: https://firms.modaps.eosdis.nasa.gov/data/country/yearly_summary_files.txt
- NASA informa fim de novas observações Suomi-NPP em 02/11/2026; NOAA-20/NOAA-21 são fontes de continuidade.
- NRT não apresenta necessariamente `type`; não assumir `type=0` quando ausente.
- Arquivos anuais consolidados de NOAA-21 para Brasil 2022–24 não foram localizados no padrão tentado (`viirs-jpss2_...` retorna 404); **a disponibilidade de NOAA-21 NRT é questão distinta e não foi testada**.
- CSVs de pontos ativos não têm denominador de observações em céu claro: não corrigir nuvens sem fonte adicional.
- `frp` representa **potência radiativa** (MW), não energia em MWh, nem área queimada.

## Pendências, limitações e riscos
1. NOAA-20 testado somente em dados históricos consolidados até 2024, não no NRT de novembro de 2026. Fluxo operacional e atualização ao vivo não testados.
2. Validações temporais em apenas dois holdouts e dois recortes; generalização nacional NÃO demonstrada.
3. Sem validação de tendência secular 2000–2026, MODIS Terra, máscaras de nuvens ou MapBiomas/área queimada.
4. Zero detecção pode significar fogo não observado; um registro ativo não é um incêndio.
5. A normalização de horário solar local no experimento descarta observações que atravessam o ano UTC. Para um calendário histórico rigoroso é preciso ler também os CSVs UTC adjacentes ou permanecer em UTC e informar isso; não produzir calendário completo com meses de borda silenciosamente incompletos.
6. Modelo Quasi-Poisson/intervalos de incerteza do Gemini não foi validado com dados reais e apresentou rotulagem equivocada de percentis: intervalo central de 90% é aproximadamente P05–P95, não P10–P90. Não usar IC numérico como calibrado sem testar cobertura fora da amostra.
7. Falta testar Tradutor 2 com usuários e garantir que ele não extrapole o que as medições suportam.

## Registros de decisão
**IDEIA-01 | proposta principal, aprovação definitiva pendente.** Motivo: dois tradutores + calendário com explicação auditável e contribuição metodológica demonstrável; alternativa rejeitada como núcleo: calendário simples sem correção. Evidência: arquivo de experimentos e números acima. Risco: interpretação errada de detecções e generalização espacial. Validação: testes fora da amostra e rotulagem clara. Responsável: Stack Manauara. Data: 14/11/2026.
**VAL-TRAD-02 | parecer: ENTRADA CONDICIONADA NA ENGENHARIA, aprovação humana pendente.** Motivo: baseline global diurno com NOAA-20 apresentou desempenho verificável de WAPE 20,00%–22,16% na região A em dois testes; complexidade sazonal não se justificou consistentemente. Alternativas: bruto, fator global, fator mensal, regularizado. Riscos: não é harmonização física completa, NRT não testado. Critério de validação antes de alegação final: desempenho holdout superior a VIIRS bruto; manter fontes, filtros, ausência de nuvens e divergências; sucesso da demonstração com arquivos congelados. Responsável: sessão principal. Data: 14/11/2026.
**ARQ-01 | pendente da engenharia e aprovação da equipe.** Nenhuma stack/arquitetura foi previamente aprovada.

## Missão da engenharia (primeiro passo)
Comparar 2–3 alternativas de implementação com custo, riscos, tempo, operação offline e manutenção; submeter recomendação à sessão principal antes da escolha definitiva. No MVP, priorizar **região-piloto fixa**, dados históricos verificados (não prometer tempo real), comparador de contagens originais MODIS/VIIRS e baseline global diurno, calendário histórico e explicações rastreáveis com linguagem simples. Mostrar diferenças de tendência e condições de observação. Se tempo permitir, investigar NOAA-20 NRT, anos anteriores e expansão regional depois, sempre com testes.

## Critérios de aceitação da próxima missão
Demonstração funcional reproduzível em dados reais e congelados, sem credenciais expostas; visualização do calendário e das duas séries; pelo menos uma comparação que evidencie divergência/limitação; testes unitários de datas, filtros e métricas; comparação objetiva entre alternativas arquiteturais; README com origem/ano/filtros/limitações; submissão exige revisão humana. Não apresentar modelo como operacional/validado em toda a Amazônia. Preparar documentação e material de prova para portfólio e jurados.

## Artefatos nesta transferência
- `validacao_noaa20_2026.json`: números da execução com NOAA-20 nas regiões A/B, dias/noites e dois holdouts.
- `validacao_tradutor1_reproduzivel.py`: script Python reproduzível, sem bibliotecas externas; dependência de internet para buscar FIRMS ou de CSVs armazenados em cache.
- `auditoria_cientifica_tradutor1_stack_manauara.md`: parecer do Gemini, com erros a não assumir como validados.
- `experimento_tradutor1_auditado.py`: código Gemini, não promover automaticamente para produção.
- `resultados_experimento_tradutor1.json`: métricas originais de S-NPP.
