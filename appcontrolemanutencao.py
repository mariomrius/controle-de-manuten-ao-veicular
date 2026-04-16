import streamlit as st
import pandas as pd
from datetime import date, datetime
import sqlite3
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Controle de Manutenção PRO", layout="wide")

# ================= BANCO DE DADOS =================
conn = sqlite3.connect("manutencao.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS manutencao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    veiculo TEXT,
    data TEXT,
    km INTEGER,
    peca TEXT,
    valor_peca REAL,
    local TEXT,
    mao_obra REAL,
    proxima TEXT,
    obs TEXT,
    nota TEXT
)
""")
conn.commit()

# ================= LOGIN SIMPLES =================
st.sidebar.title("🔐 Login")
usuario = st.sidebar.text_input("Usuário")
senha = st.sidebar.text_input("Senha", type="password")

if usuario != "admin" or senha != "123":
    st.warning("Faça login para continuar")
    st.stop()

st.title("🚗 Controle de Manutenção Veicular PRO")

menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Consultar"])

# ================= CADASTRO =================
if menu == "Cadastrar":
    st.header("📋 Registrar Manutenção")

    with st.form("form"):
        col1, col2 = st.columns(2)

        with col1:
            veiculo = st.text_input("Veículo")
            data = st.date_input("Data", value=date.today())
            km = st.number_input("KM Atual", min_value=0)
            peca = st.text_input("Peça Trocada")
            valor_peca = st.number_input("Valor Peça", min_value=0.0)

        with col2:
            local = st.text_input("Local")
            mao = st.number_input("Mão de Obra", min_value=0.0)
            proxima = st.text_input("Próxima Troca (KM ou Data)")
            obs = st.text_area("Observação")
            nota = st.file_uploader("Upload Nota Fiscal")

        salvar = st.form_submit_button("Salvar")

        if salvar:
            nota_nome = None
            if nota:
                nota_nome = nota.name
                with open(nota.name, "wb") as f:
                    f.write(nota.getbuffer())

            c.execute("""
                INSERT INTO manutencao (usuario, veiculo, data, km, peca, valor_peca, local, mao_obra, proxima, obs, nota)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (usuario, veiculo, str(data), km, peca, valor_peca, local, mao, proxima, obs, nota_nome))
            conn.commit()

            st.success("Salvo com sucesso")

# ================= CONSULTA =================
if menu == "Consultar":
    st.header("🔎 Histórico")

    df = pd.read_sql_query("SELECT * FROM manutencao WHERE usuario=?", conn, params=(usuario,))

    if df.empty:
        st.warning("Sem dados")
    else:
        veiculo_filtro = st.selectbox("Filtrar veículo", ["Todos"] + list(df["veiculo"].unique()))

        if veiculo_filtro != "Todos":
            df = df[df["veiculo"] == veiculo_filtro]

        st.dataframe(df)

        # ALERTA AUTOMÁTICO
        st.subheader("🔔 Alertas")
        for _, row in df.iterrows():
            if "km" in str(row["proxima"]).lower():
                try:
                    limite = int(''.join(filter(str.isdigit, str(row["proxima"]))))
                    if row["km"] >= limite:
                        st.error(f"Troca pendente: {row['peca']} no veículo {row['veiculo']}")
                except:
                    pass

        # PDF
        if st.button("Gerar Relatório PDF"):
            doc = SimpleDocTemplate("relatorio.pdf")
            styles = getSampleStyleSheet()
            elementos = []

            for _, row in df.iterrows():
                texto = f"{row['veiculo']} - {row['peca']} - R$ {row['valor_peca']}"
                elementos.append(Paragraph(texto, styles['Normal']))

            doc.build(elementos)

            with open("relatorio.pdf", "rb") as f:
                st.download_button("Baixar PDF", f, file_name="relatorio.pdf")

        total = df["valor_peca"].sum() + df["mao_obra"].sum()
        st.metric("Total Gasto", f"R$ {total:.2f}")

st.sidebar.success("Sistema PRO ativo")
