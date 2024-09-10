import tsplib95
import random
import numpy as np
import argparse
import time
from math import sqrt

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
    historico_custos = []
    while True:
        vizinhaca = Vizinhaca(solucao)
        melhor_vizinha = max(vizinhaca, key=lambda vizinha: calcularQualidade(vizinha, coordenadas_pontos), default=None)
        custo_atual = calcularQualidade(solucao, coordenadas_pontos)
        historico_custos.append(-custo_atual)

        if melhor_vizinha and calcularQualidade(melhor_vizinha, coordenadas_pontos) > custo_atual:
            solucao = melhor_vizinha
        else:
            break
    return solucao, historico_custos

def GRASP(maxInteracoes, LRC, coordenadas_pontos, alpha=0.1):
    melhorSolucao = None
    historico_custos = []

    for _ in range(maxInteracoes):
        solucao = construcaoGulosaRandomica(LRC, coordenadas_pontos, alpha)
        solucao, custo_historico = buscaLocal(solucao, coordenadas_pontos)
        historico_custos.append(custo_historico)

        if melhorSolucao is None or calcularQualidade(solucao, coordenadas_pontos) > calcularQualidade(melhorSolucao, coordenadas_pontos):
            melhorSolucao = solucao
    return melhorSolucao, historico_custos

def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo GRASP para o problema do caixeiro viajante.")
    parser.add_argument('arquivo_tsp', type=str, help="O arquivo .tsp com as coordenadas dos pontos.")
    parser.add_argument('maxInteracoes', type=int, help="Número máximo de iterações.")
    parser.add_argument('alpha', type=float, help="Parâmetro alpha para a construção gulosa randomica.")
    parser.add_argument('num_execucoes', type=int, help="Número de execuções do algoritmo.")
    parser.add_argument('execucao_num', type=int, help="Número da execução atual.")
    parser.add_argument('--seed', type=int, default=None, help="Seed para reprodutibilidade")
    parser.add_argument('--output', type=str, required=True, help="Nome do arquivo de saída.")

    args = parser.parse_args()
    
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    coordenadas_pontos = lerCoordenadas(args.arquivo_tsp)
    LRC = list(coordenadas_pontos.keys())
    
    start_time = time.time()
    melhor_solucao, historico_custos = GRASP(args.maxInteracoes, LRC, coordenadas_pontos, args.alpha)
    tempo_execucao = time.time() - start_time
    
    distancia_total = -calcularQualidade(melhor_solucao, coordenadas_pontos)
    
    # Carregar resultados existentes, se houver
    try:
        dados_existentes = np.load(args.output, allow_pickle=True)
        resultados_grasp = dados_existentes['resultados_grasp'].tolist()
    except FileNotFoundError:
        resultados_grasp = []
    
    resultados_grasp.append({
        'execucao_num': args.execucao_num,
        'melhor_caminho': melhor_solucao,
        'tempo_execucao': tempo_execucao,
        'distancia_total': distancia_total,
        'historico_custos': historico_custos
    })
    
    np.savez(args.output, resultados_grasp=resultados_grasp)

if __name__ == "__main__":
    main()
