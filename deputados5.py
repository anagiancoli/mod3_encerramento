import requests
import pandas as pd
import streamlit as st

# URLs para buscar os dados de deputados e deputadas
url_f = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=nome'
url_m = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=nome'

# URL para buscar as despesas por deputado (usaremos formato com f-string para inserção do ID)
url_dep_template = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas?ordem=ASC&ordenarPor=ano'

# Função para buscar deputados(as) a partir das URLs fornecidas
@st.cache_data
def get_deputados_data() -> pd.DataFrame:
    response_f = requests.get(url_f)
    response_m = requests.get(url_m)
    
    if response_f.status_code == 200 and response_m.status_code == 200:
        # Combinar os resultados de deputados(as) masculinos(as) e femininos(as)
        data_f = response_f.json().get('dados', [])
        data_m = response_m.json().get('dados', [])
        all_data = data_f + data_m
        df = pd.DataFrame(all_data)
        return df[['id', 'nome', 'siglaPartido', 'siglaUf']]  # Selecionar colunas principais
    else:
        st.error("Falha ao obter dados de deputados(as).")
        return pd.DataFrame()

# Função para buscar despesas por deputado(a) com base no ID
@st.cache_data
def get_deputado_despesas(deputado_id: int) -> pd.DataFrame:
    url_dep = url_dep_template.format(id=deputado_id)
    response = requests.get(url_dep)
    
    if response.status_code == 200:
        data = response.json().get('dados', [])
        if data:
            df = pd.DataFrame(data)
            return df[['ano', 'mes', 'tipoDespesa', 'valorLiquido']]  # Selecionar colunas de interesse
        else:
            st.warning("Nenhum dado de despesas disponível.")
            return pd.DataFrame()
    else:
        st.error("Falha ao obter dados de despesas.")
        return pd.DataFrame()

# Configuração de Streamlit
st.title("Visualização de Dados de Deputados(as) e Despesas")

# Carregar dados de deputados(as)
df_deputados = get_deputados_data()

if not df_deputados.empty:
    # Seleção de deputado(a) para visualizar despesas
    st.header("Selecione um(a) Deputado(a)")
    deputado_selecionado = st.selectbox("Escolha um(a) deputado(a) para visualizar as despesas:",
                                        df_deputados['nome'].values)
    
    deputado_id = df_deputados[df_deputados['nome'] == deputado_selecionado]['id'].values[0]

    # Buscar e exibir despesas do deputado(a) selecionado(a)
    despesas_df = get_deputado_despesas(deputado_id)
    
    if not despesas_df.empty:
        st.header(f"Despesas de {deputado_selecionado}")
        st.dataframe(despesas_df, use_container_width=True)

        # Visualização simples das despesas por tipo e por ano
        st.subheader("Despesas por Tipo")
        despesas_por_tipo = despesas_df.groupby('tipoDespesa')['valorLiquido'].sum().reset_index()
        st.bar_chart(despesas_por_tipo, x='tipoDespesa', y='valorLiquido')

        st.subheader("Despesas por Ano")
        despesas_por_ano = despesas_df.groupby('ano')['valorLiquido'].sum().reset_index()
        st.line_chart(despesas_por_ano, x='ano', y='valorLiquido')
    else:
        st.warning("Nenhuma despesa disponível para o(a) deputado(a) selecionado(a).")
else:
    st.warning("Nenhum dado de deputados(as) disponível.")
