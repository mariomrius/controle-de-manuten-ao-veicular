import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Controle de Manutenção Veicular", layout="wide")

DATA_FILE = "manutencao_veiculos.csv"

# ================= FUNÇÕES =================
def carregar_dados():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, dtype=str)
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

    # 🔥 força tudo como string (resolve o erro)
    df = df.astype(str)

    return df

def salvar_dados(df):
    df = df.astype(str)
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
            proxima = st.text_input("Próxima Troca")
            obs = st.text_area("Observação")

        submit = st.form_submit_button("Salvar")

        if submit:
            novo = pd.DataFrame([[str(data), str(km), str(peca), str(valor_peca), str(local), str(mao_obra), str(proxima), str(obs)]],
                    columns=df.columns)
            
            df = pd.concat([df, novo], ignore_index=True)
            salvar_dados(df)

            st.success("Registro salvo com sucesso!")
            st.rerun()

# ================= CONSULTA / EDIÇÃO =================
if menu == "Consultar / Editar":
    st.header("🔍 Histórico de Manutenções")

    if df.empty:
        st.warning("Nenhum registro encontrado.")
    else:
        df = df.reset_index(drop=True)
        df_exibir = df.copy()
        df_exibir["ID"] = df_exibir.index

        st.dataframe(df_exibir, use_container_width=True)

        st.subheader("✏️ Editar ou Excluir")

        id_selecionado = st.number_input(
            "Digite o ID", 
            min_value=0, 
            max_value=len(df_exibir)-1, 
            step=1
        )

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

        # ✅ ATUALIZAR (CORRIGIDO)
        with col_btn1:
            if st.button("💾 Atualizar"):
                df.at[id_selecionado, "Data"] = str(data)
                df.at[id_selecionado, "KM Atual"] = str(km)
                df.at[id_selecionado, "Peça Trocada"] = str(peca)
                df.at[id_selecionado, "Valor Peça"] = str(valor_peca)
                df.at[id_selecionado, "Local"] = str(local)
                df.at[id_selecionado, "Mão de Obra"] = str(mao)
                df.at[id_selecionado, "Próxima Troca"] = str(proxima)
                df.at[id_selecionado, "Observação"] = str(obs)

                salvar_dados(df)
                st.success("Atualizado com sucesso!")
                st.rerun()

        # ✅ EXCLUIR (CORRIGIDO)
        with col_btn2:
            if st.button("🗑️ Excluir"):
                df = df.drop(id_selecionado).reset_index(drop=True)
                salvar_dados(df)
                st.success("Excluído com sucesso!")
                st.rerun()

        # ================= RESUMO =================
        st.subheader("📊 Resumo")

        total_pecas = pd.to_numeric(df["Valor Peça"], errors='coerce').sum()
        total_mao = pd.to_numeric(df["Mão de Obra"], errors='coerce').sum()
        total = total_pecas + total_mao

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Peças", f"R$ {total_pecas:.2f}")
        col2.metric("Mão de Obra", f"R$ {total_mao:.2f}")
        col3.metric("Total Geral", f"R$ {total:.2f}")

        # ================= DOWNLOAD =================
        st.download_button(
            "📥 Baixar CSV",
            df.to_csv(index=False),
            "manutencao_veiculos.csv",
            "text/csv"
        )

st.sidebar.info("Sistema com edição e exclusão funcionando")