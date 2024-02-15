import streamlit as st
from io import BytesIO
# from background import getImage, remove_bg
from docx import Document
import datetime

import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage
import pandas as pd

# FUNÇÕES

# Definir a classe Professor
class Professor():
    def __init__(self, nome, disciplinas, horarios, periodos, turmas):
        self.nome = nome
        self.disciplinas = disciplinas
        self.horarios = horarios
        self.periodos = periodos
        self.turmas = turmas

def organizar_disponibilidade(profs, periodo):
    disponiveis = [prof for prof in profs if periodo in prof.periodos]
    disponibilidade_professores = []

    for professor in disponiveis:
        disponibilidade = sum(horario == False for turmas in professor.horarios.values() 
                                               for periodos in turmas.values() 
                                               for dias in periodos.values() 
                                               for horario in dias.values())
        disponibilidade_professores.append((professor, disponibilidade))

    professores_ordenados = sorted(disponibilidade_professores, key=lambda x: x[1])

    return [professor[0] for professor in professores_ordenados][::-1]

def montarHorarios(professores, turma, periodo):
    
    if turma == "Vestibular":
      qnt_materia_semana = {
          "Matemática": 2,
          "Química": 2,
          "Física": 2,
          "Biologia": 2,
          "Geografia": 2,
          "História": 2,
          "Socio/Filo": 1,
          "Literatura": 1,
          "Gramática": 1
      }

    # Definindo os horários iniciais para o período matutino
    periodos = {
        "Matutino": {
            "Segunda": {"08:00 - 09:15": "", "09:30 - 10:45": "", "10:45 - 12:00": ""},
            "Terça": {"08:00 - 09:15": "", "09:30 - 10:45": "", "10:45 - 12:00": ""},
            "Quarta": {"08:00 - 09:15": "", "09:30 - 10:45": "", "10:45 - 12:00": ""},
            "Quinta": {"08:00 - 09:15": "", "09:30 - 10:45": "", "10:45 - 12:00": ""},
            "Sexta": {"08:00 - 09:15": "", "09:30 - 10:45": "", "10:45 - 12:00": ""}
        },
        "Vespertino": {
            "Segunda": {"14:00 - 15:15": "", "15:30 - 16:45": "", "16:45 - 18:00": ""},
            "Terça": {"14:00 - 15:15": "", "15:30 - 16:45": "", "16:45 - 18:00": ""},
            "Quarta": {"14:00 - 15:15": "", "15:30 - 16:45": "", "16:45 - 18:00": ""},
            "Quinta": {"14:00 - 15:15": "", "15:30 - 16:45": "", "16:45 - 18:00": ""},
            "Sexta": {"14:00 - 15:15": "", "15:30 - 16:45": "", "16:45 - 18:00": ""}
        },
        "Noturno": {
            "Segunda": {"19:00 - 20:05": "", "20:20 - 21:25": "", "21:25 - 22:30": ""},
            "Terça": {"19:00 - 20:05": "", "20:20 - 21:25": "", "21:25 - 22:30": ""},
            "Quarta": {"19:00 - 20:05": "", "20:20 - 21:25": "", "21:25 - 22:30": ""},
            "Quinta": {"19:00 - 20:05": "", "20:20 - 21:25": "", "21:25 - 22:30": ""},
            "Sexta": {"19:00 - 20:05": "", "20:20 - 21:25": "", "21:25 - 22:30": ""}
        }
    }

    profs = organizar_disponibilidade(professores, periodo)
    
    horarios = periodos[periodo] 

    for dia in periodos[periodo].keys():
      for horario in periodos[periodo][dia]:
        for professor in profs:

          if periodos[periodo][dia][horario] == "" and professor.horarios[turma][periodo][dia][horario] == True: #and # qnt_materia_semana[professor.disciplina] > 0:
            periodos[periodo][dia][horario] = professor.nome
            # qnt_materia_semana[professor.disciplina.any()] -= 1      

    return periodos

# MAIN

ref = db.reference('/teachers')

# Recupere todos os professores
professores_data = ref.get()

professores = []
for key, value in professores_data.items():
    professor = Professor(value["nome"], value["disciplinas"], value["horarios"], value["periodos"], value["turmas"])
    professores.append(professor)

st.title("Montador de Horários.")

st.write("Esse é um teste de montar horários utilizando PL em conjunto com LUNA.")

periodo = st.selectbox("Selecione Período:", ["Matutino", "Vespertino", "Noturno", "Sábado"])

turma = st.selectbox("Selecione a turma", ["Vestibular", "Técnico", "Sábado"])

professores_disponiveis = organizar_disponibilidade(professores, periodo)

teachers = st.multiselect("Selecione os Professores", [prof.nome for prof in professores_disponiveis])

montar = st.button("Montar Horário")

if montar:
    horario = montarHorarios(professores_disponiveis, turma, periodo)

    df = pd.DataFrame(horario[periodo])    

    df