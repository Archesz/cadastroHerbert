import streamlit as st
from io import BytesIO
import matplotlib.pyplot as plt
from background import getImage
from docx import Document

def create_word_document(file_path, nome, cpf, cep, num_casa, curso, periodo, identidade_genero, identidade_racial, institutos):
    # Criar um novo documento
    doc = Document()

    # Adicionar um título
    doc.add_heading('Contrato de Matrícula', level=1)

    # Adicionar informações do cabeçalho
    doc.add_paragraph(f"Nome Completo: {nome}")
    doc.add_paragraph(f"CPF: {cpf}")
    doc.add_paragraph(f"CEP: {cep}")
    doc.add_paragraph(f"Nº da Casa: {num_casa}")
    doc.add_paragraph(f"Curso: {curso}")
    doc.add_paragraph(f"Período: {periodo}")
    doc.add_paragraph(f"Identidade de Gênero: {identidade_genero}")
    doc.add_paragraph(f"Identidade Racial: {identidade_racial}")
    doc.add_paragraph(f"Institutos de Interesse: {', '.join(institutos)}")

    # Adicionar tópicos do contrato
    doc.add_heading('Termos do Contrato', level=2)
    doc.add_paragraph('Termo 1: ...')
    doc.add_paragraph('Termo 2: ...')
    # Adicione mais termos conforme necessário

    # Adicionar seção de assinatura
    doc.add_page_break()
    doc.add_paragraph('Assinatura do Aluno: ________________________')
    doc.add_paragraph('Data: ___/___/____')

    # Salvar o documento
    doc.save(file_path)


st.title("Cadastro Herbert")

nome = st.text_input("Nome Completo: ")

col1, col2, col3 = st.columns(3)

with col1:
    cpf = st.text_input("CPF:", max_chars=11)

with col2:
    cep = st.text_input("CEP:", max_chars=9)

with col3:
    num_casa = st.number_input("Nº: ", min_value=0, max_value=9999, )

curso = st.selectbox("Curso", ["Pré-Vestibular", "Pré-Técnico", "Concurso Público"])

periodos = ["Selecione o Período", "Matutino", "Vespertino", "Noturno"]

if curso == "Pré-Vestibular":
    periodos = ["Selecione o Período", "Matutino", "Vespertino", "Noturno"]
elif curso == "Pré-Técnico":
    periodos = ["Selecione o Período", "Matutino", "Vespertino", "Sábado"]
elif curso == "Concurso Público":
    periodos = ["Sábado"]

periodo = st.selectbox("Período", periodos)

photo = st.camera_input("Carometro")

if photo is not None:
    # Converter para imagem PIL
    photo_bytes = BytesIO(photo.getvalue())
    processed_image = getImage(photo_bytes)

    # Exibir a imagem ajustada

st.subheader("Informações CAD")

col4, col5 = st.columns(2)

with col4:
    genero = st.radio("**Como você se identifica**", ["Masculino", "Feminino", "Não Binário", "Outros"])

with col5:
    racial = st.radio("Como você se identifica", ["Negro/Negra", "Branco/Branca", "Pardo/Parda", "Amarelo/Amarela", "Indígena"])

instituicoes = st.multiselect("Quais institutos pretende prestar?", ["Unicamp", "USP", "Cotuca", "ETEC", "Instituto Federal", "Unesp", "Enem", "Cotil", "Particulares"])

cadastrar = st.button("Cadastrar")

if cadastrar:
    
    create_word_document("contrato.docx", nome, cpf, cep, num_casa, curso, periodo, genero, racial, instituicoes)

    if photo is not None:
        st.image(processed_image)

    st.success("Cadastrado com sucesso!")