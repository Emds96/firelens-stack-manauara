# FireLens — Dois Tradutores | Stack Manauara

NASA Space Apps Challenge 2026 · **Harmonization of MODIS and VIIRS Hot Spots**.

**Status atual:** código e dados no GitHub e **GitHub Pages publicado e testado** em https://emds96.github.io/firelens-stack-manauara/. **NASA NRT NOAA-20/NOAA-21 comprovado em 14/11/2026 nas execuções #2 e #3**. **Calendário 2022–2024 publicado com 72 registros mensais e quatro métricas WAPE reproduzidas** no workflow histórico. Execução automática por cron ainda não foi observada.

## Limites do recorte geográfico

O arquivo versionado `data/amazonas_ibge.geojson` é **uma geometria estadual simplificada de fonte secundária baseada em IBGE**, e não uma verificação direta de malha oficial atualizada. Veja `docs/GEOMETRIA_AMAZONAS.md`. O contorno pode produzir erros junto às fronteiras.

## Languages and public project demo (ENG-04)

- **English is the default** for judging, with a prominent **EN / PT-BR** toggle. Selection is remembered in the browser and shareable via `?lang=en` or `?lang=pt-BR`.
- Interface translations include scientific caveats, live-data status, time/date formatting, WAPE labels, and calendar month detail.
- **English seven-slide presentation:** https://emds96.github.io/firelens-stack-manauara/demo/FireLens_7_Slide_Demo_2026.pdf
- **Presentation landing page:** https://emds96.github.io/firelens-stack-manauara/demo/
- The demo was prepared with AI assistance; the team remains responsible for its accuracy and final approval.

## Rodar localmente

Requisitos: **Python 3.11+**, sem dependências externas.

```bash
cd firelens-stack-manauara
python -m http.server 8000
```

Acesse `http://localhost:8000/`. Abrir `index.html` diretamente por `file://` pode bloquear a leitura dos arquivos JSON.

### Testar a engenharia

```bash
python -m unittest discover -s tests -v
```

### Dados recentes NOAA-20 e NOAA-21

A [Area API NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/api/area/) usa fonte `VIIRS_NOAA20_NRT` / `VIIRS_NOAA21_NRT`, `MAP_KEY` e bbox oeste,sul,leste,norte. A [MAP_KEY gratuita](https://firms.modaps.eosdis.nasa.gov/api/map_key/) é enviada ao email cadastrado.

**Segurança:** configure a variável de ambiente `FIRMS_MAP_KEY` localmente ou o segredo GitHub Actions `FIRMS_MAP_KEY`. **Não cole a chave em conversa, frontend ou commits.**

```bash
# Linux/macOS, em ambiente local autorizado:
read -s FIRMS_MAP_KEY && export FIRMS_MAP_KEY
python scripts/firms_nrt.py
```

No Windows PowerShell, forneça a variável via mecanismo seguro de segredo/ambiente disponível; não registre a chave em scripts versionados.

O script usa a geometria versionada (simplificada, compilada a partir de dados IBGE); se o arquivo local não existir, tenta baixar a malha oficial do IBGE; usa a geometria para recortar os pixels no estado do Amazonas (a API só filtra por caixa envolvente). Consulta os dois sensores para os dois dias mais recentes, aplica confiança `n/h`, preserva dia/noite, registra hora UTC da observação e da consulta e grava `data/recente.json`. A interface exibe em Manaus (UTC−4). Não há aplicação do fator histórico a NOAA-21 ou ao NRT.

Se um sensor falhar, **todo o lote é marcado indisponível** e a última captura bem-sucedida é preservada com aviso; não se inventa um zero de ocorrências. A atualização agendada do GitHub Actions é proposta para `:23` de cada hora; horários reais podem variar. A execução manual #1 falhou por indisponibilidade na obtenção da malha; a execução automática por push #2 comprovou a API e o JSON, mas **o agendamento horário por cron ainda precisa ser observado**.

### Dados históricos e calendário

Os experimentos independentes disponíveis estão em `data/validacao.json` e `docs/research/` (artefatos fornecidos pela pesquisa).

**Séries já geradas e verificadas no GitHub em 14/11/2026** por [workflow histórico](https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632602795). Para reproduzir localmente, obtenha os 6 CSVs anuais do Brasil de 2022–24 da [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/data/country/) e armazene em `firms_cache/` com os nomes exatos utilizados pelo script científico original. Depois:

```bash
python -m scripts.build_historical --cache firms_cache
```

Esse exportador usa os **mesmos filtros, células e método** do arquivo científico original e compara os 4 resultados de WAPE (global diurno) com `data/validacao.json`, abortando se divergirem. O arquivo `data/historico.json` encontra-se `ready` após conferência dos quatro WAPEs globais diurnos; a interface pode apresentar os 72 registros mensais sem dados fabricados.

**Limite:** por usar arquivos por ano UTC sem os dados de 2025, dezembro do calendário solar local pode estar incompleto. Ele é identificado como incompleto, e a versão não alega série 2000–2026 nem limites oficiais do Amazonas para as regiões de validação A/B.

## Organização do repositório

- `index.html`, `style.css`, `app.js`: frontend estático, dois tradutores, camada NRT e calendário.
- `scripts/firms_nrt.py`: API NASA + geometria IBGE + estado de falha e fallback.
- `scripts/build_historical.py`: gerador de séries históricas, validado contra WAPE original.
- `data/recente.json`: somente resultados NRT verdadeiros ou estado indisponível.
- `data/historico.json`: 72 séries mensais de A/B × 2022–2024, geradas com validação WAPE comprovada.
- `data/validacao.json`: resultados experimentais fornecidos pela pesquisa.
- `.github/workflows/atualizar-firms.yml`: rotina NRT horária e publicação de JSON (cron ainda não observado).
- `.github/workflows/construir-historico.yml`: workflow de extração 2022–2024, com WAPE reproduzido e JSON histórico publicado.
- `tests/`: testes sintéticos para lógica, não testes de integração NASA.
- `ESTADO_PROJETO.md`: transferência e status para submissão.

## Fontes e limites científicos

- [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms)
- [NASA FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- [NASA FIRMS atributos de dados](https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs)
- [IBGE Malhas](https://servicodados.ibge.gov.br/api/docs/malhas?versao=3)

Contagens são **detecções de pixels de anomalia térmica**, não incêndios confirmados, área queimada ou concentração de poluentes. O modelo histórico ajusta escala de contagens de NOAA-20 para MODIS Aqua; não corrige nuvens nem garante comparabilidade física. Não é um produto oficial da NASA nem tem seu endosso.

## Publicação (repositório já criado)

1. Repositório público confirmado: https://github.com/Emds96/firelens-stack-manauara — **código publicado e verificado no GitHub**.
2. Código, testes, documentação e workflow já enviados; confira o commit do protótipo `943d897beec55d9d6b6d1d379ddafd3fce5beeae`.
3. Segredo `FIRMS_MAP_KEY` já configurado e verificado pela execução #2; não expor o valor.
4. Execução #2 comprovada: https://github.com/Emds96/firelens-stack-manauara/actions/runs/43632228781 ; NOAA-20=145, NOAA-21=243 detecções elegíveis em janela de 2 dias, 388 no total (contagens de pixels, não incêndios).
5. **GitHub Pages publicado e testado** em https://emds96.github.io/firelens-stack-manauara/ ; ver registro ENG-03 em `ESTADO_PROJETO.md`.
6. Se o Actions não conseguir enviar commits, verificar Settings → Actions → General → Workflow permissions: Read and write.

Para a sessão de submissão: usar somente URLs realmente criadas e verificadas; não copiar endereços hipotéticos.

## Uso de IA

O ChatGPT auxiliou na revisão de arquitetura e na criação inicial do código, testes e interface. Os testes locais não constituem validação de dados NRT. Registrar também outras ferramentas usadas de fato antes da submissão.