# Projeto Interdisciplinar para Sistemas de Informação II
### Colônia de Formigas e GRASP aplicados ao problema do caxiero viajante

Este projeto implementa e compara dois algoritmos para resolver o problema do caixeiro viajante (TSP): GRASP e Colônia de Formigas. O objetivo é analisar a relação entre qualidade de resposta e tempo de execução desses algoritmos ao tentar encontrar a rota mais curta que visita um conjunto de cidades e retorna à cidade de origem.

## Estrutura do Projeto

- **`instancias/`**: Contém arquivos de instância do problema TSP.
  - `berlin52.tsp`
  - `teste.tsp`
  
- **`main.py`**: Script principal que executa os algoritmos GRASP e Colônia de Formigas com os parâmetros fornecidos.

- **`grasp.py`**: Implementação do algoritmo GRASP para resolver o TSP.

- **`aco.py`**: Implementação do algoritmo Colônia de Formigas (ACO) para resolver o TSP.

- **`dados.ipynb`**: Caderno Jupyter para análise dos dados gerados e criação de gráficos.

- **`resultados_grasp.npz`**: Arquivo com os dados extraídos do algoritmo GRASP.

- **`resultados_colonia_formigas.npz`**: Arquivo com os dados extraídos do algoritmo Colônia de Formigas.

- **`requerimentos.txt`**: Arquivo com as dependências necessárias para executar o projeto.

## Como Executar

### Instalação

Para instalar as dependências, execute:

```bash
pip install -r requerimentos.txt
```

*Executando os Algoritmos*
GRASP: Para executar o algoritmo GRASP, use o seguinte comando:

```bash
python main.py grasp <arquivo_tsp> <maxInteracoes> <alpha> <num_execucoes>
```
Onde:
- **`arquivo_tsp`**: Caminho para o arquivo .tsp (ex.: ./instancias/berlin52.tsp)
- **`maxInteracoes`**: Número máximo de iterações
- **`alpha`**: Parâmetro alpha para a construção gulosa randomica
- **`num_execucoes`**: Número de execuções do algoritmo


Colônia de Formigas (ACO): Para executar o algoritmo de Colônia de Formigas, use o seguinte comando:

```bash
python main.py aco <arquivo_tsp> <numero_formigas> <melhor_rota> <iteracoes> <evaporacao> <alpha> <beta> <num_execucoes>
```
Onde:

- **`arquivo_tsp`**: Caminho para o arquivo .tsp (ex.: ./instancias/berlin52.tsp)
- **`numero_formigas`**: Número de formigas
- **`melhor_rota`**: Parâmetro alpha para o feromônio
- **`iteracoes`**: Número de iterações
- **`evaporacao`**: Taxa de evaporação do feromônio
- **`alpha`**: Parâmetro alpha para o feromônio
- **`beta`**: Parâmetro beta para a distância
- **`num_execucoes`**: Número de execuções do algoritmo

## Análise dos Resultados
Após executar os algoritmos, os resultados serão salvos em arquivos .npz (resultados_grasp.npz e resultados_colonia_formigas.npz). Para analisar os dados e criar gráficos, abra o caderno Jupyter `dados.ipynb` e execute as células.

## Descrição dos Arquivos
- grasp.py: Implementa o algoritmo GRASP para resolver o TSP, incluindo a construção gulosa randomica e a busca local.
- aco.py: Implementa o algoritmo de Colônia de Formigas (ACO) para resolver o TSP, incluindo a atualização do feromônio e a construção do caminho.
- dados.ipynb: Caderno Jupyter para análise dos resultados e visualização dos dados.
- resultados_grasp.npz: Contém os resultados das execuções do algoritmo GRASP.
- resultados_colonia_formigas.npz: Contém os resultados das execuções do algoritmo Colônia de Formigas.
- requerimentos.txt: Lista as dependências necessárias para o projeto.