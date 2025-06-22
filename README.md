# 🚚 Otimização de Rotas Logísticas com Algoritmos Bioinspirados (ACO & GA)

Este projeto implementa e compara algoritmos de **Colônia de Formigas (ACO)** e **Algoritmo Genético (GA)** aplicados ao problema de roteamento de veículos (VRP) sobre a malha realista de municípios do Alto Paranaíba/MG, utilizando dados atualizados de distância e tempo via **API do Google Maps**. Todo o sistema conta com interface gráfica interativa em **Streamlit**, permitindo fácil configuração, análise e visualização dos resultados em mapas interativos.

---

## **Funcionalidades**

- Configuração flexível de parâmetros dos algoritmos e dos custos.
- Atualização das matrizes de distância e tempo via Google Maps API.
- Visualização das melhores rotas no mapa com trajetos reais.
- Gráficos de evolução das soluções e análise estatística comparativa.
- Interface intuitiva totalmente em português.

---

## **Requisitos**

- Python 3.11 (recomendado)
- Conta Google Cloud com acesso à API Distance Matrix e Directions (Google Maps)
- Sistema operacional Windows (comando de ativação Powershell)

---

## **Instalação e Execução Local**

### 1. **Clone o repositório**

powershell:
git clone https://github.com/Luskinha04/Sistema-de-Log-stica-aplicando-o-ACO-e-AG
cd SEU_REPOSITORIO

### 2. **Crie e ative o ambiente virtual**
py -3.11 -m venv env
.\env\Scripts\Activate.ps11

### 3. **Instale as dependências**
pip install -r requirements.txt

### 4. **Configure as variáveis de ambiente**
Crie um arquivo chamado .env na raiz do projeto e insira sua chave da API do Google Maps:
GOOGLE_API_KEY= sua_chave_aqui

### 5. **Execute o projeto**
streamlit run main.py