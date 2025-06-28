# Painel Visual CRM Propulsor – Pós-login (Cards de Módulos com Total de Registros)
# Gustavo: Visual moderno, pronto pra evoluir pra Streamlit ou Web (cards, cores, tudo pronto pra grid)

import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

# Lista de bancos de dados
BANCOS = [
    {'nome': 'Instituições', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/instituicoes.db'},
    {'nome': 'Pessoas', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/pessoas.db'},
    {'nome': 'Procurações', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/procuracoes.db'},
    {'nome': 'Requisições', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/requisicoes.db'},
    {'nome': 'Contencioso', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/contencioso.db'},
    {'nome': 'Contratos', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/contratos.db'},
    {'nome': 'Consórcios', 'path': r'C:/ulsor/propulsor-intelligence/propulsor-backend/database/consorcios.db'},
]

st.set_page_config(page_title="Painel Propulsor", layout="wide", page_icon="🚀")
st.title("Dashboard Propulsor – Visão Geral dos Módulos")

col1, col2, col3, col4 = st.columns(4)
cores_cards = ['#0866AD', '#19A367', '#F7B500', '#DB2330', '#7D2AE8', '#3B82F6', '#22D3EE']

cards = []

for idx, banco in enumerate(BANCOS):
    db_path = banco['path']
    nome = banco['nome']
    if not Path(db_path).exists():
        cards.append((nome, '-', 'Arquivo não encontrado'))
        continue
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' LIMIT 1;")
        t = cur.fetchone()
        if not t:
            cards.append((nome, '-', 'Nenhuma tabela'))
            conn.close()
            continue
        tabela = t[0]
        cur.execute(f'SELECT COUNT(*) FROM {tabela}')
        total = cur.fetchone()[0]
        conn.close()
        cards.append((nome, tabela, total))
    except Exception as e:
        cards.append((nome, '-', f'Erro: {e}"))

# Exibir cards visualmente bonitos
grids = [col1, col2, col3, col4]

for idx, (nome, tabela, total) in enumerate(cards):
    cor = cores_cards[idx % len(cores_cards)]
    with grids[idx % 4]:
        st.markdown(f"""
            <div style='background:linear-gradient(90deg,{cor},#fff1);border-radius:20px;padding:24px 18px 18px 18px;margin:10px 0;box-shadow:0 3px 18px #0002'>
            <div style='font-size:1.3em;font-weight:bold'>{nome}</div>
            <div style='color:#555;font-size:0.9em'>Tabela: <b>{tabela}</b></div>
            <div style='font-size:2.2em;font-weight:bold;margin-top:10px;color:{cor}'>{total}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('---')
st.write('Atualize os bancos .db para ver os dados em tempo real. Painel 100% pronto para integração e drilldown.')
