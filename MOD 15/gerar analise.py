import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time


def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(
            value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None



st.set_page_config(page_title='SINASC Rondônia',
                   page_icon='https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_map_of_Rondonia.png',
                   layout='wide')

st.write('# Análise SINASC')

sinasc = pd.read_csv('./input_M15_SINASC_RO_2019.csv')


sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC, format='%Y-%m-%d')

min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()


st.sidebar.title('Data :')

data_inicial = st.sidebar.date_input('From',
                                     value=min_data,
                                     min_value=min_data,
                                     max_value=max_data)
data_final = st.sidebar.date_input('To',
                                   value=max_data,
                                   min_value=min_data,
                                   max_value=max_data)


sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final))
                & (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]

plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean',
                    'média idade mãe por data', 'data nascimento')

plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'],'mean', 
                    'media idade mae', 'data de nascimento','unstack')

plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 
                    'media peso bebe', 'data de nascimento', 'unstack')

plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median',
                  'PESO mediano', 'escolaridade mae', 'sort')

plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean','apgar1 medio',
                    'gestacao', 'sort')


st.divider()

st.markdown("# Info Tables")

sinasc.drop(['ORIGEM', 'CODESTAB', 'CODMUNNASC', 'LOCNASC', 'ESTCIVMAE',
       'CODOCUPMAE', 'CODMUNRES','HORANASC','IDANOMAL', 'DTCADASTRO',
       'CODANOMAL', 'NUMEROLOTE', 'VERSAOSIST', 'DTRECEBIM', 'DIFDATA',
       'DTRECORIGA', 'NATURALMAE', 'CODMUNNATU', 'CODUFNATU', 'ESCMAE2010',
       'SERIESCMAE', 'DTNASCMAE', 'RACACORMAE', 'QTDGESTANT', 'QTDPARTNOR',
       'QTDPARTCES', 'DTULTMENST', 'SEMAGESTAC', 'TPMETESTIM',
       'CONSPRENAT', 'MESPRENAT', 'TPAPRESENT', 'STTRABPART', 'STCESPARTO',
       'TPNASCASSI', 'TPFUNCRESP', 'TPDOCRESP', 'DTDECLARAC', 'ESCMAEAGR1',
       'STDNEPIDEM', 'STDNNOVA', 'CODPAISRES', 'TPROBSON', 'PARIDADE',
       'KOTELCHUCK', 'CONTADOR', 'munResStatus', 'munResTipo',
       'munResUf', 'munResAlt', 'munResArea'],axis=1, inplace= True)



col_left , col_right = st.columns([3,1])

municipio = col_left.selectbox('Município', options= sinasc['munResNome'].unique())

progress_bar = st.progress(0)

for i in range(100):
    # Update status text.
    # status_text.text('')
    progress_bar.progress(i+1)
    time.sleep(0.005)

col_right.success('Data loaded')

sinasc = sinasc[sinasc['munResNome'] == municipio]



col_left , col_right = st.columns(2)

val = ['IDADEPAI','IDADEMAE','PESO']
ind = 'GRAVIDEZ'
df = sinasc.groupby(ind)[val].agg('mean')

col_right.dataframe(df)

val = ['IDADEPAI','IDADEMAE','PESO','GRAVIDEZ']
ind = 'GESTACAO'
df = sinasc.groupby(ind)[val].agg('mean')

col_left.dataframe(df)

val = ['IDADEPAI','IDADEMAE','GESTACAO','PESO']
ind = 'SEXO'
df = sinasc.groupby(ind)[val].agg('mean')

col_right.dataframe(df)