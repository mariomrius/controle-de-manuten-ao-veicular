import streamlit as st
st.title("Bem vindo(a) ao Streamlit")
nome = st.text_input("Digite seu nome: ")
if nome:
    st.write(f"Seja Bem vindo(a) {nome} ao Streamlit")  
    with open("nomes.csv", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Seja Bem vindo(a) {nome} \n")
    st.success("Nome salvo no arquivo nomes.csv")
    st.balloons()               

    st.button("Clique aqui para celebrar!", on_click=lambda: st.balloons()) 
    st.write("Obrigado por usar o Streamlit!")  
    
    