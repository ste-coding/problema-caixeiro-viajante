import subprocess

def run_algoritmo(algoritmo, *args):
    try:
        result = subprocess.run(['python', f'{algoritmo}.py', *args], check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print(result.stdout)  # Imprime a saída padrão do script
    except subprocess.CalledProcessError as e:
        print(f"Erro na execução do script {algoritmo}.py: {e.stderr}")


def main():
    # Parâmetros para o GRASP
    arquivo_tsp = './instancias/berlin52.tsp'
    maxInteracoes = 100
    alpha_grasp = 0.1
    num_execucoes_grasp = 3

    # Parâmetros para a Colônia de Formigas
    numero_formigas = 50
    melhor_rota = 5
    iteracoes = 500
    evaporacao = 0.5
    alpha_aco = 1
    beta_aco = 2
    num_execucoes_aco = 3

    # Executar GRASP
    # print("Executando GRASP...")
    run_algoritmo('grasp', arquivo_tsp, str(maxInteracoes), str(alpha_grasp), str(num_execucoes_grasp))

    # Executar Colônia de Formigas
    # print("Executando Colônia de Formigas...")
    run_algoritmo('aco', arquivo_tsp, str(numero_formigas), str(melhor_rota), str(iteracoes), str(evaporacao), str(alpha_aco), str(beta_aco), str(num_execucoes_aco))


if __name__ == "__main__":
    main()
