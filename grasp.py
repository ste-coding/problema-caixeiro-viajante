import tsplib95
import random
from math import sqrt
import time
import numpy as np # importa numpy
import argparse #importa para tratar argumentos
import os



def lerCoordenadas(arquivo_tsp):
    problema = tsplib95.load(arquivo_tsp)
    coordenadas_pontos = problema.node_coords
    return coordenadas_pontos

def calcularDistancia(ponto1, ponto2):
    return sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)

def calcularQualidade(solucao, coordenadas_pontos):
    distancia_total = sum(
        calcularDistancia(coordenadas_pontos[solucao[i]], coordenadas_pontos[solucao[i + 1]])
        for i in range(len(solucao) - 1)
    )
    distancia_total += calcularDistancia(coordenadas_pontos[solucao[-1]], coordenadas_pontos[solucao[0]])
    return -distancia_total

def construcaoGulosaRandomica(LRC, coordenadas_pontos, alpha=0.1):
    LC = set(LRC)
    solucao = []
    ponto_atual = random.choice(list(LC))
    solucao.append(ponto_atual)
    LC.remove(ponto_atual)
    while LC:
        distancias = [(ponto, calcularDistancia(coordenadas_pontos[ponto_atual], coordenadas_pontos[ponto])) for ponto in LC]
        distancias.sort(key=lambda x: x[1])
        limite = distancias[0][1] + alpha * (distancias[-1][1] - distancias[0][1])
        lrc = [ponto for ponto, distancia in distancias if distancia <= limite]
        proximo_ponto = random.choice(lrc)
        solucao.append(proximo_ponto)
        LC.remove(proximo_ponto)
        ponto_atual = proximo_ponto
    return solucao

def Vizinhaca(solucao):
    vizinhaca = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            nova_solucao = solucao[:]
            nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]
            vizinhaca.append(nova_solucao)
    for i in range(len(solucao) - 1):
        for j in range(i + 2, len(solucao)):
            nova_solucao = solucao[:]
            nova_solucao[i:j+1] = reversed(solucao[i:j+1])
            vizinhaca.append(nova_solucao)
    return vizinhaca

def buscaLocal(solucao, coordenadas_pontos):
    historico_custos = [] #inicializa historico de custos
    while True:
        vizinhaca = Vizinhaca(solucao)
        melhor_vizinha = max(vizinhaca, key=lambda vizinha: calcularQualidade(vizinha, coordenadas_pontos), default=None)
        custo_atual = calcularQualidade(solucao, coordenadas_pontos) # cria variavel que armazena o custo atual
        historico_custos.append(-custo_atual) #adiciona ao historico de custos

        if melhor_vizinha and calcularQualidade(melhor_vizinha, coordenadas_pontos) > custo_atual: #mudei o calcularQualidade(...) para custo_atual pois já foi inicializado lá em cima
            solucao = melhor_vizinha
        else:
            break
    return solucao, historico_custos #retorna o historico de custos tbm

def GRASP(maxInteracoes, LRC, coordenadas_pontos, alpha=0.1):
    melhorSolucao = None
    historico_custos = [] # guardar os historicos de custos

    for _ in range(maxInteracoes):
        solucao = construcaoGulosaRandomica(LRC, coordenadas_pontos, alpha)
        solucao, custo_historico = buscaLocal(solucao, coordenadas_pontos)
        historico_custos.append(custo_historico)

        if melhorSolucao is None or calcularQualidade(solucao, coordenadas_pontos) > calcularQualidade(melhorSolucao, coordenadas_pontos):
            melhorSolucao = solucao
    return melhorSolucao, historico_custos # adiciona historico de custos no return

def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo GRASP para o problema do caixeiro viajante.")
    parser.add_argument('arquivo_tsp', type=str, help="O arquivo .tsp com as coordenadas dos pontos.")
    parser.add_argument('maxInteracoes', type=int, help="Número máximo de iterações.")
    parser.add_argument('alpha', type=float, help="Parâmetro alpha para a construção gulosa randomica.")
    parser.add_argument('num_execucoes', type=int, help="Número de execuções do algoritmo.")
    
    args = parser.parse_args()
    
    resultados_existentes = {}
    if os.path.exists('resultados_grasp.npz'):
        dados_existentes = np.load('resultados_grasp.npz', allow_pickle=True)
        resultados_existentes = {k: dados_existentes[k].item() for k in dados_existentes.keys()}
    
    for i in range(args.num_execucoes):
        inicio = time.time()
        coordenadas_pontos = lerCoordenadas(args.arquivo_tsp)
        LRC = list(coordenadas_pontos.keys())
        melhorSolucao, historico_custos = GRASP(args.maxInteracoes, LRC, coordenadas_pontos, args.alpha)
        distancia_total = -calcularQualidade(melhorSolucao, coordenadas_pontos)
        tempo_execucao = time.time() - inicio
        resultado = {
            'melhor_caminho': melhorSolucao,
            'distancia_total': distancia_total,
            'tempo_execucao': tempo_execucao,
            'historico_custos': historico_custos
        }
        
        resultados_existentes[f'execucao_{i+1}'] = resultado
    
    np.savez('resultados_grasp.npz', **resultados_existentes)

if __name__ == "__main__":
    main()