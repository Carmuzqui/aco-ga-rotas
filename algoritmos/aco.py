# algoritmos/aco.py

import numpy as np
import random

def run_aco(
    matriz_custos,
    matriz_distancias,
    matriz_tempos,
    n_formigas=20,           # Número de formigas (configurado no dashboard)
    n_iter=300,              # Número de iterações (configurado no dashboard)
    alfa=1.0,                # Influência do feromônio (configurável)
    beta=5.0,                # Influência da visibilidade (configurável)
    evaporacao=0.5,          # Taxa de evaporação do feromônio (configurável)
    feromonio_inicial=1.0,   # Valor inicial de feromônio em cada aresta
    cidade_inicio=0,         # Cidade de início (índice, geralmente Patrocínio)
    seed=None                # Semente para reprodutibilidade (para cálculos aleatórios)
):
    # Inicializa semente para reprodutibilidade, se fornecida
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    # Número total de cidades (vértices do grafo)
    n_cidades = matriz_custos.shape[0]
    cidades = list(matriz_custos.index)    # Lista com nomes das cidades
    custos = matriz_custos.values          # Matriz de custos (numpy array)
    distancias = matriz_distancias.values  # Matriz de distâncias
    tempos = matriz_tempos.values          # Matriz de tempos

    # Inicializa matriz de feromônio e matriz de visibilidade (1/custo)
    feromonio = np.ones((n_cidades, n_cidades)) * feromonio_inicial
    visibilidade = 1 / (custos + 1e-10)       # Evita divisão por zero
    np.fill_diagonal(visibilidade, 0)         # Não permite auto-loop

    # Inicializa variáveis para armazenar a melhor solução
    melhor_rota = None
    melhor_custo = float("inf")
    melhor_dist = float("inf")
    melhor_tempo = float("inf")
    historico = []        # Guarda o custo mínimo em cada iteração

    top_rotas = []        # Guarda todas as rotas únicas geradas

    # Loop principal do algoritmo (número de iterações)
    for iteracao in range(n_iter):
        rotas = []           # Rotas encontradas nesta iteração
        custos_rotas = []
        dist_rotas = []
        tempo_rotas = []

        # Cada formiga constrói uma solução (rota completa)
        for _ in range(n_formigas):
            visitado = [False] * n_cidades
            atual = cidade_inicio
            caminho = [atual]
            visitado[atual] = True

            # Construção da rota (visitando cada cidade uma vez)
            for _ in range(n_cidades - 1):
                probas = []
                for j in range(n_cidades):
                    if not visitado[j]:
                        prob = (feromonio[atual, j] ** alfa) * (visibilidade[atual, j] ** beta)
                        probas.append(prob)
                    else:
                        probas.append(0)
                soma = sum(probas)
                if soma == 0:
                    # Caso extremo: todos já visitados (deve evitar)
                    prox = [j for j, v in enumerate(visitado) if not v][0]
                else:
                    probas = [p / soma for p in probas]
                    prox = np.random.choice(range(n_cidades), p=probas)
                caminho.append(prox)
                visitado[prox] = True
                atual = prox

            # Fecha o ciclo retornando à cidade inicial
            caminho.append(cidade_inicio)

            # Calcula custo, distância e tempo total da rota construída
            custo_total = sum(custos[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
            dist_total = sum(distancias[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
            tempo_total = sum(tempos[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
            rotas.append(caminho)
            custos_rotas.append(custo_total)
            dist_rotas.append(dist_total)
            tempo_rotas.append(tempo_total)

            # Atualiza melhor solução encontrada até agora
            if custo_total < melhor_custo:
                melhor_custo = custo_total
                melhor_rota = caminho[:]
                melhor_dist = dist_total
                melhor_tempo = tempo_total

        # Atualiza feromônios globalmente (evaporação)
        feromonio = feromonio * (1 - evaporacao)
        # Reforça feromônio nos caminhos das soluções encontradas
        for rota, custo in zip(rotas, custos_rotas):
            for i in range(len(rota) - 1):
                feromonio[rota[i], rota[i + 1]] += 1.0 / (custo + 1e-10)

        # Salva histórico do melhor custo
        historico.append(melhor_custo)

        # Armazena todas as rotas distintas para posterior seleção das top 3
        for rota, custo, dist, tempo in zip(rotas, custos_rotas, dist_rotas, tempo_rotas):
            if (tuple(rota), custo, dist, tempo) not in top_rotas:
                top_rotas.append((rota, custo, dist, tempo))

    # Seleciona as três melhores rotas distintas após todas as iterações
    top_rotas = sorted(top_rotas, key=lambda x: x[1])
    melhores_3 = []
    rotas_cidades_str = set()
    for rota, custo, dist, tempo in top_rotas:
        rota_nomes = tuple(cidades[i] for i in rota)
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

    # Converte índice para nomes de cidades na melhor rota
    rota_cidades = [cidades[i] for i in melhor_rota]

    # Retorna um dicionário com todos os resultados relevantes
    return {
        "rota": rota_cidades,           # Melhor rota encontrada (nomes das cidades)
        "custo": melhor_custo,          # Custo total da melhor rota
        "distancia": melhor_dist,       # Distância total da melhor rota
        "tempo": melhor_tempo,          # Tempo total da melhor rota
        "historico": historico,         # Lista do custo mínimo a cada iteração
        "top_3": melhores_3             # Lista com as três melhores rotas distintas
    }
