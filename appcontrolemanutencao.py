import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Controle de Manutenção Veicular", layout="wide")

DATA_FILE = "manutencao_veiculos.csv"

# ================= FUNÇÕES =================

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Data",
            "KM Atual",
            "Peça Trocada",
            "Valor Peça",
            "Local",
            "Mão de Obra",
            "Próxima Troca",
            "Observação"
        ])


def salvar_dados(df):
    df.to_csv(DATA_FILE, index=False)


# ================= APP =================

df = carregar_dados()

st.title("🚗 Controle de Manutenção Veicular")

menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Consultar / Editar"])

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
            proxima = st.text_input("Previsão Próxima Troca")
            obs = st.text_area("Observação")

        submit = st.form_submit_button("Salvar")

        if submit:
            novo = pd.DataFrame([[data, km, peca, valor_peca, local, mao_obra, proxima, obs]],
                                columns=df.columns)

            df = pd.concat([df, novo], ignore_index=True)
            salvar_dados(df)

            st.success("Registro salvo com sucesso!")

# ================= CONSULTA / EDIÇÃO =================
if menu == "Consultar / Editar":
    st.header("🔍 Histórico de Manutenções")

    if df.empty:
        st.warning("Nenhum registro encontrado.")
    else:
        df_reset = df.reset_index()
        df_reset.rename(columns={"index": "ID"}, inplace=True)

        st.dataframe(df_reset, use_container_width=True)

        st.subheader("✏️ Editar ou Excluir Registro")

        id_selecionado = st.number_input("Digite o ID do registro", min_value=0, max_value=len(df_reset)-1, step=1)

        if id_selecionado is not None and id_selecionado < len(df):
            registro = df.loc[id_selecionado]

            col1, col2 = st.columns(2)

            with col1:
                data = st.date_input("Data", value=pd.to_datetime(registro["Data"]))
                km = st.number_input("KM Atual", value=int(registro["KM Atual"]))
                peca = st.text_input("Peça", value=registro["Peça Trocada"])
                valor_peca = st.number_input("Valor Peça", value=float(registro["Valor Peça"]))

            with col2:
                local = st.text_input("Local", value=registro["Local"])
                mao = st.number_input("Mão de Obra", value=float(registro["Mão de Obra"]))
                proxima = st.text_input("Próxima Troca", value=registro["Próxima Troca"])
                obs = st.text_area("Observação", value=registro["Observação"])

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                if st.button("💾 Atualizar"):
                    df.loc[id_selecionado] = [data, km, peca, valor_peca, local, mao, proxima, obs]
                    salvar_dados(df)
                    st.success("Registro atualizado com sucesso!")

            with col_btn2:
                if st.button("🗑️ Excluir"):
                    df = df.drop(id_selecionado).reset_index(drop=True)
                    salvar_dados(df)
                    st.success("Registro excluído com sucesso!")

        # RESUMO
        st.subheader("📊 Resumo")
        total_pecas = df["Valor Peça"].sum()
        total_mao_obra = df["Mão de Obra"].sum()
        total_geral = total_pecas + total_mao_obra

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Peças", f"R$ {total_pecas:.2f}")
        col2.metric("Total Mão de Obra", f"R$ {total_mao_obra:.2f}")
        col3.metric("Total Geral", f"R$ {total_geral:.2f}")

        # DOWNLOAD
        st.download_button(
            label="📥 Baixar dados em CSV",
            data=df.to_csv(index=False),
            file_name="manutencao_veiculos.csv",
            mime="text/csv"
        )

st.sidebar.info("App com edição e exclusão de registros")
