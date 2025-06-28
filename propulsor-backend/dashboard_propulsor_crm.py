import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import json

# Caminhos dos bancos - podem ser variáveis de ambiente no .env em produção
BANCOS = {
    "Pessoas": "database/pessoas.db",
    "Contratos": "database/contratos.db",
    "Instituições": "database/instituicoes.db",
    "Procuracoes": "database/procuracoes.db",
    "Depositos": "database/depositos.db",
    "Consorcios": "database/consorcios.db",
    "Contencioso": "database/contencioso.db",
    "Usuarios": "database/usuarios.db",
    "Requisicoes": "database/requisicoes.db",
}

# Carrega a paleta do Propulsor
try:
    with open("static/cores.json", encoding="utf-8") as f:
        PALETA = json.load(f)
except Exception:
    PALETA = {
        "primaria": "#254d81",
        "secundaria": "#1ab0c7",
        "terciaria": "#eaeaea",
        "destaque": "#f9c000",
        "alerta": "#e64a19"
    }

st.set_page_config(page_title="CRM Propulsor", layout="wide")

# Header visual
def logo_header():
    col1, col2 = st.columns([1,10])
    with col1:
        st.image("static/Logo.png", width=68)
    with col2:
        st.markdown(f"""
            <h1 style='color:{PALETA['primaria']};margin-bottom:0;'>Propulsor CRM</h1>
            <div style='font-size:18px;color:{PALETA['secundaria']};margin-top:0;'>Gestão Jurídica • Contencioso • Comercial</div>
        """, unsafe_allow_html=True)
logo_header()
st.markdown("---")

# Cards principais - contagem de registros
def contar_registros(banco, tabela):
    if not Path(banco).exists():
        return 0
    try:
        conn = sqlite3.connect(banco)
        cur = conn.cursor()
        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC")
        tabelas = [x[0] for x in cur.fetchall()]
        # Se for contencioso, pega a tabela mais nova
        if tabela == "Contencioso":
            if tabelas:
                tab_mais_nova = sorted(tabelas)[-1]
                cur.execute(f"SELECT COUNT(*) FROM '{tab_mais_nova}'")
                total = cur.fetchone()[0]
                conn.close()
                return total
            return 0
        else:
            cur.execute(f"SELECT COUNT(*) FROM {tabelas[0]}")
            total = cur.fetchone()[0]
            conn.close()
            return total
    except Exception as e:
        return f"Erro: {e}"

def exibe_cards():
    st.markdown(f"<div style='display: flex; gap:20px;'>", unsafe_allow_html=True)
    for nome, banco in BANCOS.items():
        cor = PALETA['primaria'] if nome != 'Contencioso' else PALETA['alerta']
        qtd = contar_registros(banco, nome)
        st.markdown(f"""
        <div style='background:{cor};color:#fff;padding:24px 32px;border-radius:16px;box-shadow:0 2px 8px #0001;min-width:160px;display:inline-block;text-align:center;'>
            <div style='font-size:32px;font-weight:bold;'>{qtd}</div>
            <div style='font-size:16px;margin-top:4px;'>{nome}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
exibe_cards()

# Dashboard visual básico
def dash_visual():
    aba = st.sidebar.selectbox(
        "Acessar módulo:", list(BANCOS.keys()), index=0
    )
    banco = BANCOS[aba]
    if not Path(banco).exists():
        st.error("Banco não localizado!")
        return
    conn = sqlite3.connect(banco)
    tabelas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC", conn)
    tabela_ativa = tabelas['name'][0]
    df = pd.read_sql_query(f"SELECT * FROM '{tabela_ativa}' LIMIT 300", conn)
    st.markdown(f"### {aba}")
    st.dataframe(df)
    conn.close()
dash_visual()

st.markdown(f"""<div style='text-align:right;font-size:12px;margin-top:60px;color:#aaa;'>Propulsor &copy; 2025</div>""", unsafe_allow_html=True)
