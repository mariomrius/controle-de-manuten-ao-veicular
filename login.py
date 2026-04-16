nçetflix:///
çimport streamlit as st
st.title("Sistema de Login")
username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")
if st.button("Login"):
    if username == "admin" and password == "1234":
        st.success("Login bem-sucedido!")
    else:
        st.error("Usuário ou senha incorretos.")    
