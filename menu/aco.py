# import streamlit as st
# import pandas as pd
# from algoritmos.aco import run_aco
# import folium
# from streamlit_folium import st_folium
# import json
# import os
# import plotly.graph_objects as go
# import time

# def render():
#     st.header("Algoritmo de colônia de formigas (ACO)")

#     matriz_custos = pd.read_csv("dados/matriz_custos.csv", index_col=0)
#     cidades = matriz_custos.index.tolist()

#     # Patrocínio por padrão
#     idx_patrocinio = cidades.index("Patrocínio") if "Patrocínio" in cidades else 0
#     cidade_inicio = st.selectbox("Cidade inicial/final", cidades, index=idx_patrocinio)

#     st.subheader("Parâmetros do ACO")
#     n_formigas = st.number_input("Número de formigas", 1, 100, 20)
#     n_iter = st.number_input("Número de iterações", 10, 10000, st.session_state.get("max_iter", 1000), step=10)
#     alfa = st.slider("Alfa (peso do feromônio)", 0.1, 5.0, 1.0, 0.1)
#     beta = st.slider("Beta (peso da heurística)", 0.1, 10.0, 5.0, 0.1)
#     evaporacao = st.slider("Taxa de evaporação", 0.01, 1.0, 0.5, 0.01)

#     if st.button("Executar ACO"):
#         idx_inicio = cidades.index(cidade_inicio)
#         t0 = time.time()
#         resultado = run_aco(
#             matriz_custos,
#             n_formigas=n_formigas,
#             n_iter=n_iter,
#             alfa=alfa,
#             beta=beta,
#             evaporacao=evaporacao,
#             cidade_inicio=idx_inicio
#         )
#         t1 = time.time()
#         resultado["tempo_execucao"] = t1 - t0
#         st.session_state["aco_resultado"] = resultado

#     if "aco_resultado" in st.session_state:
#         resultado = st.session_state["aco_resultado"]
#         st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")
#         st.write(f"Custo total: R$ {resultado['custo']:.2f}")

#         # Visualização no mapa
#         with open("dados/municipios.json", encoding="utf-8") as f:
#             dados_cidades = json.load(f)
#         coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}
#         coordenadas = [coords_dict[nome] for nome in resultado["rota"]]

#         lat_c, lng_c = coordenadas[0]
#         m = folium.Map(location=[lat_c, lng_c], zoom_start=8)
#         folium.Marker([lat_c, lng_c], tooltip="Início", icon=folium.Icon(color="green")).add_to(m)
#         for (lat, lng), nome in zip(coordenadas[1:], resultado["rota"][1:]):
#             folium.Marker([lat, lng], tooltip=nome).add_to(m)
#         folium.PolyLine(locations=coordenadas, color="blue", weight=4).add_to(m)
#         st_folium(m, width=800, height=500)

#         # Gráfico de evolução do custo (Plotly, com títulos)
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             y=resultado["historico"],
#             x=list(range(1, len(resultado["historico"]) + 1)),
#             mode='lines+markers'
#         ))
#         fig.update_layout(
#             title="Evolução do custo ao longo das iterações",
#             xaxis_title="Iteração",
#             yaxis_title="Custo (R$)",
#             template="simple_white"
#         )
#         st.plotly_chart(fig, use_container_width=True)

#         # Tempo de execução
#         tempo_exec = resultado.get("tempo_execucao", None)
#         if tempo_exec is not None:
#             st.info(f"Tempo de execução do algoritmo: {tempo_exec:.2f} segundos")
#     else:
#         st.info("Configure os parâmetros e clique em 'Executar ACO' para visualizar o resultado.")









# import streamlit as st
# import pandas as pd
# from algoritmos.aco import run_aco
# import folium
# from streamlit_folium import st_folium
# import json
# import os
# import plotly.graph_objects as go
# import time

# def render():
#     st.header("Algoritmo de colônia de formigas (ACO)")

#     matriz_custos = pd.read_csv("dados/matriz_custos.csv", index_col=0)
#     cidades = matriz_custos.index.tolist()

#     idx_patrocinio = cidades.index("Patrocínio") if "Patrocínio" in cidades else 0
#     cidade_inicio = st.selectbox("Cidade inicial/final", cidades, index=idx_patrocinio)

#     st.subheader("Parâmetros do ACO")
#     n_formigas = st.number_input("Número de formigas", 1, 100, 20)
#     n_iter = st.number_input("Número de iterações", 10, 10000, st.session_state.get("max_iter", 1000), step=10)
#     alfa = st.slider("Alfa (peso do feromônio)", 0.1, 5.0, 1.0, 0.1)
#     beta = st.slider("Beta (peso da heurística)", 0.1, 10.0, 5.0, 0.1)
#     evaporacao = st.slider("Taxa de evaporação", 0.01, 1.0, 0.5, 0.01)

#     if st.button("Executar ACO"):
#         idx_inicio = cidades.index(cidade_inicio)
#         t0 = time.time()
#         resultado = run_aco(
#             matriz_custos,
#             n_formigas=n_formigas,
#             n_iter=n_iter,
#             alfa=alfa,
#             beta=beta,
#             evaporacao=evaporacao,
#             cidade_inicio=idx_inicio
#         )
#         t1 = time.time()
#         resultado["tempo_execucao"] = t1 - t0
#         st.session_state["aco_resultado"] = resultado

#     if "aco_resultado" in st.session_state:
#         resultado = st.session_state["aco_resultado"]
#         st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")
#         st.write(f"Custo total: R$ {resultado['custo']:.2f}")

#         # Visualização das três melhores rotas no mapa
#         with open("dados/municipios.json", encoding="utf-8") as f:
#             dados_cidades = json.load(f)
#         coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}

#         # Cores para as rotas
#         cores = ["blue", "red", "orange"]
#         m = None

#         # Criar um set para armazenar cidades já marcadas
#         cidades_marcadas = set()

#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             coordenadas = [coords_dict[nome] for nome in rota_info["rota"]]
#             if m is None:
#                 # Centro do mapa na cidade inicial
#                 lat_c, lng_c = coordenadas[0]
#                 m = folium.Map(location=[lat_c, lng_c], zoom_start=8)

#             # Adicionar linhas coloridas
#             folium.PolyLine(
#                 locations=coordenadas, 
#                 color=cores[idx % len(cores)], 
#                 weight=4, 
#                 opacity=0.7,
#                 tooltip=f"Rota #{idx+1}: Custo R$ {rota_info['custo']:.2f}"
#             ).add_to(m)

#             # Marcar as cidades apenas uma vez, com marker pequeno
#             for (lat, lng), nome in zip(coordenadas, rota_info["rota"]):
#                 if nome not in cidades_marcadas:
#                     folium.CircleMarker(
#                         location=[lat, lng],
#                         radius=5, # marcador menor
#                         color="black",
#                         fill=True,
#                         fill_color="yellow",
#                         fill_opacity=0.7,
#                         tooltip=nome
#                     ).add_to(m)
#                     cidades_marcadas.add(nome)

#         st_folium(m, width=800, height=500)

#         # Gráfico de evolução do custo
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             y=resultado["historico"],
#             x=list(range(1, len(resultado["historico"]) + 1)),
#             mode='lines+markers'
#         ))
#         fig.update_layout(
#             title="Evolução do custo ao longo das iterações",
#             xaxis_title="Iteração",
#             yaxis_title="Custo (R$)",
#             template="simple_white"
#         )
#         st.plotly_chart(fig, use_container_width=True)

#         # Exibição das métricas comparativas
#         tempo_exec = resultado.get("tempo_execucao", None)
#         if tempo_exec is not None:
#             st.info(f"Tempo de execução do algoritmo: {tempo_exec:.2f} segundos")
#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             st.markdown(f"**Rota #{idx+1}:** {' → '.join(rota_info['rota'])}")
#             st.write(f"Custo total: R$ {rota_info['custo']:.2f}")
#     else:
#         st.info("Configure os parâmetros e clique em 'Executar ACO' para visualizar o resultado.")







import streamlit as st
import pandas as pd
from algoritmos.aco import run_aco
import folium
from streamlit_folium import st_folium
import json
import os
import plotly.graph_objects as go
import time

def render():
    st.header("Algoritmo de colônia de formigas (ACO)")

    matriz_custos = pd.read_csv("dados/matriz_custos.csv", index_col=0)
    cidades = matriz_custos.index.tolist()

    idx_patrocinio = cidades.index("Patrocínio") if "Patrocínio" in cidades else 0
    cidade_inicio = st.selectbox("Cidade inicial/final", cidades, index=idx_patrocinio)

    st.subheader("Parâmetros do ACO")
    n_formigas = st.number_input("Número de formigas", 1, 100, 20)
    n_iter = st.number_input("Número de iterações", 10, 10000, st.session_state.get("max_iter", 1000), step=10)
    alfa = st.slider("Alfa (peso do feromônio)", 0.1, 5.0, 1.0, 0.1)
    beta = st.slider("Beta (peso da heurística)", 0.1, 10.0, 5.0, 0.1)
    evaporacao = st.slider("Taxa de evaporação", 0.01, 1.0, 0.5, 0.01)

    if st.button("Executar ACO"):
        idx_inicio = cidades.index(cidade_inicio)
        t0 = time.time()
        resultado = run_aco(
            matriz_custos,
            n_formigas=n_formigas,
            n_iter=n_iter,
            alfa=alfa,
            beta=beta,
            evaporacao=evaporacao,
            cidade_inicio=idx_inicio
        )
        t1 = time.time()
        resultado["tempo_execucao"] = t1 - t0
        st.session_state["aco_resultado"] = resultado

    if "aco_resultado" in st.session_state:
        resultado = st.session_state["aco_resultado"]
        st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")
        st.write(f"Custo total: R$ {resultado['custo']:.2f}")

        # Visualização das três melhores rotas no mapa com checkboxes
        with open("dados/municipios.json", encoding="utf-8") as f:
            dados_cidades = json.load(f)
        coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}

        # Emojis e cores para cada rota
        cores = ["blue", "red", "orange"]
        cores_emojis = ["🔵", "🔴", "🟠"]

        # Checkboxes para mostrar/ocultar rotas
        # mostrar_rotas = []
        # for idx, rota_info in enumerate(resultado.get("top_3", [])):
        #     checked = True if idx == 0 else False  # Exibe só a melhor rota por padrão
        #     label = f"{cores_emojis[idx]} Rota #{idx+1} (Custo: R$ {rota_info['custo']:.2f})"
        #     mostrar = st.checkbox(label, value=checked, key=f"rota_{idx+1}")
        #     mostrar_rotas.append(mostrar)
        # Cria 3 colunas para exibir os checkboxes na mesma linha
        colunas = st.columns(3)
        mostrar_rotas = []
        for idx, rota_info in enumerate(resultado.get("top_3", [])):
            checked = True if idx == 0 else False  # Exibe só a melhor rota por padrão
            label = f"{cores_emojis[idx]} Rota #{idx+1} (Custo: R$ {rota_info['custo']:.2f})"
            # Adiciona o checkbox na coluna correspondente
            with colunas[idx]:
                mostrar = st.checkbox(label, value=checked, key=f"rota_{idx+1}")
            mostrar_rotas.append(mostrar)

        m = None
        cidades_marcadas = set()

        for idx, rota_info in enumerate(resultado.get("top_3", [])):
            if not mostrar_rotas[idx]:
                continue  # Não desenha esta rota se não estiver marcada

            coordenadas = [coords_dict[nome] for nome in rota_info["rota"]]
            if m is None:
                # Centraliza o mapa na primeira rota exibida
                lat_c, lng_c = coordenadas[0]
                m = folium.Map(location=[lat_c, lng_c], zoom_start=8)

            # Adiciona linha colorida para a rota selecionada
            folium.PolyLine(
                locations=coordenadas,
                color=cores[idx % len(cores)],
                weight=4,
                opacity=0.7,
                tooltip=f"Rota #{idx+1}: Custo R$ {rota_info['custo']:.2f}"
            ).add_to(m)

            # Marca as cidades apenas uma vez
            for (lat, lng), nome in zip(coordenadas, rota_info["rota"]):
                if nome not in cidades_marcadas:
                    folium.CircleMarker(
                        location=[lat, lng],
                        radius=5,
                        color="black",
                        fill=True,
                        fill_color="yellow",
                        fill_opacity=0.7,
                        tooltip=nome
                    ).add_to(m)
                    cidades_marcadas.add(nome)

        if m:
            st_folium(m, width=800, height=500)
        else:
            st.info("Selecione pelo menos uma rota para visualizar o mapa.")

        # Gráfico de evolução do custo
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=resultado["historico"],
            x=list(range(1, len(resultado["historico"]) + 1)),
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Evolução do custo ao longo das iterações",
            xaxis_title="Iteração",
            yaxis_title="Custo (R$)",
            template="simple_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Exibição das métricas comparativas
        tempo_exec = resultado.get("tempo_execucao", None)
        if tempo_exec is not None:
            st.info(f"Tempo de execução do algoritmo: {tempo_exec:.2f} segundos")
        for idx, rota_info in enumerate(resultado.get("top_3", [])):
            st.markdown(f"**Rota #{idx+1}:** {' → '.join(rota_info['rota'])}")
            st.write(f"Custo total: R$ {rota_info['custo']:.2f}")
    else:
        st.info("Configure os parâmetros e clique em 'Executar ACO' para visualizar o resultado.")
