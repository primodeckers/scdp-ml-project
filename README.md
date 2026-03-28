# scdp-ml-project

Projeto de **Introdução a Machine Learning** (mestrado em Ciência de Dados) com foco em **diárias e passagens** do governo federal (SCDP — Sistema de Custos de Diárias e Passagens). Objetivo: análise exploratória e modelagem de **regressão** para prever valor da despesa, com vistas a orçamento, redução de custos e sustentabilidade.

---

## Estrutura do repositório

| Arquivo / pasta | Descrição |
|-----------------|-----------|
| **`DiariasEPassagens_ultimos_2_anos.csv`** | Cópia “padrão” do conjunto SCDP (últimos 2 anos) usada em `daily_rates_and_tickets.ipynb`, `scdp_exploration` e `one_hot_encoding_*`. Não versionar se for grande — ver `.gitignore`. |
| **`base_rene_estevam_deckers.csv`** | Mesmo tipo de base (mesmo esquema de colunas), com nome local para o relatório entregue em **`rene_estevam_deckers.ipynb`**. Ajuste o `read_csv` se o ficheiro tiver outro nome. |
| **`daily_rates_and_tickets.ipynb`** | Relatório preliminar (Fase 1), alinhado ao template da disciplina: dicionário, 3.1, 3.2, discussão. Usa o CSV `DiariasEPassagens_ultimos_2_anos.csv` por defeito. |
| **`rene_estevam_deckers.ipynb`** | Variante do relatório (mesma estrutura de análise) apontando para **`base_rene_estevam_deckers.csv`**. Mantém-se em paralelo ao `daily_rates_*`; não misturar os dois CSV no mesmo kernel sem voltar a carregar. |
| **`one_hot_encoding_variaveis_categoricas.ipynb`** | Complemento: **one-hot encoding** — cardinalidade por coluna, resumo por faixas e ilustração com `pd.get_dummies` em amostra. Depende de `df` já carregado (mesmo kernel que **`daily_rates_and_tickets`** ou **`rene_estevam_deckers`**, ou rodar antes a preparação nesse relatório). |
| **`template_report_fase_one.ipynb`** | Template da disciplina (estrutura do relatório; não preencher diretamente). |
| **`pre_projeto_diarias_passagens.md`** | Documento de pré-projeto: contexto institucional (viagens/SCDP), problema, opções de ML, dicionário (resumo), fases, qualidade dos dados, referências. |
| **`sugestoes_titulo_pre_projeto.md`** | Ideias de título para capa/relatório (e ligação aos notebooks e ao README). |
| **`mlflow_planejamento.md`** | Roteiro futuro para **MLflow** (tracking de experimentos, métricas, artefatos) quando a etapa de modelagem avançar. |
| **`dicionario_dados.xlsx`** | Dicionário em **Excel** (23 variáveis) usado no fluxo do `daily_rates_and_tickets.ipynb`. Entrega conforme template. |
| **`dicionario_dados.csv`** | Mesmo dicionário em CSV (separador `;`) para versionamento. |
| **`dicionario_rene_estevam_deckers.xlsx`** | Variante de entrega com o mesmo tipo de conteúdo, referenciada no **`rene_estevam_deckers.ipynb`** (nome do ficheiro alinhado ao relatório nominal). |
| **`scdp_exploration.ipynb`** | Notebook de exploração inicial da base (carga, primeiras análises). |
| **`requirements.txt`** | Dependências Python (pandas, openpyxl, jupyter, matplotlib, seaborn, etc.). |

---

## Base de dados

- **Fonte:** Dados abertos — [Viagens a serviço do governo federal (SCDP)](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp), Portal da Transparência.
- **Ficheiro de trabalho:** o mesmo conjunto do portal pode aparecer como `DiariasEPassagens_ultimos_2_anos.csv` (notebooks “genéricos”) ou como cópia renomeada, p.ex. `base_rene_estevam_deckers.csv` no notebook de entrega com o seu nome.
- **Conteúdo:** 23 colunas por registro (trecho de viagem ou lançamento de diária): órgão, unidade gestora, servidor, datas, motivo, valor total, valor diárias, valor passagem, número diárias, meio de transporte, origem/destino, etc. **Variável alvo** na regressão: **Valor total** (R$).

---

## Como rodar

### 1. Ambiente virtual (venv)

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se aparecer erro de política de execução:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS e Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

Com o venv ativado:

```bash
pip install -r requirements.txt
```

### 3. Colocar a base de dados

Coloque na raiz o CSV que o notebook vai ler: **`DiariasEPassagens_ultimos_2_anos.csv`** ou **`base_rene_estevam_deckers.csv`**, conforme o ficheiro que estiver referenciado na primeira carga de dados.

### 4. Abrir o relatório principal

Use **`daily_rates_and_tickets.ipynb`** ou **`rene_estevam_deckers.ipynb`** (conteúdo equivalente; o segundo aponta para `base_rene_estevam_deckers.csv`). Execute as células **em ordem** até ao fim da secção que precisar (carga → numéricos → tabelas → gráficos).

### 5. (Opcional) One-hot e cardinalidade

Abra **`one_hot_encoding_variaveis_categoricas.ipynb`** no **mesmo kernel** em que já existe `df` com `valor_total_num`, ou copie para lá as células de leitura e conversão do CSV que estiver a usar (**Diarias…** ou **base_rene…**).

---

## Referências

- [dados.gov.br — Conjunto SCDP](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp)
- [Sistema SCDP (novoscdp)](https://www2.scdp.gov.br/novoscdp/home.xhtml)
- [Portal da Transparência — Viagens a Serviço](https://portaldatransparencia.gov.br/viagens/visao-geral)

Documentação detalhada do pré-projeto e do dicionário: **`pre_projeto_diarias_passagens.md`**. Ideias de título para capa: **`sugestoes_titulo_pre_projeto.md`**. Planejamento futuro de experimentos: **`mlflow_planejamento.md`**.

---

## Licença

O **código, notebooks e documentação** deste repositório estão sob a **MIT License** — veja o arquivo [LICENSE](LICENSE). Os **dados** da base (diárias e passagens) vêm de conjuntos de dados abertos do governo federal e estão sujeitos às condições de uso da fonte (dados.gov.br / Portal da Transparência).
