import streamlit as st
st.title("Bem vindo(a) à tela de cadastro")
nome = st.text_input("Digite seu nome: ")
email = st.text_input("Digite seu email: ") 
endereco = st.text_input("Digite seu endereço: ")
complemento = st.text_input("Digite o complemento do endereço: ")
bairro = st.text_input("Digite seu bairro: ")   
cidade = st.text_input("Digite sua cidade: ")
estado = st.text_input("Digite seu estado: ")
telefone = st.text_input("Digite seu telefone: ")
cpf = st.text_input("Digite seu CPF: ")
rg = st.text_input("Digite seu RG: ")
data_nascimento = st.text_input("Digite sua data de nascimento: ")
if st.button("Cadastrar"):
    if nome and email and endereco and complemento and bairro and cidade and estado and telefone and cpf and rg and data_nascimento:
        st.success("Cadastro realizado com sucesso!")
        with open("cadastros.csv", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{nome},{email},{endereco},{complemento},{bairro},{cidade},{estado},{telefone},{cpf},{rg},{data_nascimento}\n")
        st.success("Dados salvos no arquivo cadastros.csv")
    else:
        st.error("Por favor, preencha todos os campos para realizar o cadastro.")   


