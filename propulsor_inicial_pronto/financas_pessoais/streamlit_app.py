import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Painel Financeiro - Propulsor", layout="wide")
st.title("Painel Financeiro - Propulsor")

db_path = "C:/Propulsor/propulsor-intelligence/data/db_financas.db"

def carregar_dados(tabela):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
    conn.close()
    return df

abas = st.tabs(["Transações", "Saldos", "Cartões", "Investimentos", "Empréstimos"])

with abas[0]:
    st.subheader("Transações")
    df = carregar_dados("transacoes")
    st.dataframe(df)
    st.metric("Total de Transações", len(df))
    st.metric("Valor Total", f"R$ {df['valor'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with abas[1]:
    st.subheader("Saldos")
    df = carregar_dados("saldos")
    st.dataframe(df)

with abas[2]:
    st.subheader("Cartões")
    df = carregar_dados("cartoes")
    st.dataframe(df)

with abas[3]:
    st.subheader("Investimentos")
    df = carregar_dados("investimentos")
    st.dataframe(df)

with abas[4]:
    st.subheader("Empréstimos")
    df = carregar_dados("emprestimos")
    st.dataframe(df)
