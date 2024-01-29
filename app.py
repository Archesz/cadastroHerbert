import streamlit as st
from io import BytesIO
# from background import getImage, remove_bg
from docx import Document
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://herbert2024-be557-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://herbert2024-be557.appspot.com'
}) 


st.title("Sistema Herbert de Souza")

st.write("""
         O sistema do Herbert é um protótipo para um sistema de cadastro e visualização dos estudantes do Herbert.

         Versão: 0.1.4
         
         Desenvolvedor: AToSh
        """)