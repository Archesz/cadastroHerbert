import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from datetime import datetime
import plotly.express as px

def transformar_em_dataframe(dados):
    return pd.DataFrame(dados.values())

firebase_admin.get_app()

st.set_page_config(
    layout="wide"
)

st.title('Meu Dashboard')

# Função para buscar os dados dos estudantes
def buscar_dados_estudantes():
    ref = db.reference('/students')
    return ref.get()

# Exibir dados dos estudantes
dados_estudantes = buscar_dados_estudantes()

# Buscar dados
dados_estudantes = buscar_dados_estudantes()
df = transformar_em_dataframe(dados_estudantes)

# Calcular a idade dos estudantes
df['idade'] = df['nascimento'].apply(lambda x: datetime.now().year - pd.to_datetime(x).year)

# Distribuição de Estudantes por Curso
fig_curso = px.histogram(df, x='curso', title='Distribuição de Estudantes por Curso')
st.plotly_chart(fig_curso)

# Distribuição de Estudantes por Gênero
fig_genero = px.histogram(df, x='genero', title='Distribuição de Estudantes por Gênero')
st.plotly_chart(fig_genero)

# Média de Idade dos Estudantes por Curso
fig_idade_curso = px.bar(df.groupby('curso')['idade'].mean().reset_index(), x='curso', y='idade', title='Média de Idade por Curso')
st.plotly_chart(fig_idade_curso)

# Distribuição de Estudantes por Etnia
fig_etnia = px.histogram(df, x='etnia', title='Distribuição de Estudantes por Etnia')
st.plotly_chart(fig_etnia)
