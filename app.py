
import os
import streamlit.web.bootstrap

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    streamlit.web.bootstrap.run("app.py", "", [], port=port)
# Configuração inicial da página
st.set_page_config(
    page_title="Propulsor Intelligence",
    layout="wide",
    page_icon="🚀"
)

# Estilo visual personalizado com as cores Ulsor
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Trebuchet MS', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #002e5d;
        }
        .css-1d391kg {  /* Título */
            color: #e30613;
        }
        h1, h2, h3, h4 {
            color: #002e5d !important;
        }
        .stButton>button {
            background-color: #1dd3f8;
            color: #fff;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.image("Propulsor.png", width=180)
st.title("Propulsor Intelligence – Painel Geral")
st.markdown("---")

# Lista de módulos com descrição
modulos = {
    "painel_familiar_gpt": "👨‍👩‍👧 Painel Familiar GPT – Controle e suporte da IA para sua família.",
    "consorcios": "📊 Consórcios – Análise de propostas e monitoramento de grupos.",
    "outro": "🧪 Módulo de Testes – Scripts diversos para integração e protótipos."
}

# Menu lateral com nomes descritivos
opcao = st.sidebar.radio("Selecione o Módulo", list(modulos.keys()))

# Exibir descrição na área principal
st.subheader(modulos[opcao])
st.markdown("---")

# Execução do módulo correspondente
try:
    exec(open(f"{opcao}/streamlit_app.py").read())
except Exception as e:
    st.error(f"❌ Erro ao carregar o módulo `{opcao}`:\n\n{str(e)}")
