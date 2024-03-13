import streamlit as st
from io import BytesIO
# from background import getImage, remove_bg
from docx import Document
import datetime

import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage

def register_teacher(nome, disciplinas, cpf, telefone, turmas, periodos):
    
    firebase_admin.get_app()

    ref = db.reference('/teachers')

    teacher_data = {
        'nome': nome,
        'cpf': cpf,
        'telefone': telefone,
        'turmas': turmas,
        'periodos': periodos,
        'disciplinas': disciplinas,
        'horarios': {
            "Técnico": {
                "Matutino": {
                    "Segunda": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Terça": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Quarta": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Quinta": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Sexta": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    }
                },
                "Vespertino": {
                    "Segunda": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Terça": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Quarta": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Quinta": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Sexta": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    }
                },
                "Sábado": {
                    "Matutino": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False, 
                        "10:45 - 12:00": False,
                        "13:00 - 14:15": False,
                        "14:30 - 15:45": False,
                        "15:45 - 17:00": False
                    },
                },
            },
            "Vestibular": {
                "Matutino": {
                    "Segunda": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Terça": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Quarta": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Quinta": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    },
                    "Sexta": {
                        "08:00 - 09:15": False,
                        "09:30 - 10:45": False,
                        "10:45 - 12:00": False,
                    }
                },
                "Vespertino": {
                    "Segunda": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Terça": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Quarta": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Quinta": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    },
                    "Sexta": {
                        "14:00 - 15:15": False,
                        "15:30 - 16:45": False,
                        "16:45 - 18:00": False,
                    }
                },
                "Noturno": {
                    "Segunda": {
                        "19:00 - 20:05": False,
                        "20:20 - 21:25": False,
                        "21:25 - 22:30": False,
                    },
                    "Terça": {
                        "19:00 - 20:05": False,
                        "20:20 - 21:25": False,
                        "21:25 - 22:30": False,
                    },
                    "Quarta": {
                        "19:00 - 20:05": False,
                        "20:20 - 21:25": False,
                        "21:25 - 22:30": False,
                    },
                    "Quinta": {
                        "19:00 - 20:05": False,
                        "20:20 - 21:25": False,
                        "21:25 - 22:30": False,
                    },
                    "Sexta": {
                        "19:00 - 20:05": False,
                        "20:20 - 21:25": False,
                        "21:25 - 22:30": False,
                    }
                },
            },
        }
    }


    new_teacher_ref = ref.push(teacher_data)

    photo_url = upload_photo_to_storage(photo, cpf)  # Usando CPF como identificador único

    teacher_data['photo'] = photo_url
    new_teacher_ref.update({'photo': photo_url})


    return True

def upload_photo_to_storage(photo_bytes, teacher_id):
    firebase_admin.get_app()

    bucket = storage.bucket('herbert2024-be557.appspot.com')

    blob = bucket.blob(f'teacher_photos/{teacher_id}.jpg')

    blob.upload_from_string(photo_bytes.getvalue(), content_type='image/jpeg')

    blob.make_public()

    return blob.public_url

view = st.selectbox("", ["Cadastro", "Professores"])

if view == "Cadastro":

    st.title("Cadastro Professores Herbert")

    st.subheader("Dados Pessoais")

    nome = st.text_input("Nome Completo: ")

    disciplinas = st.multiselect("Disciplinas", ["Matemática", "Física", "Química", "Biologia", "História", "Geografia", "Sociologia", "Filosofia", "Gramática", "Redação", "Literatura"])

    col1, col2 = st.columns(2)

    with col1:
        cpf = st.text_input("CPF:", max_chars=11)    

    with col2:
        telefone = st.text_input("Whatsapp: ")

    photo = st.camera_input("Carometro")

    if photo is not None:
        photo_bytes = BytesIO(photo.getvalue())
    
    st.subheader("Dados Herbert")

    col6, col7 = st.columns(2)

    with col6:
        turmas = st.multiselect("Turmas", ["Pré-Vestibular", "Pré-Técnico", "Concurso Público"])

    periodos = ["Selecione o Período", "Matutino", "Vespertino", "Noturno", "Sábado"]

    with col7:
        periodo = st.multiselect("Período", periodos)


    cadastrar = st.button("Cadastrar")

    if cadastrar:

        registrar = register_teacher(nome, disciplinas, cpf, telefone, turmas, periodo)

        if registrar == True:
            st.success("Cadastrado com sucesso!")
        else:
            st.error("Não cadastrado. Erro.")

elif view == "Professores":
    def atualizar_horario(id_professor, turma, periodo, horarios):
        ref = db.reference(f'/teachers/{id_professor}/horarios/{turma}/{periodo}')
        ref.update(horarios)

    # Recupere todos os professores
    ref = db.reference('/teachers')
    professores = ref.get()

    # Lista para armazenar apenas os nomes dos professores e seus IDs
    nomes_professores = [{"nome": "Selecionar", "id": ""}]

    # Extrair os nomes e IDs dos professores
    if professores:
        for key, professor in professores.items():
            nomes_professores.append({"nome": professor['nome'], "id": key})

    # Exibir o selectbox com os nomes dos professores
    professor_selecionado = st.selectbox("Selecione um professor:", [professor['nome'] for professor in nomes_professores])

    # Obter o ID do professor selecionado
    id_professor_selecionado = next((professor['id'] for professor in nomes_professores if professor['nome'] == professor_selecionado), "")

    # Definir a ordem dos dias da semana
    ordem_dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

    if id_professor_selecionado:
        turma = st.selectbox("Seleciona a Turma: ", ["Vestibular", "Técnico", "Concurso"])
        periodo = st.selectbox("Selecione um periodo:", ["Matutino", "Vespertino", "Noturno", "Sábado"])

        horarios = professores[id_professor_selecionado]["horarios"][turma][periodo]

        st.write(f"Horários para {turma} - {periodo}:")

        # Exibir os horários na ordem desejada
        for dia in ordem_dias_semana:
            if dia in horarios:
                st.write(f"{dia}:")
                for horario_key, status in horarios[dia].items():
                    novo_status = st.checkbox(horario_key, value=status, key=f"{dia}-{horario_key}")
                    horarios[dia][horario_key] = novo_status

        if st.button("Salvar"):
            # Atualizar os dados no Firebase
            atualizar_horario(id_professor_selecionado, turma, periodo, horarios)
            st.success("Horários atualizados com sucesso!")
    else:
        st.write("Nenhum professor selecionado.")
