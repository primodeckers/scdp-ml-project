# Dicionário de Dados v3 – Sistema de Concessão de Diárias e Passagens

**Data de Criação do Documento:** 01/11/2017  
**Data da Última Atualização do Documento:** 18/09/2019  

---

## 1. Recurso: Bilhetes aéreos na Compra Direta

### 1.1. Início da Publicação dos Dados
01/11/2017, com dados referentes ao mês de outubro de 2017.

### 1.2. Periodicidade de Publicação dos Dados
Mensal. Divulgação, em geral, no primeiro dia útil do mês subsequente.

### 1.3. Escopo
Extração de dados de bilhetes emitidos pela compra direta em viagens públicas (não sigilosas ou sigilosas já publicadas) e que tiveram ocorrência de emissão, remarcação, cancelamento ou no show no período da extração.

### 1.4. Descrição das colunas e dados

| Nome da Coluna | Descrição |
|----------------|-----------|
| **Código do órgão superior** | Código do órgão superior, no Sistema de Informações Organizacionais do Governo Federal (SIORG). |
| **Nome do órgão superior** | Nome do órgão superior, conforme consta no SIORG. |
| **Código do órgão solicitante da viagem** | Código, no Sistema de Informações Organizacionais do Governo Federal (SIORG), do órgão solicitante da viagem. |
| **Nome do órgão solicitante da viagem** | Nome do órgão solicitante da viagem, conforme consta no SIORG. |
| **N. PCDP** | Proposta de Concessão de Diárias e Passagem (PCDP) cadastrada no SCDP, onde constam os dados do servidor, as informações do deslocamento, os documentos comprobatórios da demanda e os dados financeiros. |
| **N. Reserva/Localizador** | Código alfanumérico pelo qual se identifica a reserva da passagem junto à companhia aérea. |
| **Data Emissão Bilhete** | Data em que foi registrada no SCDP a emissão do bilhete junto à companhia aérea. |
| **Data Embarque** | Data de embarque do passageiro para a viagem a serviço. |
| **Valor Tarifa Comercial** | Valor monetário da tarifa do serviço de transporte aéreo praticada pela companhia aérea para o público em geral. |
| **Percentual Desconto Aplicado** | Percentual do desconto aplicado para o Governo Federal, conforme parâmetros acordados com as companhias aéreas credenciadas para a Compra Direta. |
| **Valor Tarifa Governo** | Valor monetário da tarifa do serviço de transporte aéreo, aplicado o desconto do Governo Federal, conforme parâmetros acordados com as companhias aéreas credenciadas para a Compra Direta. |
| **Valor Tarifa Embarque** | Valor monetário da tarifa cobrada pelo uso das instalações aeroportuárias. |
| **Valor Bilhete** | Valor monetário final do bilhete aéreo. Corresponde à soma do Valor Tarifa Governo e do Valor Tarifa Embarque. |
| **Companhia Aérea** | Nome da empresa prestadora do serviço de transporte aéreo de passageiros. |
| **Classe Tarifária Bilhete** | Influencia o valor da tarifa e as regras quanto a franquia de bagagem despachada, multas de remarcação, reembolso e no show do bilhete de passagem aérea, entre outros. |
| **Regra Tarifária** | Condições aplicadas à base tarifária do Bilhete, onde estão dispostos todos os benefícios e penalidades aplicadas à tarifa adquirida. |
| **No Show** | Indica se houve ou não comparecimento do passageiro com reserva confirmada para o embarque, a qual não foi cancelada dentro do prazo estipulado. Valores: **Sim** (houve no show) / **Não** (não houve no show). |
| **Remarcado** | Bilhete emitido, mas devido a mudanças na viagem, foi alterado utilizando o crédito do bilhete anteriormente adquirido. Valores: **Sim** / **Não**. |
| **Cancelado** | Bilhete emitido, mas devido a mudanças na viagem, não foi utilizado e solicitado o reembolso. Valores: **Sim** / **Não**. |
| **Valor Multas** | Valor monetário da penalidade aplicada nos casos de alteração do bilhete devido à remarcação ou ao cancelamento/reembolso. |
| **Valor Reembolso** | Valor monetário do crédito devolvido pela não utilização do bilhete, conforme regra tarifária. |
| **Diferença de Tarifa** | Valor monetário eventualmente desembolsado devido ao aumento da tarifa nos casos de remarcação do bilhete, em razão da alteração da viagem. |
| **Situação Final Bilhete** | Identifica a situação final do bilhete aéreo: **Voado** (utilizado), **Cancelado** (não utilizado, crédito solicitado), **Andamento** (remarcação ou reembolso ainda não finalizado). |
