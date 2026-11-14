# Geometria da área-piloto — Amazonas (ENG-02)

**Data:** 14/11/2026. **Status:** fonte secundária simplificada, provisória, não validada contra arquivo oficial recente.

O arquivo `data/amazonas_ibge.geojson` contém uma única feição do estado Amazonas (código IBGE 13), extraída de um GeoJSON público de limites estaduais pré-compilados: https://github.com/henriquemalvar/br-geojson/blob/main/dist/estados.geojson . O mantenedor informa origem em dados do IBGE, mas **esta sessão não verificou a versão original nem a precisão das coordenadas no serviço oficial IBGE**.

**Por que está versionado?** A execução do GitHub Actions #1 em 14/11/2026 falhou com `URLError` antes de consultar os sensores, ao tentar baixar a geometria em tempo de execução. Para remover essa dependência de rede, o processamento passa a ler a geometria local. A API NASA FIRMS continua sendo necessária para obter NRT.

**Limite:** o contorno tem 323 posições geográficas e está simplificado; pode incluir ou excluir detecções próximas às fronteiras administrativas. Não afirmar que este recorte tem precisão cartográfica oficial. Para demonstração e validação final, comparar a malha com um arquivo oficial IBGE versionado, documentar diferenças em ocorrências elegíveis e substituir somente mediante verificação.

**Validação:** arquivo tem propriedades `cd_geocuf=13`, `sigla=AM`, geometria Polygon e limites plausíveis (lon -73,7981 a -56,0954; lat -9,8180 a 2,2185). Verificação independente de posição conhecida em Manaus e ponto externo será executada pelo conjunto de testes. A consulta real NOAA-20/21 deve ser comprovada por execução posterior.

**Registro de decisão ENG-02 — Proposta operacional aplicada.** Motivo: eliminar falha de rede com malha em tempo de execução. Alternativa: continuar fazendo download IBGE em cada atualização (instável no teste); geometria compilada baseada em IBGE versionada (adotada provisoriamente). Evidência: logs Actions #1 e URL fonte. Risco: limites simplificados sem auditoria de exatidão; mitigação com transparência e comparação futura. Responsável: engenharia Stack Manauara; aprovação da utilização como limite científico definitivo: pendente da sessão principal.
