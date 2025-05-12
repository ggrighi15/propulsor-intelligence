import streamlit as st
import os

st.set_page_config(page_title="Propulsor Intelligence", page_icon="🚀", layout="wide")
st.markdown("<h1 style='color:#00FF00;'>🚀 Inteligência Propulsora</h1>", unsafe_allow_html=True)

st.markdown("### Módulos Disponíveis:")
modules = [
    "cadastro_pessoas", "contencioso", "contratos", "societario", "procuracoes", "requisicoes",
    "consorcios", "familiar_gpt", "Teacher_Emma", "Eva_pro", "Teliga_bot", "Teapruma_bot",
    "financas_pessoais", "ciencia_dados", "data"
]

cols = st.columns(4)
for i, module in enumerate(modules):
    with cols[i % 4]:
        if st.button(f"📁 {module.replace('_', ' ').title()}"):
            os.system(f"streamlit run {module}/streamlit_app.py")
