import itertools
import timeit

def read_matrix(file):
    """ler todas as linhas, exceto a primeira (slice)"""
    with open(file, 'r') as f:
        return [list(line.strip()) for line in f.readlines()[1:]]

def find_points(matrix):
    """"Itera sob cada linha e retorna os pontos com suas cordenadas em um dic, i é o indice da linha e row é a lista de caracteres na matriz. Para cada combinação de (i, j, char) que passa pelo filtro if, um par char: (i, j) é criado no dicionário."""
    return {char: (i, j) for i, row in enumerate(matrix) for j, char in enumerate(row) if char != '0'}

#soma das diferenças absolutas
taxi_geometry = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def route_cost(route, points):
    """recebe a rota e os dicionarios(points definido em main), itera sob cada par de pontos consecutivos até a penultima posição (já que a última não tem consecutivo), calcula a distância e soma"""
    return sum(taxi_geometry(points[route[i]], points[route[i + 1]]) for i in range(len(route) - 1))

def find_best_route(points):
    """cria lista com os pontos de interesse, excluindo R. Gera permutaçõese chama route_cost para caulcular o custo de cada uma e retorna a menor"""
    deliveries = [point for point in points if point != 'R']
    return ''.join(min(itertools.permutations(deliveries), key=lambda perm: route_cost(['R'] + list(perm) + ['R'], points)))

def main():
    matrix = read_matrix('./instancias/forca_bruta/input.txt')
    points = find_points(matrix)
    start_time = timeit.default_timer()
    best_route = find_best_route(points)
    print("Best route:", best_route)
    print("Execution time: {:.4f} seconds".format(timeit.default_timer() - start_time))

if __name__ == '__main__':
    main()
