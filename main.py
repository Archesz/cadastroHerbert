from faker import Faker
import random
import streamlit as st
from io import BytesIO
from background import getImage, remove_bg
from docx import Document
import datetime

import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage

from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://herbert2024-be557-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://herbert2024-be557.appspot.com'
}) 

# firebase_admin.get_app()
# Sua função register_student_to_firebase vem aqui

def upload_photo_to_storage(photo_bytes, student_id):
    firebase_admin.get_app()

    bucket = storage.bucket('herbert2024-be557.appspot.com')

    blob = bucket.blob(f'student_photos/{student_id}.jpg')

    blob.upload_from_string(photo_bytes.getvalue(), content_type='image/jpeg')

    blob.make_public()

    return blob.public_url


def register_student_to_firebase(nome, cpf, nascimento, telefone, email, cep, num_casa, curso, periodo, genero, racial, instituicoes, photo=None):
    data_atual = datetime.date.today()
    ano_atual = data_atual.year
    # Verifica se o CPF já está cadastrado
    
    ref = db.reference('/students')
    students = ref.order_by_child('cpf').equal_to(cpf).get()

    if students:
        return False  # CPF já existe

    student_data = {
        'nome': nome,
        'cpf': cpf,
        'nascimento': str(nascimento),
        'telefone': telefone,
        'email': email,
        'cep': cep,
        'num_casa': num_casa,
        'curso': curso,
        'periodo': periodo,
        'genero': genero,
        'etnia': racial,
        'instituicoes': instituicoes,
        'ano': ano_atual,
        'frequencia': {
            "Matemática": 100,
            "Física": 100,
            "Química": 100,
            "Biologia": 100,
            "História": 100,
            "Geografia": 100,
            "Filosofia": 100,
            "Sociologia": 100,
            "Gramática": 100,
            "Literatura": 100,
            "Redação": 100
        },
        'score': {
            "Matemática": 0,
            "Física": 0,
            "Química": 0,
            "Biologia": 0,
            "História": 0,
            "Geografia": 0,
            "Filosofia": 0,
            "Sociologia": 0,
            "Gramática": 0,
            "Literatura": 0,
            "Redação": 0
        },
        'simulados': {
            "Unicamp": [],
            "USP": [],
            "Unesp": [],
            "Enem": [],
            "Cotuca": [],
            "Etec": [],
            "IF": [],
        }
    }
    firebase_admin.get_app()

    # Envia os dados para o Firebase
    new_student_ref = ref.push(student_data)

    if photo is not None:
        photo_url = upload_photo_to_storage(photo, cpf)  # Usando CPF como identificador único
        student_data['photo'] = photo_url
        new_student_ref.update({'photo': photo_url})

    return True

def create_fake_students(num_students):
    fake = Faker()

    for _ in range(num_students):
        nome = fake.name()
        cpf = fake.ssn()  # Isso gera um número de seguro social, ajuste conforme necessário
        nascimento = fake.date_of_birth(minimum_age=17, maximum_age=30).strftime("%Y-%m-%d")
        telefone = fake.phone_number()
        email = fake.email()
        cep = fake.postcode()
        num_casa = random.randint(1, 1000)
        curso = random.choice(['Engenharia', 'Medicina', 'Direito', 'Artes', 'Ciência da Computação'])
        periodo = random.choice(['Manhã', 'Tarde', 'Noite'])
        genero = random.choice(['Masculino', 'Feminino', 'Outro'])
        racial = random.choice(['Branco', 'Negro', 'Pardo', 'Indígena', 'Amarelo'])
        instituicoes = random.choice(['Instituição A', 'Instituição B', 'Instituição C'])

        # Chama a função para registrar o estudante
        register_student_to_firebase(nome, cpf, nascimento, telefone, email, cep, num_casa, curso, periodo, genero, racial, instituicoes)

# Cria 10 estudantes fictícios
create_fake_students(10)