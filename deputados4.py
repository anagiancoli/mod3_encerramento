import requests
import pandas as pd
import streamlit as st

# URL para buscar as despesas do deputado
url_dep = 'https://dadosabertos.camara.leg.br/api/v2/deputados/74646/despesas?ordem=ASC&ordenarPor=ano'

# Função para buscar dados de despesas do deputado
@st.cache_data
def get_deputado_despesas() -> pd.DataFrame:
    response = requests.get(url_dep)
    
    if response.status_code == 200:
        # Convertendo os dados de JSON para DataFrame
        data = response.json().get('dados', [])  # Supondo que os dados estão na chave 'dados'
        if data:
            df = pd.DataFrame(data)
            return df  # Retorna o DataFrame com todas as colunas disponíveis
        else:
            st.warning("Nenhum dado disponível para esta consulta.")
            return pd.DataFrame()
    else:
        st.error("Falha ao obter dados da URL fornecida.")
        return pd.DataFrame()

# Configurações de Streamlit
st.title("Despesas do Deputado - Dados Abertos Câmara dos Deputados")
df = get_deputado_despesas()

if not df.empty:
    # Exibir o DataFrame com as despesas
    st.header("Despesas do Deputado")
    st.dataframe(df, use_container_width=True)

    # Opcional: filtros para explorar os dados
    ano_selecionado = st.selectbox("Selecione um ano para filtrar:", options=df['ano'].unique())
    df_filtrado = df[df['ano'] == ano_selecionado]
    st.header(f"Despesas no Ano de {ano_selecionado}")
    st.dataframe(df_filtrado, use_container_width=True)

    # Exemplo de visualização gráfica simples
    st.header("Gráfico de Despesas por Tipo de Despesa")
    df_agrupado = df_filtrado.groupby('tipoDespesa')['valorLiquido'].sum().reset_index()
    st.bar_chart(df_agrupado, x='tipoDespesa', y='valorLiquido')
else:
    st.warning("Nenhum dado de despesas disponível para exibição.")
