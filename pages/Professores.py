import streamlit as st
from io import BytesIO
from background import getImage, remove_bg
from docx import Document
import datetime

import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage

firebase_admin.get_app()

def upload_photo_to_storage(photo_bytes, student_id):
    firebase_admin.get_app()

    bucket = storage.bucket('herbert2024-be557.appspot.com')

    blob = bucket.blob(f'teacher_photos/{student_id}.jpg')

    blob.upload_from_string(photo_bytes.getvalue(), content_type='image/jpeg')

    blob.make_public()

    return blob.public_url

def register_teacher_to_firebase(nome, cpf, nascimento, telefone, email, disciplinas, periodos, photo=None):
    data_atual = datetime.date.today()
    ano_atual = data_atual.year
    # Verifica se o CPF já está cadastrado
    
    ref = db.reference('/teachers')


    student_data = {
        'nome': nome,
        'cpf': cpf,
        'nascimento': str(nascimento),
        'telefone': telefone,
        'email': email,
        'ano': ano_atual,
        'disciplinas': disciplinas,
        'periodos': periodos
    }
    firebase_admin.get_app()

    # Envia os dados para o Firebase
    new_student_ref = ref.push(student_data)

    if photo is not None:
        photo_url = upload_photo_to_storage(photo, cpf)  # Usando CPF como identificador único
        student_data['photo'] = photo_url
        new_student_ref.update({'photo': photo_url})

    return True


st.title("Cadastro Professor Herbert")

st.subheader("Dados Pessoais")

nome_prof = st.text_input("Nome Completo: ")

col1, col2, col3 = st.columns(3)

with col1:
    cpf_prof = st.text_input("CPF:", max_chars=11)
    
with col2:
    nascimento_prof = st.date_input("Data de Nascimento: ", format="DD/MM/YYYY")

with col3:
    telefone_prof = st.text_input("Whatsapp: ")

email_prof = st.text_input("Email: ")

st.subheader("Dados Herbert")

disciplinas_prof = st.multiselect("Selecione a Disciplia: ", ["Matemática", "Física", "Química", "Biologia", "História", "Geografia", "Sociologia", "Filosofia", "Gramática", "Redação", "Literatura", "Inglês"])

col6, col7 = st.columns(2)

with col6:
    curso_prof = st.multiselect("Curso", ["Pré-Vestibular", "Pré-Técnico", "Concurso Público"])

periodos = ["Quais Períodos irá lecionar?", "Matutino", "Vespertino", "Noturno", "Sábado"]

with col7:
    periodo_prof = st.multiselect("Período", periodos)

st.subheader("Identificação")

photo_prof = st.camera_input("Carometro")

if photo_prof is not None:
    photo_bytes = BytesIO(photo_prof.getvalue())
    processed_image = remove_bg(photo_bytes)

cadastrar_prof = st.button("Cadastrar")

if cadastrar_prof:
    
    # docx_buffer = create_word_document(".", nome, cpf, cep, num_casa, curso, periodo, genero, racial, instituicoes)
    registrar = register_teacher_to_firebase(nome_prof, cpf_prof, nascimento_prof, telefone_prof, email_prof, disciplinas_prof, periodo_prof, processed_image)

    if photo_prof is not None:
        st.image(processed_image)

    st.success("Cadastrado com sucesso!")