import requests
import pandas as pd
import streamlit as st

# URLs para os dados de deputados
url_f = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=nome'
url_m = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=nome'

# Função para buscar dados da API
@st.cache_data
def get_deputados_data() -> pd.DataFrame:
    response_f = requests.get(url_f)
    response_m = requests.get(url_m)
    
    if response_f.status_code == 200 and response_m.status_code == 200:
        # Convertendo os dados de JSON para DataFrame
        data_f = response_f.json()['dados']
        data_m = response_m.json()['dados']
        all_data = data_f + data_m
        # Transformando em DataFrame
        df = pd.DataFrame(all_data)
        return df[['nome', 'siglaPartido', 'siglaUf']]  # Seleciona colunas principais
    else:
        st.error("Falha ao obter dados da API.")
        return pd.DataFrame()

# Configurações de Streamlit
st.title("Deputados Federais - Brasil")
df = get_deputados_data()

if not df.empty:
    # Exibir DataFrame na aba de seleção
    select, compare = st.tabs(["Selecione os Deputados", "Comparar Selecionados"])
    
    with select:
        st.header("Todos os Deputados")
        st.dataframe(df, use_container_width=True)

        # Seleção de linhas
        selected_rows = st.multiselect("Selecione deputados para comparação", df.index, format_func=lambda x: df.loc[x, 'nome'])
        selected_df = df.loc[selected_rows]

        st.header("Deputados Selecionados")
        st.dataframe(selected_df, use_container_width=True)

    with compare:
        if not selected_df.empty:
            st.header("Comparação (Exemplo)")
            st.write("Aqui, você pode adicionar gráficos ou análises adicionais com base nos deputados selecionados.")
        else:
            st.markdown("Nenhum deputado selecionado.")
else:
    st.warning("Nenhum dado disponível para exibição.")
