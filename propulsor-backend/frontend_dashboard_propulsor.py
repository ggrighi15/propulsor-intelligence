import requests
import streamlit as st

# URL base da sua API Flask (ajuste para o endereço real em prod)
API_BASE = "http://localhost:5000"

st.set_page_config(page_title="Painel Propulsor - CRM Jurídico", layout="wide")
st.markdown("""
<style>
body, .stApp {background-color: #f6fbfe;}
.big-title {font-size: 2.4rem; font-weight: 800; color: #0081c9; margin-bottom: 1.5rem;}
.card {
    border-radius: 1.7rem; padding: 2.1rem 2rem; background: #fff;
    box-shadow: 0 2px 14px #0081c91a;
    margin: 0.9rem 0.9rem 1.2rem 0; display: flex; flex-direction: column; align-items: flex-start;
    min-width: 250px; max-width: 100%;
}
.card .label {font-size: 1.0rem; color: #848484; letter-spacing: 1.1px; font-weight: 600; text-transform: uppercase;}
.card .value {font-size: 2.6rem; font-weight: 700; margin: 0.4rem 0; color: #0081c9;}
.card .desc {font-size: 1.02rem; color: #6a6a6a;}
.card-green .value {color: #1bbc81;}
.card-red .value {color: #e95e5e;}
.card-yellow .value {color: #ffb400;}
.card-orange .value {color: #ff8220;}
.card-gray .value {color: #666;}
.card .error {color: #f00; font-weight: 600; font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">Painel Propulsor - Registros por Módulo</div>', unsafe_allow_html=True)

# Função para buscar dados da API Flask
def fetch_api(endpoint):
    try:
        resp = requests.get(API_BASE + endpoint, timeout=3)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {'erro': str(e)}

# Busca dados dos cards (dashboard)
data = fetch_api('/dashboard/cards')

cols = st.columns(4)

# Cards principais
modulos = [
    ("instituicoes", "INSTITUICOES", "Tabela: instituicoes", "card"),
    ("pessoas", "PESSOAS", "Tabela: pessoas", "card card-green"),
    ("procuracoes", "PROCURACOES", "Tabela: procuracoes", "card card-red"),
    ("requisicoes", "REQUISICOES", "Tabela: requisicoes", "card card-yellow"),
    ("contencioso", "CONTENCIOSO", "Tabela: contencioso mais recente", "card card-green"),
    ("contratos", "CONTRATOS", "Tabela: contratos", "card"),
    ("consorcios", "CONSORCIOS", "Tabela: consorcios", "card card-red"),
    ("depositos", "DEPOSITOS", "Tabela: depositos", "card card-gray"),
]

for i, (mod, label, desc, card_style) in enumerate(modulos):
    col = cols[i % 4]
    with col:
        st.markdown(f'<div class="{card_style}">', unsafe_allow_html=True)
        st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="desc">{desc}</div>', unsafe_allow_html=True)
        if data and mod in data:
            v = data[mod]
            # Trata erro textual (ex: contencioso pode dar erro de SQL)
            if isinstance(v, int):
                st.markdown(f'<div class="value">{v}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error">{v}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error">N/A</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Exibe histórico do contencioso
st.markdown('---')
st.subheader('Histórico de Contencioso - Todas as Tabelas')
hist = fetch_api('/contencioso/historico')
if hist and isinstance(hist, list):
    st.table([{"Tabela": h["tabela"], "Registros": h["total"]} for h in hist])
else:
    st.error('Não foi possível obter o histórico do contencioso.')

# Opções para futuro: detalhar cada módulo (listar registros), CRUD visual, filtros, etc.
