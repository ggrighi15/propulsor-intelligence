
import streamlit as st
import os

st.set_page_config(page_title="Inteligência Propulsora", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🚀 Inteligência Propulsora</h1>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

def modulo(titulo, pasta, icone):
    if st.button(f"{icone} {titulo}", key=pasta):
        st.session_state["modulo"] = pasta

modulos = [
    ("Contencioso + Administrativo", "painel_contencioso", "💬"),
    ("Consórcios", "painel_consorcios", "🛰️"),
    ("Cadastro Pessoas", "cadastro_pessoas", "📂"),
    ("Contratos", "contratos", "📑"),
    ("Requisições", "requisicoes", "📋"),
    ("Societário", "societario", "🏛️"),
    ("Teacher Emma", "teacher_emma", "🧠"),
    ("Teliga Bot", "teliga_bot", "🛰️"),
    ("Teapruma Bot", "teapruma_bot", "💭"),
    ("Autopeças", "autoparts", "🔧"),
    ("Eva Pro", "eva_pro", "💬"),
]

cols = [col1, col2, col3]
for i, (titulo, pasta, icone) in enumerate(modulos):
    with cols[i % 3]:
        modulo(titulo, pasta, icone)

if "modulo" in st.session_state:
    pasta = st.session_state["modulo"]
    try:
        exec(open(f"{pasta}/streamlit_app.py").read())
    except Exception as e:
        st.error(f"Erro ao carregar o módulo {pasta}: {str(e)}")
