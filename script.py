nome = input("Digite seu nome: ")

print(nome)

with open("nomes.csv", "a", encoding="utf-8") as arquivo:
    arquivo.write(f"Seja Bem vindo(a) {nome} \n")

print("Nome salvo no arquivo nomes.csv")    

import streamlit as st
st.title("Bem vindo(a) ao Streamlit")
st.write(f"Seja Bem vindo(a) {nome} ao Streamlit")  
st.balloons()
