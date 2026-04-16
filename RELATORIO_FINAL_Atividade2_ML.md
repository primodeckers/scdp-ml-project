# Projeto final — Introdução ao Machine Learning

**Disciplina:** Introdução ao Machine Learning  
**Curso:** Mestrado em Administração Pública  
**Área de concentração:** Ciência de Dados e Inteligência Artificial  
**Docente responsável:** Roberta Moreira Wichmann  
**Ano e bimestre de referência:** 2026/1  

**Título do projeto:** Previsão de despesas em diárias e passagens com dados do SCDP  

**Autores:** Renê Estevam; Rodrigo Costa; Liandro Silva  

---

## 1. Introdução

A modelagem está descrita no notebook *rene_estevam_deckers_atividade_2.ipynb*; este ficheiro é o relatório em texto. Os dados são do conjunto **Viagens a Serviço do Governo Federal (SCDP)** ([dados.gov.br](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp)), no mesmo tipo de CSV já trabalhado na Atividade 1 (*rene_estevam_deckers.ipynb*), por exemplo `base_rene_estevam_deckers.csv`.

Cada linha corresponde a um trecho de viagem ou a um lançamento (órgão, unidade gestora, datas, motivo, valores de diárias e de passagem, meio de transporte, origem e destino, entre outros campos). Uma viagem pode aparecer em mais do que uma linha. O foco é explorar padrões de gasto e apoiar a leitura dos custos, sem pretender substituir normas orçamentárias nem decisões administrativas.

O problema abordado é de **regressão**: estimar o **valor total da despesa** em R$ com base nas outras variáveis do registo. No código, o alvo está em `valor_total_num`. A descrição das 23 variáveis mantém-se no `dicionario_rene_estevam_deckers.xlsx` da primeira entrega.

Na construção das preditoras (`X`), retirámos parcelas monetárias que, na mesma linha, entram no **Valor total** (**Valor diárias**, **Valor passagem**) e evitámos repetir o alvo na forma textual do total, para reduzir *data leakage*. Se essas parcelas entrassem como *features*, o modelo aproximava-se de reconstruir o próprio total em vez de aprender a relação com as características da viagem.

---

## 2. Metodologia

No *rene_estevam_deckers_atividade_2.ipynb* percorremos, passo a passo, análise descritiva inicial, divisão treino/teste, pré-processamento, escolha e comparação de modelos, métricas, ajuste de hiperparâmetros e avaliação final no conjunto de teste. O que segue resume as decisões principais; o código e as figuras completas ficam no notebook.

### 2.1. Análise descritiva preliminar

Reutilizámos a preparação da **Atividade 1** (*rene_estevam_deckers.ipynb*): importação do CSV, remoção de duplicatas e conversão para número dos campos de valores e de *Número diárias*, para permitir estatísticas e gráficos coerentes. O conjunto final tem **cerca de 2,2 milhões** de registos.

O **Valor total** (alvo) é assimétrico à direita (média acima da mediana, cauda longa), o que faz com que erros grandes pesem mais em métricas quadráticas. O **Valor passagem** mistura muitos zeros, valores positivos e, por vezes, valores negativos ligados a ajustes. Em **Município**, **UF** e **categoria de passagem** há muitos valores em falta; nos textos (*Cargo*, *Motivo*, *Meio de transporte*) foi preciso combinar imputação com codificação que não explodisse a dimensão.

Na correlação linear com o alvo, sobressaem a **duração em dias** (intervalo entre datas de fim e de início), o **número de diárias** e o **valor monetário das diárias**; estes dois últimos correlacionam bastante entre si, o que aperta modelos lineares simples sem regularização ou sem cuidado na escolha de variáveis. Os gráficos completos da descritiva estão na Atividade 1; aqui só retemos o que guiou a modelagem.

### 2.2. Divisão entre treino e teste

Definimos **80% treino / 20% teste** (`test_size=0.2`) e fixámos **`random_state=42`** para o resultado poder ser repetido ao correr o mesmo código.

Como o alvo é contínuo e muito assimétrico, um *split* puramente aleatório pode desequilibrar, por acaso, a mistura de valores baixos, médios e altos entre treino e teste. Por isso usámos **estratificação por decis** do alvo (`pd.qcut`, com `duplicates="drop"` quando há empates nos quantis) e passámos essa etiqueta ao `stratify` de `train_test_split`, para aproximar a distribuição do custo nos dois lados.

O conjunto de **teste** não entra no `fit` do pré-processamento nem no treino dos modelos; serve só para a **avaliação final**. Linhas sem `valor_total_num` saem antes da divisão. Em `X` ficam as colunas úteis **exceto** o alvo numérico e a coluna textual **Valor total**, quando existe.

### 2.3. Pré-processamento e transformações

Encaixámos pré-processamento e regressor num **`Pipeline`** (`ColumnTransformer` + modelo): medianas, modas, escalas e *one-hot* aprendem-se **só no treino** e aplicam-se ao teste com `transform`, para não haver *data leakage* por estatísticas calculadas com linhas de avaliação.

Criámos **`duracao_dias`** entre a data de fim e a de início (negativos cortados a zero), alinhado ao que na Fase 1 já se observava em relação ao custo. Tirámos também colunas de datas e textos redundantes ou difíceis de tratar no `ColumnTransformer`.

**Valor diárias** e **Valor passagem** ficam de fora das preditoras porque, na mesma linha, entram no total; usá-las como *features* chega perto de “copiar” o alvo. **Nome servidor** saiu por ser identificador individual e pouco adequado a um modelo agregado de despesa, além da questão de privacidade. Mantivemos **Número diárias** como quantidade; tirar o valor monetário das diárias ajuda a não repetir informação entre número e montante.

Valores em falta: `SimpleImputer` com **mediana** nos números e **moda** nas categorias, ajustado no treino. Categorias: `OneHotEncoder` (**até 25 categorias** por variável, `handle_unknown='ignore'`, saída **esparsa** quando o pacote permite), por causa do volume de linhas. Depois da imputação, as numéricas passam por **`StandardScaler`**, o que ajuda o Ridge e coloca escalas mais parecidas.

**HistGradientBoostingRegressor** e **RandomForestRegressor** (nas versões que usámos) pedem **matriz densa** depois do *one-hot*, com `.toarray()` e **muita RAM**. Daí o uso de **subamostras** (`AMOSTRA_CV`, `AMOSTRA_RF`, etc.) nas partes mais pesadas, como forma de caber na máquina disponível sem desistir do exercício.

### 2.4. Construção e escolha do modelo

Testámos três regressores com o **mesmo** pré-processamento (`clone(preprocessor)` + estimador), para que a comparação não misture transformações diferentes.

**Ridge** serve de referência **linear com regularização** (L2) e ainda lida bem com entrada esparsa do *one-hot*. **HistGradientBoostingRegressor** e **RandomForestRegressor** são **árvores** e *ensembles*, mais flexíveis quando há relações não lineares e cruzamentos entre categorias codificadas e variáveis numéricas.

No **treino**, com **`cross_validate`** (MSE negativo, de onde sai o RMSE, mais MAE e R² por *fold*), o teste continuou de fora. Na execução que está no notebook, a **Random Forest** teve o **menor RMSE médio** na validação cruzada; o **Ridge** ficou atrás, o que faz sentido com muitas *dummies* após *one-hot* e com o formato do alvo.

### 2.5. Métricas utilizadas

Usámos **RMSE** (castiga erros grandes; mesma unidade do alvo), **MAE** (erro médio em R$, menos sensível a poucos valores muito extremos) e **R²** (quanto da variância do alvo o modelo explica, no treino/CV ou no teste). As três métricas aparecem na CV e de novo na avaliação final no *hold-out*.

### 2.6. Otimização de hiperparâmetros

Corremos **`RandomizedSearchCV`** numa **subamostra do treino** (`AMOSTRA_SEARCH`), com `cv=3` e `scoring='neg_mean_squared_error'` (o RMSE mostrado é a raiz, para ficar em R$). Preferimos **busca aleatória** a um *grid* completo, pelo tamanho do espaço de hiperparâmetros e pelo tempo de execução.

Afinámos em paralelo **Random Forest**, **HistGradientBoosting** e **Ridge**, **sem olhar para o teste**. Na execução de referência, os melhores RMSE na CV após a busca ficaram por volta de **1022,5** (RF), **1030,6** (HGB) e **1256,6** (Ridge, com `alpha` perto de **3**). Como RF e HGB ficaram próximos na CV, e só há três *folds*, tratámos o **teste** como passo decisivo para escolher o modelo final.

### 2.7. Avaliação final do modelo

Com os *pipelines* que a busca escolheu, fizemos **uma única** avaliação no **conjunto de teste** da secção 2.2: voltámos a calcular RMSE, MAE e R² e gerámos gráficos de **resíduos *vs* predito** e de **predito *vs* real** (com amostragem quando o número de pontos atrapalha o gráfico). Não faz sentido voltar a mexer nos hiperparâmetros à luz do teste — isso deixaria de ser uma leitura imparcial da generalização —, por isso o teste foi usado **uma vez**, como se costuma recomendar neste tipo de trabalho.

---

## 3. Resultados e discussões

### 3.1. Resultados da descritiva preliminar

Os pontos descritivos que mais influenciaram a modelagem já estão resumidos em 2.1 (forma do **Valor total**, zeros e ajustes no **Valor passagem**, falhas em campos geográficos, ligação do custo à **duração** e às **diárias**, e decisão de não usar o **valor monetário das diárias** como preditora). Não repetimos aqui os gráficos; eles continuam no notebook da Atividade 1.

### 3.2. Resultados dos modelos testados

Na validação cruzada do treino, a **Random Forest** teve o menor RMSE médio em relação ao HistGradientBoosting e ao Ridge; o Ridge ficou claramente atrás. Em todos os modelos, o RMSE médio por *fold* foi maior que o MAE, o que indica **alguns erros bem grandes**, coerente com a **cauda longa** do alvo.

Depois da busca de hiperparâmetros, a RF continuou na frente na CV; o Ridge não recuperou.

No **teste** (números da execução registada no notebook):


| Modelo               | RMSE (teste) | MAE (teste) | R² (teste) |
| -------------------- | ------------ | ----------- | ---------- |
| **Random Forest**    | ≈ 812,04     | ≈ 302,96    | ≈ 0,9623   |
| Ridge                | ≈ 1191,81    | ≈ 465,22    | ≈ 0,9188   |
| HistGradientBoosting | ≈ 1247,47    | ≈ 390,12    | ≈ 0,9110   |


O MAE da RF no teste ficou na ordem dos **R$ 303** por linha em média; o RMSE maior diz que ainda há registos em que o erro dispara.

A **Figura 1** ajuda a ver o erro **linha a linha** no teste: em cada ponto, o eixo vertical é o **resíduo** (valor observado menos valor predito pela Random Forest) e o horizontal é o **próprio valor predito**. Espera-se uma nuvem em torno de **zero**; se o espalhamento **crescer** quando o predito aumenta, isso indica que o modelo erra mais nos totais mais altos (ideia retomada na secção 3.3).

![Figura 1 - Resíduos vs valor predito, Random Forest, teste](./figuras/residuos_vs_predito_rf.png)

*Figura 1 — Resíduos (observado − predito) em função do valor predito; Random Forest, conjunto de teste.*

A **Figura 2** compara **total observado** e **total predito** numa **amostra** de linhas (o volume completo tornaria o gráfico ilegível). A referência visual é a **diagonal** onde predito = observado: quanto mais os pontos se aproximam dela, melhor o ajuste; desvios para baixo ou para cima mostram sub ou superestimação.

![Figura 2 - Valores reais vs preditos, Random Forest, amostra](./figuras/predito_vs_real_rf.png)

*Figura 2 — Valores observados versus preditos (amostra); Random Forest.*

### 3.3. Discussão crítica

No teste, a **Random Forest** foi melhor nos três indicadores do que o Ridge e o HistGradientBoosting. Modelos com **muitas árvores em conjunto** costumam lidar melhor com **cruzamentos** e **curvas** quando há muitas categorias depois do *one-hot*, situação em que um modelo **só linear** costuma sofrer. O HistGradientBoosting chegou perto da RF na CV, mas **não acompanhou** no *hold-out* desta corrida; com poucos *folds* e busca aleatória, o teste acabou por desempatar.

Os resíduos parecem mais espalhados quando o valor predito é alto (**heterocedasticidade**). No gráfico **predito *vs* observado**, o miolo acompanha a diagonal; nos totais muito altos o modelo tende a **subestimar**, o que é frequente quando a função de perda é quadrática.

### 3.4. Limitações

Linhas da **mesma viagem** podem estar ligadas entre si; aqui tratámo-las como independentes, o que é uma **simplificação**. A CV e a busca de hiperparâmetros correram sobre **subamostras**, por **memória e tempo**, por isso os números podem mudar um pouco com outra semente ou outro recorte. Não fizemos **corte temporal** entre treino e teste: o modelo descreve o **período coberto pelo ficheiro**, mas não simula de forma rigorosa uma previsão “para a frente”. Por último, a Random Forest **não dá coeficientes** fáceis de ler como numa regressão; para uso institucional mais fino, faria sentido olhar para **importância de variáveis** ou para **SHAP** numa amostra.

---

## 4. Conclusão

Na exploração inicial, o **Valor total** já aparecia assimétrico e ligado à **duração** e ao **número de diárias**. O uso de **Pipeline**, com transformações ajustadas só no treino e sem preditoras que “reconstruam” o total, foi **central** para não enganar na leitura das métricas no teste.

Entre **Ridge**, **HistGradientBoosting** e **Random Forest**, a última — com hiperparâmetros vindos da **`RandomizedSearchCV`** — foi a que **melhor se saiu** no teste (RMSE ≈ 812, MAE ≈ 303, R² ≈ 0,96), ainda com **erros maiores nos valores muito altos**.

Como continuações possíveis (não desenvolvidas neste relatório), caberia testar transformação do alvo (por exemplo `log1p`), validação por **período temporal**, *boosting* em maior escala com **XGBoost**, **LightGBM** e **CatBoost** (habitualmente com **uso de GPU** e memória suficiente), e ferramentas de **explicabilidade** (importância por permutação, SHAP) numa amostra.

---

## 5. Referências

BRASIL. **Conjunto de dados: Viagens a serviço do governo federal – SCDP**. Portal Brasileiro de Dados Abertos, 2026. Disponível em: [https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp](https://dados.gov.br/dados/conjuntos-dados/viagens-a-servico-do-governo-federal-scdp). Acesso em: 16 abr. 2026.

GRUS, J. **Data science do zero: noções fundamentais com Python**. 2. ed. São Paulo: Alta Books, 2021. 416 p. ISBN 978-85-5081-176-5.

HARRISON, M. **Machine learning – guia de referência rápida: trabalhando com dados estruturados em Python**. São Paulo: Novatec, 2019. 272 p. ISBN 978-85-7522-817-3.

HUYEN, C. **Projetando sistemas de machine learning: processo interativo para aplicações prontas para produção**. São Paulo: Alta Books, 2024. 384 p. ISBN 978-85-5081-967-9.

WICHMANN, Roberta Moreira. **Introdução ao Machine Learning: slides de aula**. 2026. Material didático do Mestrado em Administração Pública. [S.l.: s.n.], 2026.

The Matplotlib Development Team. **Matplotlib: visualization with Python**. Disponível em: [https://matplotlib.org](https://matplotlib.org). Acesso em: 16 abr. 2026.

Documentação oficial: **scikit-learn** — User Guide. Disponível em: [https://scikit-learn.org/stable/user_guide.html](https://scikit-learn.org/stable/user_guide.html). Acesso em: 16 abr. 2026.
