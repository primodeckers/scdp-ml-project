# scdp-ml-project

Projeto de **Introdução ao Machine Learning** (mestrado em Ciência de Dados) com foco em **diárias e passagens** do governo federal (SCDP — Sistema de Custos de Diárias e Passagens). Objetivo: análise exploratória e modelagem de **regressão** para prever o valor da despesa, com vistas a transparência, orçamento e análise de custos.

---

## Estrutura do repositório

| Ficheiro / pasta | Descrição |
|------------------|-----------|
| **`DiariasEPassagens_ultimos_2_anos.csv`** | Cópia típica do conjunto SCDP (últimos 2 anos) usada em `daily_rates_and_tickets.ipynb`, `scdp_exploration` e `one_hot_encoding_*`. Não versionar se for muito grande — ver `.gitignore`. |
| **`base_rene_estevam_deckers.csv`** | Mesmo esquema de colunas, nome local para o relatório em **`rene_estevam_deckers.ipynb`**. Ajuste o `read_csv` se o ficheiro tiver outro nome. |
| **`rene_estevam_deckers_atividade_2.ipynb`** | **Atividade 2 (modelagem):** pré-processamento, *pipelines* scikit-learn, Ridge / HistGradientBoosting / Random Forest, validação cruzada, `RandomizedSearchCV`, métricas no teste (RMSE, MAE, R²). Variável alvo: **Valor total**. |
| **`RELATORIO_FINAL_Atividade2_ML.md`** | Texto do relatório final (Markdown), alinhado ao template da disciplina. |
| **`RELATORIO_FINAL_Atividade2_ML.docx`** | Versão Word gerada a partir do `.md` (regenerável com o script abaixo). |
| **`figuras/`** | PNG dos gráficos referenciados no relatório (resíduos, previsto *vs* real). |
| **`relatorio/figuras/`** | Cópia espelhada das mesmas figuras (opcional). |
| **`scripts/export_relatorio_docx.py`** | Exporta o `.md` para `.docx` com Times New Roman 12, justificado e espaçamento 1,5. |
| **`daily_rates_and_tickets.ipynb`** | Relatório preliminar (Fase 1), alinhado ao template: dicionário, 3.1, 3.2, discussão. CSV por defeito: `DiariasEPassagens_ultimos_2_anos.csv`. |
| **`rene_estevam_deckers.ipynb`** | Variante da Fase 1 com **`base_rene_estevam_deckers.csv`**. |
| **`one_hot_encoding_variaveis_categoricas.ipynb`** | Complemento: *one-hot encoding* e cardinalidade. Depende de `df` já carregado no mesmo *kernel* ou de correr antes a preparação do CSV em uso. |
| **`template_report_fase_one.ipynb`** | Template da disciplina (estrutura; não preencher diretamente). |
| **`pre_projeto_diarias_passagens.md`** | Pré-projeto: contexto, problema, ML, dicionário (resumo), fases, qualidade dos dados, referências. |
| **`sugestoes_titulo_pre_projeto.md`** | Ideias de título para capa/relatório. |
| **`mlflow_planejamento.md`** | Roteiro futuro para **MLflow** (experimentos e métricas). |
| **`dicionario_dados.xlsx`** / **`dicionario_dados.csv`** | Dicionário (23 variáveis) no fluxo `daily_rates_and_tickets.ipynb`. |
| **`dicionario_rene_estevam_deckers.xlsx`** | Variante referenciada em **`rene_estevam_deckers.ipynb`**. |
| **`scdp_exploration.ipynb`** | Exploração inicial (carga, primeiras análises). |
| **`requirements.txt`** | Dependências Python: ver secção [Como rodar](#como-rodar). |

---

## Base de dados

- **Fonte:** [Viagens a serviço do governo federal (SCDP)](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp) (dados.gov.br / transparência).
- **Ficheiro de trabalho:** `DiariasEPassagens_ultimos_2_anos.csv` ou `base_rene_estevam_deckers.csv`, conforme o notebook.
- **Conteúdo:** cerca de 23 colunas por registro (órgão, UG, datas, motivo, valores, meio de transporte, origem/destino, etc.). Na regressão da Atividade 2, a **variável alvo** é **Valor total** (R$).

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

Com o *venv* ativado:

```bash
pip install -r requirements.txt
```

Inclui **Jupyter**, **pandas**, **scikit-learn**, **matplotlib**, **seaborn**, **plotly**, **openpyxl**, **python-docx** (para gerar o relatório em Word a partir do Markdown).

### 3. Colocar a base de dados

Na raiz do projeto, coloque o CSV que o notebook vai ler: **`DiariasEPassagens_ultimos_2_anos.csv`** ou **`base_rene_estevam_deckers.csv`**, conforme referenciado na primeira célula de carga.

### 4. Notebooks principais

| Objetivo | Notebook |
|----------|----------|
| Fase 1 / EDA (fluxo genérico) | `daily_rates_and_tickets.ipynb` |
| Fase 1 / EDA (cópia `base_rene_…`) | `rene_estevam_deckers.ipynb` |
| **Atividade 2 — modelagem** | `rene_estevam_deckers_atividade_2.ipynb` |

Execute as células **em ordem** até à secção necessária (carga → preparação → modelagem → gráficos).

### 5. (Opcional) One-hot e cardinalidade

Abra **`one_hot_encoding_variaveis_categoricas.ipynb`** no **mesmo *kernel*** em que já existe `df` (por exemplo após carregar o CSV em `daily_rates_*` ou `rene_estevam_deckers*`), ou copie para lá as células de leitura e conversão.

### 6. Relatório final (Markdown → Word → PDF)

1. Edite o conteúdo em **`RELATORIO_FINAL_Atividade2_ML.md`** (e mantenha as imagens em **`figuras/`** se alterar gráficos).
2. Gere o Word:

```bash
python scripts/export_relatorio_docx.py
```

O ficheiro **`RELATORIO_FINAL_Atividade2_ML.docx`** é criado/atualizado na raiz do projeto. No Microsoft Word ou LibreOffice: reveja margens e **exporte para PDF** para entrega, se a disciplina exigir PDF.

> O *preview* de Markdown integrado no Cursor pode não mostrar imagens locais; use **Open Preview** / **Open Preview to the Side** se precisar de pré-visualizar o `.md` com figuras.

---

## Referências

- [dados.gov.br — conjunto SCDP](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp)
- [Sistema SCDP (novoscdp)](https://www2.scdp.gov.br/novoscdp/home.xhtml)
- [Portal da Transparência — Viagens a Serviço](https://portaldatransparencia.gov.br/viagens/visao-geral)

Documentação complementar: **`pre_projeto_diarias_passagens.md`**, **`sugestoes_titulo_pre_projeto.md`**, **`mlflow_planejamento.md`**.

---

## Licença

O **código, notebooks e documentação** deste repositório estão sob a **MIT License** — veja o ficheiro [LICENSE](LICENSE). Os **dados** da base (diárias e passagens) vêm de conjuntos abertos do governo federal e estão sujeitos às condições de uso da fonte (dados.gov.br / Portal da Transparência).
