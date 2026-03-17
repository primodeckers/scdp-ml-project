# Pré-projeto: Diárias e Passagens — Análise e Machine Learning

**Base:** `DiariasEPassagens_ultimos_2_anos.csv`  
**Arquivo de trabalho:** `daily_rates_and_tickets.ipynb`  
**Referência de estrutura:** `template_report_fase_one.ipynb`

---

## 1. Contexto e fonte dos dados

- **Fonte:** Dados abertos do governo federal (portal da transparência / SCDP — Sistema de Custos de Diárias e Passagens), cobrindo os **últimos 2 anos** de gastos com diárias e passagens no âmbito da administração pública federal.
- **Contextualização:** Cada registro representa um **trecho de viagem** (ou lançamento de diária) vinculado a um servidor, órgão, período e valores. Há múltiplas linhas por viagem quando há mais de um trecho (origem–destino) ou quando diárias e passagens são lançadas separadamente. A base permite analisar padrões de gastos, órgãos, motivos, meios de transporte e valores.
- **Relevância:** Transparência, controle de gastos, identificação de padrões e oportunidades de **redução de custos e de impacto ambiental** (viagens desnecessárias, escolha de meios mais sustentáveis).

---

## 2. Problema de pesquisa e objetivo

- **Problema de pesquisa:** Com base nos dados de diárias e passagens dos últimos 2 anos, queremos **entender e modelar** o comportamento dos gastos e, a partir daí, propor uso de **machine learning** para:
  - **Prever** valores (regressão) ou **classificar** eventos (ex.: tipo de deslocamento, motivo, meio de transporte).
  - **Detectar anomalias** (gastos atípicos) ou **agrupar** padrões (órgãos, perfis de viagem) para políticas mais sustentáveis e econômicas.
- **Objetivo da utilização da base:** Construir um pré-projeto bem definido (com dicionário de dados e fases alinhadas ao template da disciplina), preparando o terreno para modelagem em `daily_rates_and_tickets.ipynb`, com foco em **alternativas sustentáveis e em melhor uso dos recursos**.

---

## 3. Opções de modelagem (Machine Learning)

| Opção | Tipo de aprendizado | Variável alvo (exemplo) | Uso sustentável / gestão |
|-------|---------------------|--------------------------|----------------------------|
| **A** | **Regressão** | Valor total (ou Valor diárias / Valor passagem) | Estimar custo esperado por viagem; orçamento e metas de redução. |
| **B** | **Classificação** | Meio de transporte (Aéreo, Rodoviário, etc.) | Entender quando se usa avião vs. alternativas menos poluentes. |
| **C** | **Classificação** | Motivo da viagem (categorizado) | Priorizar viagens essenciais e reduzir “outros”. |
| **D** | **Detecção de anomalias** | Outliers em Valor total / Valor diárias | Sinalizar gastos atípicos para auditoria e controle. |
| **E** | **Clustering** | Sem target — agrupar viagens/órgãos | Perfis de gastos; comparação entre órgãos e políticas. |

**Recomendação inicial:** Definir **uma** variável alvo principal (ex.: regressão para Valor total ou classificação para Meio de transporte) e manter as demais como **análises complementares** ou **próximas fases**, para o relatório não ficar disperso.

---

### 3.1 Exploração da Opção A — Regressão

**Objetivo:** Prever o **valor da despesa** (valor total, valor de diárias ou valor de passagem) a partir de características da viagem e do órgão, para apoiar orçamento, metas de redução de custos e auditoria.

**Formulação do problema (supervisionado — regressão):**
- **Variável alvo (target):** uma entre:
  - **Valor total** — custo total do registro (diárias + passagens); boa para orçamento geral.
  - **Valor diárias** — quando o foco é apenas diárias (muitos registros têm passagem = 0).
  - **Valor passagem** — quando o foco é custo de deslocamento (subset onde há passagem > 0).
- **Variáveis preditoras (candidatas):**
  - **Numéricas:** Código órgão superior, Código órgão, Código unidade gestora, **Número diárias**, duração da viagem (derivada de Data início/término), mês/ano (derivados).
  - **Categóricas (encoding):** Nome órgão superior, Nome órgão, Nome unidade gestora, **Motivo**, **Meio de transporte**, Categoria passagem (quando disponível), UF origem/destino (quando disponível).
- **Métricas típicas:** RMSE, MAE, R² (e eventualmente MAPE para interpretação em %). Validação cruzada ou hold-out temporal (se quiser respeitar ordem no tempo).
- **Cuidados:** (1) Valores com vírgula decimal e colunas em texto devem ser convertidos. (2) Outliers em valor total/diárias podem distorcer; considerar log(y) ou tratamento de cauda. (3) Muitas categorias (órgão, servidor) podem levar a overfitting — agrupar ou usar apenas órgão/motivo/meio no início. (4) Decidir se modelar todos os registros ou subconjuntos (ex.: só registros com passagem > 0 para prever valor passagem).
- **Modelos a explorar:** Regressão linear (baseline), árvore de decisão, random forest, gradient boosting (ex.: sklearn), sempre com pré-processamento (encoding de categorias, eventual escalonamento).

---

## 4. Dicionário de dados (campos da base)

A base possui **23 colunas**. Abaixo, descrição objetiva de cada uma para uso no pré-projeto e no dicionário em Excel (quando for gerado).

| # | Nome do campo | Tipo sugerido | Unidade / valores | Descrição |
|---|----------------|---------------|-------------------|-----------|
| 1 | **Código órgão superior** | Numérico (inteiro) | Código único | Identificador do órgão superior ao qual a despesa está vinculada (ex.: 20000 = Presidência da República). |
| 2 | **Nome órgão superior** | Categórico (texto) | — | Nome do órgão superior (ex.: PRESIDENCIA DA REPUBLICA). |
| 3 | **Código órgão** | Numérico (inteiro) | Código único | Identificador do órgão (pode coincidir com o órgão superior). |
| 4 | **Nome órgão** | Categórico (texto) | — | Nome do órgão. |
| 5 | **Código unidade gestora** | Numérico (float) | Código único | Identificador da unidade gestora que realizou o gasto. Pode haver nulos em casos de consolidação. |
| 6 | **Nome unidade gestora** | Categórico (texto) | — | Nome da unidade gestora (ex.: SECT DE SEG PRESIDENCIAL/GSIPR). |
| 7 | **Nome servidor** | Categórico (texto) | — | Nome do servidor que realizou a viagem ou recebeu a diária. |
| 8 | **Cargo** | Categórico (texto) | — | Cargo do servidor. **Apresenta muitos nulos** na base; útil para análises quando preenchido. |
| 9 | **Data início viagem** | Data | AAAA-MM-DD | Data de início da viagem. |
| 10 | **Data término viagem** | Data/hora | AAAA-MM-DD HH:MM:SS | Data e hora de término da viagem. |
| 11 | **Motivo** | Categórico (texto) | — | Motivo oficial da viagem (ex.: "Nacional - A Serviço", "Audiência", "COMITIVA/ESCAV PRESIDENCIAL", "Viagem - Reunião"). Fundamental para análise de necessidade e sustentabilidade. |
| 12 | **Valor total** | Numérico (decimal) | Reais (R$) | Valor total da despesa do registro (diárias + passagens do trecho, quando aplicável). **Candidato forte a variável alvo em regressão.** |
| 13 | **Início trecho** | Data/hora | AAAA-MM-DD HH:MM:SS | Início do trecho de deslocamento (quando há origem/destino). |
| 14 | **Término trecho** | Data/hora | AAAA-MM-DD HH:MM:SS | Término do trecho. |
| 15 | **Município origem** | Categórico (texto) | — | Município de origem do trecho. **Muitos nulos** quando o registro é só diária (sem trecho de passagem). |
| 16 | **UF origem** | Categórico (texto) | Sigla UF (2 letras) | Unidade federativa de origem. **Muitos nulos** junto com Município origem. |
| 17 | **Município destino** | Categórico (texto) | — | Município de destino do trecho. **Muitos nulos** nos mesmos casos. |
| 18 | **UF destino** | Categórico (texto) | Sigla UF | Unidade federativa de destino. **Muitos nulos.** |
| 19 | **Número diárias** | Numérico (decimal) | Quantidade | Número de diárias pagas no registro (formato pode usar vírgula decimal, ex.: 2,00; ,50). |
| 20 | **Valor diárias** | Numérico (decimal) | Reais (R$) | Valor em reais das diárias. Formato pode usar vírgula decimal. **Candidato a target ou feature.** |
| 21 | **Meio de transporte** | Categórico (texto) | — | Meio utilizado no trecho: Veículo Oficial, Aéreo, Rodoviário, Veículo Próprio, Fluvial, Ferroviário, Marítimo. **Relevante para sustentabilidade.** Poucos nulos. |
| 22 | **Categoria passagem** | Categórico (texto) | — | Categoria da passagem (ex.: Classe Econômica). **Muitos nulos** quando não há passagem (só diária). |
| 23 | **Valor passagem** | Numérico (decimal) | Reais (R$) | Valor pago em passagens no trecho. Zero quando não há passagem. **Candidato a target ou feature.** |

**Observações técnicas:**  
- Valores monetários e "Número diárias" podem vir com vírgula como separador decimal; é necessário padronizar para numérico (ponto decimal) no pré-processamento.  
- Datas em formato texto; converter para `datetime` para análises temporais e duração de viagem.  
- Campos com muitos nulos (Cargo, Município/UF origem e destino, Categoria passagem) devem ser tratados na análise (exclusão, imputação ou uso condicional).

---

## 5. Qualidade dos dados (resumo para discussão preliminar)

- **Valores ausentes:** Cargo (grande quantidade); Município origem/destino, UF origem/destino (ausentes em muitos registros onde não há “trecho” de passagem); Categoria passagem (ausente quando não há passagem); Meio de transporte (poucos nulos).
- **Inconsistências:** Colunas de data/hora e valores em texto; formato numérico com vírgula. Tipos mistos em algumas colunas (ex.: Município/UF) — usar `low_memory=False` ou `dtype` na leitura.
- **Duplicatas:** A base pode conter linhas duplicadas; no notebook de exploração já foi usado `drop_duplicates` (redução de ~2,24M para ~2,21M linhas). Manter critério documentado.
- **Unidades:** Padronizar datas (timezone, se houver), valores em R$ (decimal) e quantidade de diárias.

---

## 6. Fases do pré-projeto (alinhadas ao template da disciplina)

As fases abaixo seguem a lógica do `template_report_fase_one.ipynb`, mas o desenvolvimento será feito em **`daily_rates_and_tickets.ipynb`**; o template serve só de guia de estrutura do relatório.

| Fase | Conteúdo (resumo) | Onde desenvolver |
|------|-------------------|-------------------|
| **1** | **Descrição da base** — Fonte (SCDP/transparência), contextualização, objetivo de uso, problema de pesquisa, tipo de ML (regressão/classificação/outro) e **o que será previsto** (variável alvo). | Texto no relatório + células iniciais do notebook. |
| **2** | **Dicionário de dados** — Todas as variáveis, tipos, unidades e significados. Entregar também em Excel (`dicionario_dados.xlsx`) conforme exigência. | Este MD + arquivo Excel + referência no notebook. |
| **3** | **Análises descritivas iniciais** — Medidas de posição e dispersão (média, mediana, min, max, quartis, dp, CV) para variáveis numéricas principais (Valor total, Valor diárias, Valor passagem, Número diárias); resumos por Motivo e Meio de transporte. | `daily_rates_and_tickets.ipynb`. |
| **4** | **Exploração gráfica** — Histogramas, boxplots, dispersão (ex.: valor total x número diárias; valor por órgão/motivo); séries temporais (gasto por mês). | `daily_rates_and_tickets.ipynb`. |
| **5** | **Discussão preliminar** — Padrões observados; qualidade (nulos, inconsistências, padronização); implicações para a modelagem e para políticas sustentáveis. | Texto no relatório + conclusões no notebook. |
| **6** | **Próximos passos** — Ajustes nos dados; definição formal da variável-alvo e das preditoras; técnicas de ML a testar (ex.: regressão linear, árvores, detecção de anomalias). | Relatório + planejamento no notebook. |

---

## 7. Alternativas sustentáveis e melhores práticas (enfoque do projeto)

- **Redução de viagens desnecessárias:** Usar **Motivo** e padrões temporais para identificar viagens que poderiam ser substituídas por reuniões remotas ou eventos concentrados.  
- **Preferência por meios menos poluentes:** Modelos que expliquem ou prevejam **Meio de transporte** (ex.: quando é mais comum usar aéreo) ajudam a definir metas (ex.: priorizar rodoviário/ferroviário em rotas curtas).  
- **Controle de custos e anomalias:** Regressão para **Valor total** (ou Valor diárias/Valor passagem) e detecção de **outliers** apoiam orçamento e auditoria, liberando verba para outras políticas.  
- **Transparência e clusters:** Agrupamento de órgãos ou perfis de viagem facilita benchmarking e boas práticas entre unidades gestoras.

---

## 8. Próximos passos imediatos

1. **Confirmar** qual será a **variável alvo principal** (regressão ou classificação) para o relatório da disciplina.  
2. **Exportar** o dicionário deste MD para `dicionario_dados.xlsx` (variáveis, tipos, unidades, descrições).  
3. **Implementar** no `daily_rates_and_tickets.ipynb`: carga da base, tratamento de vírgula decimal e datas, e as análises descritivas e gráficos das fases 3 e 4.  
4. **Redigir** o relatório final (em cima do template) com base nos resultados do notebook, sem alterar diretamente o `template_report_fase_one.ipynb` — apenas usar como base de estrutura.

---

## Referências sugeridas

- **Viagens a serviço do governo federal (SCDP)** — Dados abertos: [dados.gov.br – conjunto SCDP](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp).
- **Sistema SCDP:** [novoscdp – home](https://www2.scdp.gov.br/novoscdp/home.xhtml).
- **Portal da Transparência — Viagens a Serviço:** [visão geral](https://portaldatransparencia.gov.br/viagens/visao-geral).
- Normas sobre diárias e passagens no âmbito da administração federal (ex.: IN da CGU/MPOG, se aplicável).
- Material da disciplina de Introdução a Machine Learning (regressão, classificação, métricas, validação).
