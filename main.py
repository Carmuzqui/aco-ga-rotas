# main.py

# Importa a biblioteca Streamlit para construção da interface web interativa
import streamlit as st

# Importa o componente de menu lateral com ícones
from streamlit_option_menu import option_menu

# Importa módulos do sistema operacional para manipulação de caminhos
import sys
import os

# Adiciona a pasta 'menu' ao caminho de importação para facilitar a importação dos módulos das páginas
sys.path.append(os.path.join(os.path.dirname(__file__), "menu"))

# Importa cada página da aplicação (parâmetros, algoritmos, comparação, sobre)
import parametros
import aco
import ga
import comparacao

# Configuração inicial da página Streamlit (título, layout e ícone)
st.set_page_config(
    page_title="Otimização de rotas",
    layout="wide",
    page_icon="🚚"
)

# Define as opções e ícones do menu lateral
menu_options = [
    "Início",
    "Parâmetros",
    "🐜 ACO",
    "🧬 GA",
    "Comparação",    
]
menu_icons = [
    "house", "gear", "transparency", "transparency", "bar-chart"
]
MENU_KEY = "menu_selected_option"

# Define a opção de menu ativa na sessão do usuário
if MENU_KEY not in st.session_state:
    st.session_state[MENU_KEY] = menu_options[0]
active_page = st.session_state[MENU_KEY]

# Cria o menu lateral com as opções e ícones definidos
with st.sidebar:
    st.title("🚚 Otimização de rotas")
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=menu_options.index(active_page),
        key=MENU_KEY,
        orientation="vertical"
    )

# Renderiza cada página de acordo com a seleção do usuário no menu lateral
if selected == "Início":
    st.markdown("""
    <div style="display:flex;align-items:center;">
        <span style="font-size:3rem; margin-right:1rem;">🚚</span>
        <h1 style="display:inline;">Sistema de Otimização de Rotas</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <br>
    <h3 style="color:#2c3e50;">Bem-vindo!</h3>
    <p style="font-size:1.1rem;">
        Este sistema foi desenvolvido com objetivo acadêmico para comparar técnicas de inteligência computacional aplicadas ao <b>problema de roteamento de veículos (VRP)</b>, utilizando:
        <ul>
            <li><b>Colônia de formigas (ACO))</b>: inspiração no comportamento coletivo das formigas para encontrar rotas eficientes.</li>
            <li><b>Algoritmo genético (GA))</b>: baseado nos princípios da evolução e seleção natural.</li>
        </ul>
        Explore as abas no menu lateral para definir os parâmetros, rodar cada algoritmo e comparar seus desempenhos em múltiplos cenários.<br><br>
        <b>Funcionalidades principais:</b>
        <ul>
            <li>Configuração flexível de parâmetros de simulação</li>
            <li>Visualização interativa das melhores rotas no mapa</li>
            <li>Gráficos comparativos de custo, distância e tempo</li>
            <li>Análise estatística de múltiplas execuções</li>
        </ul>
    </p>
    """, unsafe_allow_html=True)

elif selected == "Parâmetros":
    parametros.render()

elif selected == "🐜 ACO":
    aco.render()

elif selected == "🧬 GA":
    ga.render()

elif selected == "Comparação":
    comparacao.render()

else:
    st.error("Página não reconhecida.")
