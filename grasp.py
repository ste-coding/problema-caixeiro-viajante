import tsplib95
import random
from math import sqrt
import time

def lerCoordenadas(arquivo):
    problema = tsplib95.load(arquivo)
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
    while True:
        vizinhaca = Vizinhaca(solucao)
        melhor_vizinha = max(vizinhaca, key=lambda vizinha: calcularQualidade(vizinha, coordenadas_pontos), default=None)
        if melhor_vizinha and calcularQualidade(melhor_vizinha, coordenadas_pontos) > calcularQualidade(solucao, coordenadas_pontos):
            solucao = melhor_vizinha
        else:
            break
    return solucao

def GRASP(maxInteracoes, LRC, coordenadas_pontos, alpha=0.1):
    melhorSolucao = None
    for _ in range(maxInteracoes):
        solucao = construcaoGulosaRandomica(LRC, coordenadas_pontos, alpha)
        solucao = buscaLocal(solucao, coordenadas_pontos)
        if melhorSolucao is None or calcularQualidade(solucao, coordenadas_pontos) > calcularQualidade(melhorSolucao, coordenadas_pontos):
            melhorSolucao = solucao
    return melhorSolucao

def main():
    inicio = time.time()
    arquivo = 'Caixeiro-Viajante/teste.tsp'
    coordenadas_pontos = lerCoordenadas(arquivo)
    LRC = list(coordenadas_pontos.keys())
    maxInteracoes = 500
    alpha = 0.1
    melhorSolucao = GRASP(maxInteracoes, LRC, coordenadas_pontos, alpha)
    if melhorSolucao:
        distancia_total = -calcularQualidade(melhorSolucao, coordenadas_pontos)
        print(f"\nMelhor Solução:\n {melhorSolucao} \nDistância Total: {distancia_total}")
    else:
        print("Nenhuma solução encontrada.")
    fim = time.time() 
    duracao = fim - inicio  
    print(f"Tempo de execução: {duracao: .2f} segundos")

if __name__ == "__main__":
    main()
