
import streamlit as st

st.title("🚀 Painel de Consórcios")
st.markdown("---")
st.success("Módulo de Consórcios carregado com sucesso!")

# Área de simulação ou gestão de consórcios
st.subheader("Simulação de Lance")
valor_cota = st.number_input("Valor da Cota", min_value=0.0, format="%.2f")
lance_ofertado = st.number_input("Lance Ofertado (%)", min_value=0.0, max_value=100.0, format="%.2f")

if valor_cota > 0 and lance_ofertado > 0:
    valor_lance = valor_cota * (lance_ofertado / 100)
    st.write(f"💰 Valor do lance ofertado: R$ {valor_lance:,.2f}")
