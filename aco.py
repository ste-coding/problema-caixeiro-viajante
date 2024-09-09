import tsplib95
import numpy as np
import math 
import random   
import time 
import argparse
import os


def calcular_distancia(cidade1, cidade2):   
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1]- cidade2[1])**2)  

def ler_coordenadas(arquivo_tsp):
    problem = tsplib95.load(arquivo_tsp)
    #    return [problem.node_coords[node] for node in problem.node_coords]
    cidade = []
    for node in problem.node_coords:
        cidade.append(problem.node_coords[node])
    return cidade


class ColoniadeFormigas:
    def __init__(self, cidades, numero_formigas, melhor_rota, iteracao, evaporacao, alpha=1, beta=1):
        self.cidades = cidades
        self.feromonio = np.ones((len(cidades), len(cidades)))/ len(cidades)
        self.total_cidades = range(len(cidades))
        self.numero_formigas = numero_formigas
        self.melhor_rota = melhor_rota 
        self.iteracao = iteracao
        self.evaporacao = evaporacao
        self.alpha = alpha
        self.beta = beta


    def distancia_cidades(self):
        numero_cidades = len(self.cidades)
        distancia_matriz = np.zeros((numero_cidades, numero_cidades))
        for i in range(numero_cidades):
            for j in range(numero_cidades):
                if i != j:
                    distancia_matriz[i][j] = calcular_distancia(self.cidades[i], self.cidades[j])
        return distancia_matriz

    def run(self):
        menor_percuso = None
        melhor_caminho = ("placeholder", float('inf'))
        historico_custos = []
        distancia = self.distancia_cidades()

        for t in range(self.iteracao):
            caminho_atual = self.caminho_formigas(distancia) #mudança: renomeia todos_caminho para caminho atual
            custo_atual = min(caminho_atual, key=lambda x: x[1])[1]
            historico_custos.append(custo_atual)  # Adiciona o custo atual ao histórico
            self.atual_feromonio(caminho_atual, distancia, self.melhor_rota)
            menor_percuso = min(caminho_atual, key=lambda x: x[1])
            if menor_percuso[1] < melhor_caminho[1]:
                melhor_caminho = menor_percuso
            self.feromonio *= (1 - self.evaporacao)

        caminho_formatado = [(int(start), int(end)) for start, end in melhor_caminho[0]]
        distancia_total = melhor_caminho[1]

        return caminho_formatado, distancia_total, historico_custos #adiciona todos_caminhos

        
    def caminho_formigas(self, distancia):
        todos_caminhos = []
        for i in range(self.numero_formigas):
            cidade_inicial = random.randint(0, len(self.cidades) - 1)
            caminho = self.percuso_formiga(cidade_inicial, distancia)
            todos_caminhos.append((caminho, self.distancia_total(caminho, distancia)))
        return todos_caminhos
    

    def distancia_total(self, caminho, distancia):
        distancia_total = 0 
        for i in range(len(caminho)):
            start, end = caminho[i]
            distancia_total += distancia[start][end]
        return distancia_total       

    def percuso_formiga(self, inicio, distancia):
        caminho_formiga = []
        paradas = set()
        paradas.add(inicio)
        cid_atual = inicio
        for i in range(len(self.cidades) - 1):
            ponto = self.prox_cidade(self.feromonio[cid_atual], distancia[cid_atual], paradas)
            caminho_formiga.append((cid_atual, ponto))
            cid_atual = ponto
            paradas.add(ponto)
        caminho_formiga.append((cid_atual, inicio))
        return caminho_formiga
    
    def atual_feromonio(self, todos_caminhos, distancia, melhor_rota):
        caminho_ordenado = sorted(todos_caminhos, key=lambda x: x[1])
        for caminho, dist in caminho_ordenado[:melhor_rota]:
            for start, end in caminho:
                self.feromonio[start][end] += 1.0 / dist
                self.feromonio[end][start] += 1.0 / dist 
            

    def prox_cidade(self, feromonio, dist, visitado):
        feromonio = np.copy(feromonio)
        feromonio[list(visitado)] = 0 
        dist[dist == 0] = 1e-10  # Pequeno valor para evitar divisão por zero
        escolha_cidade = feromonio ** self.alpha * ((1.0 / dist) ** self.beta)
        
        if np.all(escolha_cidade == 0):
            escolha_cidade[:] = 1  # Se todos os valores são zero, atribui 1 para todas as cidades restantes
        
        escolha_cidade_sum = escolha_cidade.sum()
        if escolha_cidade_sum == 0:
            escolha_cidade[:] = 1
            escolha_cidade_sum = escolha_cidade.sum()
        
        prox_escolha = escolha_cidade / escolha_cidade_sum
        
        if np.any(np.isnan(prox_escolha)) or np.any(np.isinf(prox_escolha)):
            prox_escolha = np.nan_to_num(prox_escolha)
        
        ponto = np.random.choice(self.total_cidades, 1, p=prox_escolha)[0]
        return ponto

def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo de Colônia de Formigas para o problema do caixeiro viajante.")
    parser.add_argument('arquivo_tsp', type=str)
    parser.add_argument('numero_formigas', type=int)
    parser.add_argument('melhor_rota', type=int)
    parser.add_argument('iteracoes', type=int)
    parser.add_argument('evaporacao', type=float)
    parser.add_argument('alpha', type=float)
    parser.add_argument('beta', type=float)
    parser.add_argument('num_execucoes', type=int)

    args = parser.parse_args()
    
    resultados_existentes = {}
    if os.path.exists('resultados_colonia_formigas.npz'):
        dados_existentes = np.load('resultados_colonia_formigas.npz', allow_pickle=True)
        resultados_existentes = {k: dados_existentes[k].item() for k in dados_existentes.keys()}
    
    for i in range(args.num_execucoes):
        tempo_inicial = time.time()
        coordenadas = ler_coordenadas(args.arquivo_tsp)
        aco = ColoniadeFormigas(coordenadas, args.numero_formigas, args.melhor_rota, args.iteracoes, args.evaporacao, args.alpha, args.beta)
        melhor_caminho, distancia_total, historico_custos = aco.run()
        tempo_final = time.time()

        resultado = {
            'melhor_caminho': melhor_caminho,
            'distancia_total': distancia_total,
            'tempo_execucao': tempo_final - tempo_inicial,
            'historico_custos': historico_custos
        }
        
        resultados_existentes[f'execucao_{i+1}'] = resultado
    
    np.savez('resultados_colonia_formigas.npz', **resultados_existentes)

if __name__ == "__main__":
    main()