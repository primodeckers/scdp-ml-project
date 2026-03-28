# Planejamento: MLflow no projeto SCDP

Documento de referência para **implementar o MLflow mais adiante**, quando a etapa de **modelagem supervisionada** (regressão do **Valor total**) estiver em andamento. Nada aqui é obrigatório para o relatório preliminar; serve como roteiro técnico.

---

## Objetivo

- Registrar **experimentos** de forma reprodutível: parâmetros, métricas, artefatos e versões de modelo.
- Comparar execuções (ex.: baseline linear vs. Ridge vs. Random Forest) sem depender só de planilhas ou células soltas no notebook.
- Opcionalmente usar o **Model Registry** para versionar um modelo candidato a “produção” ou entrega.

---

## O que é o MLflow (em resumo)

- **Tracking**: cada treino vira uma **run** com parâmetros, métricas e arquivos anexos.
- **Modelos**: salvar o pipeline ou o estimador (ex.: `sklearn`) com metadados.
- **UI local**: comando `mlflow ui` para navegar runs em um navegador (pasta `mlruns/` por padrão).

Documentação oficial: [https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html)

---

## Encaixe neste projeto

Os dados vêm do **mesmo conjunto aberto SCDP**; no disco o ficheiro pode chamar-se `DiariasEPassagens_ultimos_2_anos.csv` (fluxo genérico) ou `base_rene_estevam_deckers.csv` (cópia local no relatório nominal). O que importa para MLflow é **registar qual caminho e qual notebook** geraram o `df` da run.

| Aspecto | Uso sugerido |
|--------|----------------|
| **Alvo** | `Valor total` (regressão), conforme Opção A do relatório |
| **Parâmetros** | Tipo de modelo, hiperparâmetros, `random_state`, tamanho da amostra, estratégia de split (ex.: temporal), opções de pré-processamento (imputação, one-hot, `drop_first`) |
| **Métricas** | RMSE, MAE, R² no treino/validação/teste; opcionalmente tempo de treino |
| **Artefatos** | Gráficos (predito vs. real, resíduos), `requirements` ou hash do ambiente, notas em Markdown |
| **Modelo** | `mlflow.sklearn.log_model` com o **Pipeline** completo (pré-processamento + estimador), para não “perder” o encoders |

**Onde está a análise de encoding:** cardinalidade das categóricas e ilustração com `pd.get_dummies` (`drop_first`) estão no notebook **`one_hot_encoding_variaveis_categoricas.ipynb`** (complemento ao relatório preliminar — `daily_rates_and_tickets.ipynb` ou `rene_estevam_deckers.ipynb`, conforme o que você usar para gerar `df`). Ao registrar runs, alinhe parâmetros de pré-processamento (quais colunas, `drop_first`, etc.) ao que foi documentado ali.

---

## Passos sugeridos (quando for implementar)

1. **Dependência**  
   Adicionar `mlflow` ao `requirements.txt` (fixar versão após testar).

2. **Ignorar artefatos no Git**  
   Incluir no `.gitignore`, por exemplo:
   - `mlruns/`
   - `mlartifacts/` (se usar caminho padrão de artefatos)  
   Runs podem ficar **grandes**; versionar só **código**, não histórico local de experimentos.

3. **Organização do código**  
   - Extrair o treino para um script `.py` (ex.: `train.py`) ou notebook dedicado à modelagem, com `if __name__ == "__main__"` ou células claras.  
   - Envolver o treino com:
     - `mlflow.set_experiment("scdp-valor-total")` (nome exemplificativo)
     - `with mlflow.start_run():` … `mlflow.log_param(...)`, `mlflow.log_metric(...)`, `mlflow.log_artifact(...)`.

4. **Reprodutibilidade**  
   - Logar `random_state`, tamanho da amostra, caminho do CSV usado (`DiariasEPassagens_ultimos_2_anos.csv` ou `base_rene_estevam_deckers.csv`, etc.) e, se fizer sentido, o notebook de origem (`daily_rates_and_tickets` vs `rene_estevam_deckers`). Não commitar dados privados.  
   - Opcional: `mlflow.log_text` com o conteúdo de `requirements.txt` ou versões de `pandas`/`sklearn`.

5. **Interface**  
   Na raiz do projeto (ou onde estiver `mlruns/`):  
   `mlflow ui`  
   Abrir o URL indicado no terminal (geralmente `http://127.0.0.1:5000`).

6. **(Opcional) Servidor remoto ou Databricks**  
   Só se o time precisar compartilhar runs; para trabalho individual, o modo local costuma bastar.

---

## Esqueleto conceitual (Python)

Não é código pronto para colar; ilustra a ideia:

```python
import mlflow
import mlflow.sklearn

# mlflow.set_tracking_uri("file:./mlruns")  # padrão local

with mlflow.start_run(run_name="baseline-ridge"):
    mlflow.log_param("model", "Ridge")
    mlflow.log_param("alpha", 1.0)
    # ... treinar pipeline ...
    mlflow.log_metric("rmse_val", rmse_val)
    mlflow.log_metric("r2_val", r2_val)
    mlflow.sklearn.log_model(pipeline, "model")
```

Ajustar imports e nomes conforme o pipeline real (ex.: `ColumnTransformer` + regressão).

---

## Cuidados

- **Volume de dados**: a base SCDP pode ser grande; runs que copiam o dataset inteiro para artefatos devem ser evitadas. Logar **amostras** ou **caminhos** com moderação.
- **Dados públicos**: ainda assim, não commitar CSV gigante no repositório; o `.gitignore` já trata padrões de arquivos de diárias.
- **Overhead**: para experimentos muito simples, MLflow pode ser opcional; o ganho aparece quando há **várias** combinações de modelo e pré-processamento.

---

## Checklist rápido antes da primeira run

- [ ] `mlflow` instalado e testado (`pip show mlflow` ou equivalente).
- [ ] `mlruns/` (e similares) no `.gitignore`.
- [ ] Um experimento com nome estável (`set_experiment`).
- [ ] Métricas alinhadas ao relatório (RMSE, MAE, R²).
- [ ] Modelo salvo como **pipeline** completo, se houver transformações.

---

## Referências

- MLflow — documentação: [https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html)
- MLflow + scikit-learn — exemplos na documentação de *MLflow Models* e *Tracking*.
