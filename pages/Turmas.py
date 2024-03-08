import streamlit as st
import firebase_admin
import pandas as pd
from firebase_admin import db
import datetime
import plotly.express as px

st.title("Turmas")

firebase_admin.get_app()

# Função para carregar dados dos alunos do Firebase
def load_student_data():
    ref = db.reference('/students')
    students_dict = ref.get()
    if students_dict:
        students_df = pd.DataFrame(students_dict).T
        return students_df
    else:
        return pd.DataFrame()

def load_turmas():
    ref = db.reference("/turmas")
    salas_dict = ref.get()

    if salas_dict:
        students_df = pd.DataFrame(salas_dict).T
        return students_df
    else:
        return pd.DataFrame()

students_df = load_student_data()
turmas_df = load_turmas()

tab_1 , tab_2, tab_3, tab_4 = st.tabs(["Editar Turmas", "Criar Turma", "Visualizar Turmas", "Verificar Alunos"])

with tab_1:
    st.header("Turmas")

    ref = db.reference('/students')

    col1, col2, col3 = st.columns(3)

    with col1:
        curso = st.selectbox("Curso ", ["Pré-Vestibular", "Pré-Técnico", "Concurso Público"])
    with col2:
        periodo = st.selectbox("Periodo ", ["Matutino", "Vespertino", "Noturno", "Sábado"])

    students = students_df.query(f"curso == '{curso}' and periodo == '{periodo}' and Turma != 'Pixinguinha' and Turma != 'Dandara' and Turma != 'Laudelina'").reset_index()

    student_name = st.selectbox("Selecione o Estudante", students["nome"])
    sala = st.selectbox("Sala ", ["Laudelina", "Pixinguinha", "Dandara"])

    atribuir = st.button("Atribuir")
    
    if atribuir:

        students_data = {}
        keys = list(students["index"])
        names = list(students["nome"])

        for i in range(0, len(keys)):
            students_data[names[i]] = keys[i]

        key = students_data[student_name]
        ref.child(key).update({"Turma": sala})

        st.success("Atribuido")
        
with tab_2:
    st.header("Cadastrar Turma")

    data_atual = datetime.date.today()
    year = data_atual.year

    sala = st.selectbox("Sala", ["Laudelina", "Pixinguinha", "Dandara"])
    periodo = st.selectbox("Período", ["Selecione o periodo", "Matutino", "Vespertino", "Noturno", "Sábado"])
    curso = st.selectbox("Curso", ["Selecione o curso", "Pré-Vestibular", "Pré-Técnico", "Concurso Público"])

    btn_confirm = st.button("Criar Turma")

    if btn_confirm:
        ref = db.reference('/turmas')
        nome = f"{sala}_{curso}_{periodo}_{year}"
        try:
            exist = ref.order_by_child('Nome').equal_to(nome).get()
        except:
            exist = False

        if exist:
            st.warning("Sala já criada.")
        else:

            turma_data = {
                "Nome": nome,
                "Periodo": periodo,
                "Sala": sala,
                "Curso": curso,
                "Alunos": {},
                "Professores": {},
                "Horários": {}
            }

            ref.push(turma_data)
            st.success("Sala Criada.")

with tab_3:

    ref = db.reference('/students')
    students_df = load_student_data()

    periodo = st.selectbox("Selecione o Período", ["Matutino", "Vespertino", "Noturno", "Sábado"])
    curso = st.selectbox("Selecione o Curso", ["Pré-Vestibular", "Pré-Técnico", "Concurso Público"])

    students_df = students_df.query(f"periodo == '{periodo}' and curso == '{curso}'")
    turmas_count = students_df.value_counts("Turma").reset_index()
    turmas_count.columns = ["Turma", "Quantidade"]

    fig = px.bar(turmas_count, x="Turma", y="Quantidade")
    st.plotly_chart(fig)


with tab_4:
    periodo = st.selectbox("Escolha o Período", ["Matutino", "Vespertino", "Noturno", "Sábado"])
    curso = st.selectbox("Escolha o Curso", ["Pré-Vestibular", "Pré-Técnico", "Concurso Público"])
    turma = st.selectbox("Escolha a turma", ["Selecione", "Pixinguinha", "Laudelina", "Dandara"])

    if turma == "Selecione":
        df_not_turma = students_df.query(f"Turma != 'Pixinguinha' and Turma != 'Laudelina' and Turma != 'Dandara' and periodo == '{periodo}' and curso == '{curso}'")
    else:
        df_not_turma = students_df.query(f"Turma == '{turma}' and periodo == '{periodo}' and curso == '{curso}'")

    df_not_turma[["nome", "Turma", "periodo", "photo"]]
    
