# MAP-01 — Mapa interativo de detecções térmicas

**Equipe:** Stack Manauara — FireLens · Dois Tradutores. **Data:** 14/11/2026.
**Decisão:** MAP-01 implementada e validada em navegador headless para o fluxo principal; globo 3D não autorizado.

## Arquitetura e decisão

- **Alternativa adotada:** Leaflet 1.9.4 (BSD-2-Clause) com Leaflet.markercluster 1.5.3 (MIT), dados estáticos em data/recente.json, frontend HTML/CSS/JS, GitHub Pages.
- **Motivo:** zoom, movimentação e seleção de marcadores com baixo esforço. O agrupamento reduz sobreposição; se o plugin não carregar, marcadores individuais continuam utilizáveis.
- **Alternativas consideradas:** MapLibre GL JS (dependência maior e tiles vetoriais), mapa SVG/Canvas artesanal (geometria própria), globo 3D (fora do escopo e dependências maiores).
- **Fontes:** https://leafletjs.com/download.html ; https://github.com/Leaflet/Leaflet.markercluster ; https://operations.osmfoundation.org/policies/tiles/
- **Riscos:** dependência de CDN e disponibilidade dos tiles OSM, desempenho em celulares antigos, precisão do contorno do Amazonas e qualidade temporal NRT.
- **Validação:** testes automatizados de coordenadas, filtragem, ausência de dados, estado desatualizado e regressões; teste em navegador do mapa bilíngue no GitHub Pages.

## Implementação

- map-data.js normaliza detecções reais, rejeita coordenadas inválidas, mantém sensor/atributos originais e calcula status e filtragem.
- map-ui.js exibe mapa 2D inicialmente no Amazonas, marcadores reais NOAA-20 (laranja) e NOAA-21 (turquesa), agrupamento, zoom/pan, filtros, lista paginada acessível e dois tradutores bilíngues por ponto.
- index.html, app.js, style.css acrescentam o mapa à aba de Observações Recentes, preservando Tradutor Científico e Calendário Histórico.
- Limites científicos: coordenada representa pixel térmico detectado, não incêndio individual ou extensão queimada. Não há calibração histórica aplicada ao NRT. Regiões A/B são independentes da camada recente.
- last_success_utc e last_observation_utc são exibidos separadamente no horário de Manaus. Consulta há mais de quatro horas implica aviso de desatualização. Fonte indisponível e dados preservados implicam aviso de captura anterior, nunca atual. Ausência de dados não equivale a zero incêndios.
- Recorte do Amazonas usa contorno simplificado de fonte secundária no pré-processamento (docs/GEOMETRIA_AMAZONAS.md). Nenhum polígono de área queimada foi desenhado. Precisão cartográfica junto à fronteira ainda não foi auditada.
- Mapa-base © OpenStreetMap contributors com atribuição; sem pré-carregamento ou download de tiles. Dependência de rede.

## Evidências e pendências

- Tests: tests/test_map.cjs e regressões Python existentes.
- CI: .github/workflows/validate-map.yml
- Site: https://emds96.github.io/firelens-stack-manauara/
- **Testes realizados:** execução https://github.com/Emds96/firelens-stack-manauara/actions/runs/43641760032 (sucesso). Chrome headless em GitHub Actions testou seleção na lista de pontos e ambos tradutores, filtros NOAA-20/NOAA-21/ambos, ida-volta EN/PT-BR com seleção preservada, viewport 390x844 e indisponibilidade simulada do JSON; 5 testes Node e 12 Python passaram.
- **Correção durante QA:** removida a chamada de animação assíncrona markercluster.zoomToShowLayer, que causava exceção JavaScript; seleção agora usa map.setView para centralização. A nova execução não registrou erro JS.
- **Pendente:** conferir o site público após o último deploy, testar manualmente telas adicionais e validar a precisão da geometria estadual simplificada.
- **Responsável:** engenharia Stack Manauara, 14/11/2026.

## Globo 3D

Não iniciar sem autorização da sessão principal. Antes, exigir experiência móvel aprovada, mapa 2D validado e análise de custos/benefícios.
