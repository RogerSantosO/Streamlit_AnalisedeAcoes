import streamlit as st
from pandas_datareader import data as pdr
import pandas as pd
from datetime import date
import datetime
from plotly import graph_objs as go


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
     "Escolha a data inicial. (ANO/MES/DIA)",
     date.today() - datetime.timedelta(days=14))

DATA_FIM = st.sidebar.date_input(
     "Escolha a data final. (ANO/MES/DIA)",
     date.today())

if DATA_FIM < DATA_INICIO:
    st.error('A data final dever ser mais recente que a data inicial')

df_valores = pegar_valores_online(acao_escolhida,DATA_INICIO,DATA_FIM)

st.subheader('Tabela de valores - ' + nome_acao_escolhida)
st.write(df_valores)

fig = go.Figure()

st.subheader('Gráfico de preços')


st.sidebar.subheader('Opções do gráfico')
fech_check = st.sidebar.checkbox('Preço de fechamento',True)
if fech_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Close'],
                         name='Preço fechamento',
                         line_color='yellow'))
abert_check = st.sidebar.checkbox('Preço de abertura',True)
if abert_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Open'],
                         name='Preço abertura',
                         line_color='blue'))

fechajus_check = st.sidebar.checkbox('Fechamento Ajustado')
if fechajus_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Adj Close'],
                         name='Fechamento ajustado',
                         line_color='orange'))

alta_check = st.sidebar.checkbox('Preço mais alto do dia')
if alta_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['High'],
                         name='Preço mais alto',
                         line_color='green'))

baixa_check = st.sidebar.checkbox('Preço mais baixo do dia')
if baixa_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Low'],
                         name='Preço mais baixo',
                         line_color='red'))

st.plotly_chart(fig)

