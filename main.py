import subprocess
import random

def run_algoritmo(algoritmo, *args, execucao_num=None, seed=None, output=None):
    try:
        if seed is not None:
            args = list(args) + ['--seed', str(seed)]
        if execucao_num is not None:
            args = list(args) + [str(execucao_num)]
        if output is not None:
            args = list(args) + ['--output', output]
        result = subprocess.run(['python', f'{algoritmo}.py', *args], check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print(result.stdout)  # Imprime a saída padrão do script
    except subprocess.CalledProcessError as e:
        print(f"Erro na execução do script {algoritmo}.py: {e.stderr}")

def main():
    seed_principal = 10
    random.seed(seed_principal)
    seeds = [random.randint(1, 1000000) for _ in range(30)]
    
    # Parâmetros para o GRASP
    arquivo_tsp = './instancias/teste.tsp'
    maxInteracoes = 100
    alpha_grasp = 0.5
    num_execucoes_grasp = 30
    output_grasp = 'resultados_grasp_teste.npz'

    # Parâmetros para a Colônia de Formigas
    numero_formigas = 50
    melhor_rota = 5
    iteracoes = 500
    evaporacao = 0.5
    alpha_aco = 1
    beta_aco = 2
    num_execucoes_aco = 30
    output_aco = 'resultados_aco_ulysses.npz'

    # Executar GRASP
    print("Executando GRASP...")
    for i in range(num_execucoes_grasp):
        seed_atual = seeds[i]
        run_algoritmo('grasp', arquivo_tsp, str(maxInteracoes), str(alpha_grasp), str(num_execucoes_grasp), execucao_num=i+1, seed=seed_atual, output=output_grasp)

    # Executar Colônia de Formigas
    print("Executando Colônia de Formigas...")
    for i in range(num_execucoes_aco):
        seed_atual = seeds[i]
        run_algoritmo('aco', arquivo_tsp, str(numero_formigas), str(melhor_rota), str(iteracoes), str(evaporacao), str(alpha_aco), str(beta_aco), str(num_execucoes_aco), execucao_num=i+1, seed=seed_atual, output=output_aco)

if __name__ == "__main__":
    main()
