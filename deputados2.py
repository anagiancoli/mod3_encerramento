####### QUESTAO 2

# Importando as bibliotecas para download e criação de dataframe
import requests as rq
import pandas as pd
import streamlit as st
import requests as rq

url_dep = 'https://dadosabertos.camara.leg.br/api/v2/deputados/74646/despesas?ordem=ASC&ordenarPor=ano'

# Efetuando o download dados feminino
resp_dep = rq.get(url_dep)
deputados_json = resp_dep.json()

# Criando o dataframe 
df_dep = pd.DataFrame(deputados_json['dados'])

# Calculando os gastos
gastos = df_dep['valorLiquido'].sum()
nomeDeputado = "Aécio Neves"

st.title('Gastos do deputado ' + nomeDeputado)
st.metric('Gastos do deputado', gastos)
