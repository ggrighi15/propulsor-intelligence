import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Painel de Consórcios", layout="wide")

st.title("📄 Registro de Boletos e Comprovantes - Consórcios")

# Criar diretório de armazenamento, se não existir
os.makedirs("consorcios/uploads", exist_ok=True)

st.markdown("Faça o upload de boletos ou comprovantes em PDF, JPG ou PNG e registre o pagamento manualmente.")

# Upload
uploaded_file = st.file_uploader("📎 Selecione o comprovante", type=["pdf", "jpg", "jpeg", "png"])
grupo = st.text_input("Grupo")
cota = st.text_input("Cota")
data_pgto = st.date_input("Data de pagamento")
valor = st.number_input("Valor pago (R$)", min_value=0.0, step=0.01)
forma_pgto = st.selectbox("Forma de pagamento", ["Boleto", "PIX", "Transferência", "Outro"])

if st.button("Salvar registro"):
    if uploaded_file and grupo and cota and valor > 0:
        file_path = f"consorcios/uploads/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        novo = pd.DataFrame([{
            "Grupo": grupo,
            "Cota": cota,
            "Data": data_pgto,
            "Valor": valor,
            "Forma": forma_pgto,
            "Arquivo": uploaded_file.name
        }])
        # Salvar no CSV (poderia ser DB depois)
        csv_path = "consorcios/pagamentos.csv"
        if os.path.exists(csv_path):
            base = pd.read_csv(csv_path)
            base = pd.concat([base, novo], ignore_index=True)
        else:
            base = novo
        base.to_csv(csv_path, index=False)
        st.success("Pagamento registrado com sucesso.")
    else:
        st.warning("Preencha todos os campos obrigatórios.")

# Exibir registros e gráfico
st.subheader("📊 Pagamentos Registrados")
csv_path = "consorcios/pagamentos.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    filtro_grupo = st.selectbox("Filtrar por grupo", ["Todos"] + sorted(df["Grupo"].unique().tolist()))
    if filtro_grupo != "Todos":
        df = df[df["Grupo"] == filtro_grupo]
    st.dataframe(df)

    st.subheader("💰 Total por Grupo")
    st.bar_chart(df.groupby("Grupo")["Valor"].sum())
else:
    st.info("Nenhum pagamento registrado ainda.")
