import streamlit as st
import os

st.set_page_config(
    page_title="Propulsor Intelligence",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Trebuchet MS', sans-serif !important;
    }
    .stButton > button {
        font-size: 18px;
        padding: 10px 20px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("Propulsor.png", width=180)
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 Inteligência Propulsora</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sistema Jurídico
with st.expander("⚖️ Sistema Jurídico", expanded=True):
    cols_juridico = st.columns(3)
    juridico_modulos = [
        ("Cadastro de Pessoas", "cadastro_pessoas", "📂"),
        ("Contencioso", "painel_contencioso", "📁"),
        ("Contratos", "contratos", "📁"),
        ("Requisições", "requisicoes", "📋"),
        ("Societário", "societario", "🏩")
    ]
    for i, (titulo, pasta, icone) in enumerate(juridico_modulos):
        with cols_juridico[i % 3]:
            if st.button(f"{icone} {titulo}", key=pasta):
                st.session_state["modulo"] = pasta

# Demais módulos
with st.expander("🧹 Outros Módulos", expanded=True):
    cols_outros = st.columns(3)
    outros_modulos = [
        ("Autopeças", "autoparts", "🔧"),
        ("Consórcios", "painel_consorcios", "🚀"),
        ("Eva Pro", "eva_pro", "💬"),
        ("Fui Trouxa, Agora Faturei", "fui_trouxa_agora_faturei", "💸"),
        ("Teacher Emma", "teacher_emma", "🧠"),
        ("Teliga Bot", "teliga_bot", "🚀"),
        ("Teapruma Bot", "teapruma_bot", "💭")
    ]
    for i, (titulo, pasta, icone) in enumerate(sorted(outros_modulos)):
        with cols_outros[i % 3]:
            if st.button(f"{icone} {titulo}", key=pasta):
                st.session_state["modulo"] = pasta

# Carregar módulo
if "modulo" in st.session_state:
    pasta = st.session_state["modulo"]
    try:
        exec(open(f"{pasta}/streamlit_app.py").read())
    except Exception as e:
        st.error(f"Erro ao carregar o módulo {pasta}: {str(e)}")

# Login e Integrações globais (se aplicável)
if os.path.exists("login/streamlit_app.py"):
    exec(open("login/streamlit_app.py").read())

if os.path.exists("integracoes/streamlit_app.py"):
    exec(open("integracoes/streamlit_app.py").read())
