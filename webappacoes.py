import streamlit as st
from pandas_datareader import data as pdr
import pandas as pd
from datetime import date, timedelta
from plotly import graph_objs as go

def pegar_dados_acoes():
    path = 'acoes.csv'
    return pd.read_csv(path, delimiter= ';')

@st.cache
def pegar_valores_online(sigla_acao,inicio,fim):
    df = pdr.get_data_yahoo(sigla_acao, start=inicio, end=fim)
    return df

#Caixa de seleção da ação número 1
st.title('Pesquisa de ações')

df = pegar_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação',acao) 

#Caixa de seleção da ação número 2
df2 = pegar_dados_acoes()

acao2 = df2['snome']
acao2_check = st.sidebar.checkbox('Adicionar mais uma ação')
if acao2_check:
    nome_acao_escolhida2 = st.sidebar.selectbox('Escolha a segunda ação',acao2) 

#Código da ação número 1 

df_acao = df[df['snome']==nome_acao_escolhida]
acao_escolhida = df_acao.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA'

DATA_INICIO = st.sidebar.date_input(
     "Escolha a data inicial. (ANO/MES/DIA)",
     date.today() - timedelta(days=14))

DATA_FIM = st.sidebar.date_input(
     "Escolha a data final. (ANO/MES/DIA)",
     date.today())

if DATA_FIM < DATA_INICIO:
    st.error('A data final dever ser mais recente que a data inicial')

df_valores = pegar_valores_online(acao_escolhida,DATA_INICIO,DATA_FIM)

st.subheader('Tabela de valores - ' + nome_acao_escolhida)
st.write(df_valores)

#Código da ação número 2

if acao2_check:
    df_acao2 = df2[df2['snome']==nome_acao_escolhida2]
    acao_escolhida2 = df_acao2.iloc[0]['sigla_acao']
    acao_escolhida2 = acao_escolhida2 + '.SA'

    df_valores2 = pegar_valores_online(acao_escolhida2,DATA_INICIO,DATA_FIM)

    st.subheader('Tabela de valores - ' + nome_acao_escolhida2)
    st.write(df_valores2)

#Gráfico ação número 1

fig = go.Figure()

st.subheader('Gráfico de preços')


st.sidebar.subheader('Opções do gráfico')
fech_check = st.sidebar.checkbox('Preço de fechamento')
if fech_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Close'],
                         name=f'Preço fechamento {acao_escolhida}',
                         line_color='yellow'))
abert_check = st.sidebar.checkbox('Preço de abertura')
if abert_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Open'],
                         name=f'Preço abertura {acao_escolhida}',
                         line_color='blue'))

fechajus_check = st.sidebar.checkbox('Fechamento Ajustado')
if fechajus_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Adj Close'],
                         name=f'Fechamento ajustado {acao_escolhida}',
                         line_color='orange'))

alta_check = st.sidebar.checkbox('Preço mais alto do dia',True)
if alta_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['High'],
                         name=f'Preço mais alto {acao_escolhida}',
                         line_color='green'))

baixa_check = st.sidebar.checkbox('Preço mais baixo do dia')
if baixa_check:
    fig.add_trace(go.Scatter(x=df_valores.index,
                         y=df_valores['Low'],
                         name=f'Preço mais baixo {acao_escolhida}',
                         line_color='red'))

#Gráfico ação número 2
if acao2_check:
    st.sidebar.subheader('Opções do gráfico da segunda ação')
    fech_check2 = st.sidebar.checkbox('Preço de fechamento ')
    if fech_check2:
        fig.add_trace(go.Scatter(x=df_valores2.index,
                            y=df_valores2['Close'],
                            name=f'Preço fechamento {acao_escolhida2}',
                            line_color='black'))
    abert_check2 = st.sidebar.checkbox('Preço de abertura ')
    if abert_check2:
        fig.add_trace(go.Scatter(x=df_valores2.index,
                            y=df_valores2['Open'],
                            name=f'Preço abertura {acao_escolhida2}',
                            line_color='brown'))

    fechajus_check2 = st.sidebar.checkbox('Fechamento Ajustado ')
    if fechajus_check2:
        fig.add_trace(go.Scatter(x=df_valores2.index,
                            y=df_valores2['Adj Close'],
                            name=f'Fechamento ajustado {acao_escolhida2}',
                            line_color='purple'))

    alta_check2 = st.sidebar.checkbox('Preço mais alto do dia ',True)
    if alta_check2:
        fig.add_trace(go.Scatter(x=df_valores2.index,
                            y=df_valores2['High'],
                            name=f'Preço mais alto {acao_escolhida2}',
                            line_color='pink'))

    baixa_check2 = st.sidebar.checkbox('Preço mais baixo do dia ')
    if baixa_check2:
        fig.add_trace(go.Scatter(x=df_valores2.index,
                            y=df_valores2['Low'],
                            name=f'Preço mais baixo {acao_escolhida2}',
                            line_color='gray'))

st.plotly_chart(fig)

