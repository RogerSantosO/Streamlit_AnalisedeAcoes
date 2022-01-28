import streamlit as st
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
from datetime import date
import datetime
from plotly import graph_objs as go

yf.pdr_override() # <== that's all it takes :-)


#DATA_FIM = date.today().strftime('%Y-%m-%d')

# download dataframe
st.title('Pesquisa de ações')


def pegar_dados_acoes():
    path = 'acoes.csv'
    return pd.read_csv(path, delimiter= ';')

df = pegar_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação',acao) 

df_acao = df[df['snome']==nome_acao_escolhida]
acao_escolhida = df_acao.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA'

@st.cache
def pegar_valores_online(sigla_acao,inicio,fim):
    df = pdr.get_data_yahoo(sigla_acao, start=inicio, end=fim)
    return df

DATA_INICIO = st.sidebar.date_input(
     "Escolha a data inicial",
     datetime.date(2020, 1, 1))

DATA_FIM = st.sidebar.date_input(
     "Escolha a data final",
     datetime.date(2022, 1, 1))

df_valores = pegar_valores_online(acao_escolhida,DATA_INICIO,DATA_FIM)

st.subheader('Tabela de valores - ' + nome_acao_escolhida)
st.write(df_valores)

st.subheader('Gráfico de preços')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Close'],
                         name='Preço fechamento',
                         line_color='yellow'))
fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Open'],
                         name='Preço abertura',
                         line_color='blue'))

st.plotly_chart(fig)

