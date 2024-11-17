# Importando as bibliotecas para download e criação de dataframe
import requests as rq
import pandas as pd

# URL dados femininos
url_f = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=nome'

# Efetuando o download dados feminino
resp_f = rq.get(url_f)
dadosF_json = resp_f.json()

# Criando o dataframe feminino
df_F = pd.DataFrame(dadosF_json['dados'])
df_F['sexo'] = 'F'

# URL dados masculinos
url_m = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=nome'

# Efetuando o download dados masculino
resp_m = rq.get(url_m)
dadosM_json = resp_m.json()

# Criando o dataframe masculino
df_M = pd.DataFrame(dadosM_json['dados'])
df_M['sexo'] = 'M'

# Concatenando os Dataframes
df = pd.concat([df_F, df_M])

# Filtrando o dataframe por sexo e inserindo um selectbox para seleção
import streamlit as st

opcao = st.selectbox( 'Qual o sexo?', df['sexo'].unique() )

df_filtroSexo = df[df['sexo'] == opcao]

if opcao == "F":
  letra = 'a'
else:
  letra = 'o'

st.title(f'Deputad{letra}s do sexo ' + opcao)

# Ocorrências totais
# Procurando no chat GPT: Como calcular a quantidade de deputados por estado?

ocorrencias = df_filtroSexo['siglaUf'].value_counts()
df_UF = pd.DataFrame( { 'siglaUf': ocorrencias.index, 'quantidade': ocorrencias.values} )

col1, col2 = st.columns(2)

# Total de homens (sexo == M) ->> Dataframe df_M
total_masculino = df_M['id'].count()
col1.metric('Total Masculino', total_masculino)

# Total de mulheres (sexo == F) ->> Dataframe df_F
total_feminino = df_F['id'].count()
col2.metric('Total Feminino', total_feminino)

st.write(f'Total de Deputad{letra}s do sexo ' + opcao)
st.bar_chart(df_UF, x = 'siglaUf', y = 'quantidade', x_label='Siglas dos Estados', y_label=f'Quantidade de Deputad{letra}s')

st.dataframe(df_filtroSexo)
