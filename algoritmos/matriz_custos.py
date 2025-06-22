# algoritmos/matriz_custos.py

import pandas as pd
import os

def calcular_matriz_custos(
    path_dist="dados/matriz_distancias.csv",
    path_temp="dados/matriz_tempos.csv",
    custo_km=1.0,    # Custo por km, definido pelo usuário via dashboard
    custo_min=0.0,   # Custo por minuto, definido pelo usuário via dashboard
    path_saida="dados/matriz_custos.csv"
):
    """
    Calcula a matriz de custos totais entre cada par de municípios, considerando pesos diferenciados
    para a distância e o tempo de viagem, conforme parametrização escolhida na interface.
    Permite adicionar custos extras em trechos específicos (ex: pedágios) diretamente via dashboard.
    """
    # Lê as matrizes de distância e tempo
    dist = pd.read_csv(path_dist, index_col=0)
    temp = pd.read_csv(path_temp, index_col=0)
    # Trata possíveis valores ausentes ou inválidos
    dist = dist.apply(pd.to_numeric, errors='coerce').fillna(float('inf'))
    temp = temp.apply(pd.to_numeric, errors='coerce').fillna(float('inf'))

    # Calcula o custo total para cada trecho
    custos = dist * custo_km + temp * custo_min
    custos.to_csv(path_saida)
    return custos
