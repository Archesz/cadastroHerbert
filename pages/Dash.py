import streamlit as st
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

# Inicializa o app do Streamlit
st.title("Dashboard de Alunos")

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

students_df = load_student_data()

# Convertendo a coluna 'nascimento' para o formato de data
students_df['nascimento'] = pd.to_datetime(students_df['nascimento'], format='%Y-%m-%d')

# Calculando a idade com base na data de nascimento
today = datetime.date.today()
students_df['idade'] = students_df['nascimento'].apply(lambda x: relativedelta(today, x).years)

# Exibe tabela com dados dos alunos
st.subheader("Dados dos Alunos")
st.write(students_df)

# Gráfico de barras com a contagem de alunos por período e curso
fig_alunos_por_periodo_curso = px.bar(students_df, x='periodo', color='curso',
                                      title='Distribuição de Alunos por Período e Curso',
                                      labels={'periodo': 'Período', 'curso': 'Curso'},
                                      category_orders={'periodo': ['Manhã', 'Tarde', 'Noite']})
st.plotly_chart(fig_alunos_por_periodo_curso)

# Gráfico de barras empilhadas com a proporção de alunos por período, curso e sexo
fig_proporcao_sexo = px.bar(students_df, x='periodo', color='curso', barmode='stack',
                            title='Proporção de Alunos por Período, Curso e Sexo',
                            labels={'periodo': 'Período', 'curso': 'Curso'},
                            category_orders={'periodo': ['Manhã', 'Tarde', 'Noite']},
                            facet_col='genero')
st.plotly_chart(fig_proporcao_sexo)

fig_pizza_proporcao = px.sunburst(students_df, path=['genero', 'periodo', 'curso'],
                                  title='Proporção de Alunos por Período, Curso e Sexo')
st.plotly_chart(fig_pizza_proporcao)

# Gráfico de pizza com a proporção de alunos por gênero
fig_pizza_genero = px.pie(students_df, names='genero', title='Proporção de Alunos por Gênero')
st.plotly_chart(fig_pizza_genero)

# Gráfico de barras empilhadas com a relação de etnia
fig_etnia = px.bar(students_df, x='etnia', color='etnia', title='Relação de Etnia dos Alunos',
                   labels={'etnia': 'Etnia'},)
st.plotly_chart(fig_etnia)

# Gráfico de histograma da idade dos alunos
fig_idade = px.histogram(students_df.query("idade != 0"), x='idade', title='Histograma da Idade dos Alunos',
                         labels={'idade': 'Idade'})
st.plotly_chart(fig_idade)