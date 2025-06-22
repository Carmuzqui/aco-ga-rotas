# algoritmos/ga.py

import numpy as np
import random

def run_ga(
    matriz_custos,
    matriz_distancias,
    matriz_tempos,
    n_pop=50,            # Tamanho da população (configurado no dashboard)
    n_iter=300,          # Número de gerações (configurado no dashboard)
    p_crossover=0.9,     # Probabilidade de crossover (configurável)
    p_mutacao=0.2,       # Probabilidade de mutação (configurável)
    elite_frac=0.2,      # Fração da elite preservada a cada geração (configurável)
    cidade_inicio=0,     # Cidade de início (índice)
    seed=None            # Semente para reprodutibilidade (para cálculos aleatórios)
):
    # Inicializa semente aleatória para garantir reprodutibilidade
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    n_cidades = matriz_custos.shape[0]
    cidades = list(matriz_custos.index)
    custos = matriz_custos.values
    distancias = matriz_distancias.values
    tempos = matriz_tempos.values

    # Funções auxiliares para avaliar cada rota
    def calc_custo(rota):
        # Soma o custo de cada trecho e do retorno à cidade inicial
        return sum(custos[rota[i], rota[i + 1]] for i in range(n_cidades)) + custos[rota[-1], rota[0]]

    def calc_distancia(rota):
        return sum(distancias[rota[i], rota[i + 1]] for i in range(n_cidades)) + distancias[rota[-1], rota[0]]

    def calc_tempo(rota):
        return sum(tempos[rota[i], rota[i + 1]] for i in range(n_cidades)) + tempos[rota[-1], rota[0]]

    # Inicializa população aleatória de rotas (cromossomos)
    pop = []
    for _ in range(n_pop):
        rota = list(range(n_cidades))
        rota.remove(cidade_inicio)
        random.shuffle(rota)
        rota = [cidade_inicio] + rota + [cidade_inicio]
        pop.append(rota)
    pop = np.array(pop)

    historico = []
    melhor_rota = None
    melhor_custo = float("inf")
    melhor_dist = float("inf")
    melhor_tempo = float("inf")

    n_elite = max(1, int(elite_frac * n_pop))

    # Estruturas para deduplicar e armazenar as melhores rotas
    rotas_set = set()
    top_rotas = []

    # Loop principal do algoritmo (gerações)
    for it in range(n_iter):
        # Avalia toda a população
        custos_pop = np.array([calc_custo(ind) for ind in pop])
        dist_pop = np.array([calc_distancia(ind) for ind in pop])
        tempo_pop = np.array([calc_tempo(ind) for ind in pop])
        idx_sorted = np.argsort(custos_pop)
        pop = pop[idx_sorted]  # Ordena a população pelo custo

        # Atualiza o melhor indivíduo da geração
        if custos_pop[idx_sorted[0]] < melhor_custo:
            melhor_custo = custos_pop[idx_sorted[0]]
            melhor_rota = pop[0].tolist()
            melhor_dist = dist_pop[idx_sorted[0]]
            melhor_tempo = tempo_pop[idx_sorted[0]]
        historico.append(melhor_custo)

        # Salva a elite (melhores rotas únicas)
        for ind, custo, dist, tempo in zip(pop[:n_elite], custos_pop[idx_sorted[:n_elite]],
                                           dist_pop[idx_sorted[:n_elite]], tempo_pop[idx_sorted[:n_elite]]):
            rota_tupla = tuple(ind)
            if rota_tupla not in rotas_set:
                top_rotas.append((ind.tolist(), custo, dist, tempo))
                rotas_set.add(rota_tupla)

        # Processo de elitismo: os melhores continuam na nova geração
        nova_pop = [pop[i].tolist() for i in range(n_elite)]

        # Completa a nova população cruzando e mutando os indivíduos
        while len(nova_pop) < n_pop:
            pais = random.sample(list(pop[:20]), 2)  # Seleção entre os 20 melhores
            # Operador de crossover com probabilidade p_crossover
            if random.random() < p_crossover:
                filho = order_crossover(pais[0], pais[1], cidade_inicio)
            else:
                filho = pais[0].tolist()
            # Operador de mutação com probabilidade p_mutacao
            if random.random() < p_mutacao:
                filho = mutation(filho, cidade_inicio)
            nova_pop.append(filho)

        pop = np.array(nova_pop)

    # Seleciona as três melhores rotas únicas
    top_rotas = sorted(top_rotas, key=lambda x: x[1])
    melhores_3 = []
    rotas_cidades_str = set()
    for rota_idx, custo, dist, tempo in top_rotas:
        rota_nomes = tuple(cidades[i] for i in rota_idx)
        if rota_nomes not in rotas_cidades_str:
            melhores_3.append({
                "rota": list(rota_nomes),
                "custo": custo,
                "distancia": dist,
                "tempo": tempo
            })
            rotas_cidades_str.add(rota_nomes)
        if len(melhores_3) == 3:
            break

    rota_cidades = [cidades[i] for i in melhor_rota]
    return {
        "rota": rota_cidades,            # Melhor rota encontrada (nomes das cidades)
        "custo": melhor_custo,           # Custo total da melhor rota
        "distancia": melhor_dist,        # Distância total da melhor rota
        "tempo": melhor_tempo,           # Tempo total da melhor rota
        "historico": historico,          # Lista do custo mínimo por geração
        "top_3": melhores_3              # Lista com as três melhores rotas distintas
    }

def order_crossover(parent1, parent2, cidade_inicio):
    """
    Operador de crossover por ordem (Order Crossover, OX):
    - Seleciona aleatoriamente um segmento de parent1 e o copia para o filho;
    - Preenche os demais genes na ordem em que aparecem em parent2, sem repetição.
    """
    n = len(parent1)
    start, end = sorted(random.sample(range(1, n-1), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    pos = end
    for gene in parent2[1:-1]:
        if gene not in child:
            if pos == n-1:
                pos = 1
            child[pos] = gene
            pos += 1
    child[0] = parent1[0]
    child[-1] = parent1[-1]
    for i in range(1, n-1):
        if child[i] is None:
            child[i] = parent2[i]
    return child

def mutation(rota, cidade_inicio):
    """
    Operador de mutação: inverte um segmento aleatório da rota (2-opt mutation).
    """
    n = len(rota)
    i, j = sorted(random.sample(range(1, n-1), 2))
    rota[i:j] = reversed(rota[i:j])
    return rota
