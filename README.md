# scdp-ml-project

Projeto de **Introdução a Machine Learning** (mestrado em Ciência de Dados) com foco em **diárias e passagens** do governo federal (SCDP — Sistema de Custos de Diárias e Passagens). Objetivo: análise exploratória e modelagem de **regressão** para prever valor da despesa, com vistas a orçamento, redução de custos e sustentabilidade.

---

## Estrutura do repositório

| Arquivo / pasta | Descrição |
|-----------------|-----------|
| **`DiariasEPassagens_ultimos_2_anos.csv`** | Base de dados (diárias e passagens, últimos 2 anos; não versionada se for grande — ver `.gitignore`). |
| **`daily_rates_and_tickets.ipynb`** | **Relatório preliminar (Fase 1)** do projeto: descrição da base, dicionário, análises descritivas, gráficos, discussão e próximos passos. Adaptado do template ao contexto SCDP (Opção A: regressão). |
| **`template_report_fase_one.ipynb`** | Template da disciplina (estrutura do relatório; não preencher diretamente). |
| **`pre_projeto_diarias_passagens.md`** | Documento de pré-projeto: contexto, problema, opções de ML, dicionário de dados (resumo), fases, qualidade dos dados, referências. |
| **`dicionario_dados.xlsx`** | Dicionário de dados em **Excel** (23 variáveis: nome, tipo, unidade, descrição). Entrega conforme template. |
| **`dicionario_dados.csv`** | Mesmo dicionário em CSV (separador `;`) para versionamento. |
| **`scdp_exploration.ipynb`** | Notebook de exploração inicial da base (carga, primeiras análises). |
| **`requirements.txt`** | Dependências Python (pandas, openpyxl, jupyter, matplotlib, seaborn, etc.). |

---

## Base de dados

- **Fonte:** Dados abertos — [Viagens a serviço do governo federal (SCDP)](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp), Portal da Transparência.
- **Arquivo utilizado:** CSV com registros dos **últimos 2 anos** (ex.: `DiariasEPassagens_ultimos_2_anos.csv`).
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

Coloque o arquivo **`DiariasEPassagens_ultimos_2_anos.csv`** na raiz do projeto (ou ajuste o caminho no notebook).

### 4. Abrir o relatório

Abra **`daily_rates_and_tickets.ipynb`** no Jupyter ou no VS Code/Cursor e execute as células em ordem (carga, conversão de colunas, resumos, gráficos).

---

## Referências

- [dados.gov.br — Conjunto SCDP](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp)
- [Sistema SCDP (novoscdp)](https://www2.scdp.gov.br/novoscdp/home.xhtml)
- [Portal da Transparência — Viagens a Serviço](https://portaldatransparencia.gov.br/viagens/visao-geral)

Documentação detalhada do pré-projeto e do dicionário: **`pre_projeto_diarias_passagens.md`**.

---

## Licença

O **código, notebooks e documentação** deste repositório estão sob a **MIT License** — veja o arquivo [LICENSE](LICENSE). Os **dados** da base (diárias e passagens) vêm de conjuntos de dados abertos do governo federal e estão sujeitos às condições de uso da fonte (dados.gov.br / Portal da Transparência).
