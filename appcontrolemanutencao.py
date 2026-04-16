import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Controle de Manutenção Veicular", layout="wide")

DATA_FILE = "manutencao_veiculos.csv"

# Carregar dados
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "Data",
        "KM Atual",
        "Peça Trocada",
        "Valor Peça",
        "Local",
        "Mão de Obra",
        "Próxima Troca",
        "Observação"
    ])

st.title("🚗 Controle de Manutenção Veicular")

menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Consultar"])

# ================= CADASTRO =================
if menu == "Cadastrar":
    st.header("📋 Registrar Manutenção")

    with st.form("form_manutencao"):
        col1, col2 = st.columns(2)

        with col1:
            data = st.date_input("Data", value=date.today())
            km = st.number_input("KM Atual", min_value=0)
            peca = st.text_input("Peça Trocada")
            valor_peca = st.number_input("Valor da Peça (R$)", min_value=0.0, format="%.2f")

        with col2:
            local = st.text_input("Onde foi adquirida")
            mao_obra = st.number_input("Valor da Mão de Obra (R$)", min_value=0.0, format="%.2f")
            proxima = st.text_input("Previsão Próxima Troca (ex: 10.000 km ou data)")
            obs = st.text_area("Observação")

        submit = st.form_submit_button("Salvar")

        if submit:
            novo = pd.DataFrame([[data, km, peca, valor_peca, local, mao_obra, proxima, obs]],
                                columns=df.columns)

            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.success("Registro salvo com sucesso!")

# ================= CONSULTA =================
if menu == "Consultar":
    st.header("🔍 Histórico de Manutenções")

    if df.empty:
        st.warning("Nenhum registro encontrado.")
    else:
        # Filtros
        st.subheader("Filtros")
        col1, col2 = st.columns(2)

        with col1:
            filtro_peca = st.text_input("Filtrar por peça")
        with col2:
            filtro_km = st.number_input("KM mínimo", min_value=0, value=0)

        df_filtrado = df.copy()

        if filtro_peca:
            df_filtrado = df_filtrado[df_filtrado["Peça Trocada"].str.contains(filtro_peca, case=False, na=False)]

        df_filtrado = df_filtrado[df_filtrado["KM Atual"] >= filtro_km]

        st.dataframe(df_filtrado, use_container_width=True)

        # Métricas
        st.subheader("📊 Resumo")
        total_pecas = df_filtrado["Valor Peça"].sum()
        total_mao_obra = df_filtrado["Mão de Obra"].sum()
        total_geral = total_pecas + total_mao_obra

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Peças", f"R$ {total_pecas:.2f}")
        col2.metric("Total Mão de Obra", f"R$ {total_mao_obra:.2f}")
        col3.metric("Total Geral", f"R$ {total_geral:.2f}")

        # Download
        st.download_button(
            label="📥 Baixar dados em CSV",
            data=df.to_csv(index=False),
            file_name="manutencao_veiculos.csv",
            mime="text/csv"
        )

st.sidebar.info("App desenvolvido para controle de manutenção veicular")
