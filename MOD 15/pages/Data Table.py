import streamlit as st
import pandas as pd
import numpy as np
import time


st.set_page_config(page_title='',
                   page_icon='https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_map_of_Rondonia.png',
                   layout='wide')


st.markdown("# Sinasc Data Table")

sinasc = pd.read_csv('./input_M15_SINASC_RO_2019.csv')

sinasc.drop(['ORIGEM', 'CODESTAB', 'CODMUNNASC', 'LOCNASC', 'ESTCIVMAE',
       'CODOCUPMAE', 'CODMUNRES','HORANASC','IDANOMAL', 'DTCADASTRO',
       'CODANOMAL', 'NUMEROLOTE', 'VERSAOSIST', 'DTRECEBIM', 'DIFDATA',
       'DTRECORIGA', 'NATURALMAE', 'CODMUNNATU', 'CODUFNATU', 'ESCMAE2010',
       'SERIESCMAE', 'DTNASCMAE', 'RACACORMAE', 'QTDGESTANT', 'QTDPARTNOR',
       'QTDPARTCES', 'IDADEPAI', 'DTULTMENST', 'SEMAGESTAC', 'TPMETESTIM',
       'CONSPRENAT', 'MESPRENAT', 'TPAPRESENT', 'STTRABPART', 'STCESPARTO',
       'TPNASCASSI', 'TPFUNCRESP', 'TPDOCRESP', 'DTDECLARAC', 'ESCMAEAGR1',
       'STDNEPIDEM', 'STDNNOVA', 'CODPAISRES', 'TPROBSON', 'PARIDADE',
       'KOTELCHUCK', 'CONTADOR', 'munResStatus', 'munResTipo',
       'munResUf', 'munResAlt', 'munResArea'],axis=1, inplace= True)

sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC, format='%Y-%m-%d')

st.sidebar.title('Date')

col_left , col_right = st.sidebar.columns(2)

min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()

date_start = col_left.date_input('From :',
                                    value=min_data,
                                    min_value=min_data,
                                    max_value=max_data)
date_end = col_right.date_input('To :',
                                value=max_data,
                                min_value=min_data,
                                max_value=max_data)

sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(date_end))
                & (sinasc['DTNASC'] >= pd.to_datetime(date_start))]


if 'municipio' not in st.session_state or 'escola' not in st.session_state or \
'gender' not in st.session_state:
    st.session_state['municipio'] = None
    st.session_state['escola'] = None
    st.session_state['gender'] = sinasc['SEXO'].unique()


sinasc = sinasc.query('munResNome == @municipio \
                      | ESCMAE == @escola \
                      | SEXO == @gender'
                      )

col_left , col_right = st.columns(2)


with col_left.expander(label='Município'):
    municipio = st.multiselect(' ', 
                               options=sinasc['munResNome'].unique(),
                               default= st.session_state['municipio']
                               )

with col_right.expander(label='Escolaridade mãe'):
    escola = st.multiselect('',
                            options=sinasc['ESCMAE'].unique(),
                            default= st.session_state['escola']
                            )

with col_left.expander(label='Sexo'):
    gender = st.multiselect('  ', 
                            options=sinasc['SEXO'].unique(),
                            default= st.session_state['gender'])

load = col_right.button('Load', args= [municipio,escola,gender],
                        use_container_width=True)



st.dataframe(sinasc)



# col_left , col_right = st.columns([2,1])
# progress_bar = col_left.progress(0)
# # status_text = st.empty()

# for i in range(100):
#     # Update status text.
#     # status_text.text('')
#     progress_bar.progress(i+1)
#     time.sleep(0.005)

# col_right.success('Data loaded')




# Forms can be declared using the 'with' syntax
# with st.form(key='my_form'):
#     text_input = st.text_input(label='Enter your name')
#     submit_button = st.form_submit_button(label='Submit')


# Alternative syntax, declare a form and use the returned object
# form = st.form(key='my_form')
# form.text_input(label='Enter some text')
# submit_button = form.form_submit_button(label='Submit')´


# st.form_submit_button returns True upon form submit
# if submit_button:
#     st.write(f'hello {text_input}')


# uploaded_files = st.file_uploader(
#     "Upload multiple files", accept_multiple_files=True)

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         st.write("Filename: ", uploaded_file.name)


# progress_bar = st.progress(0)
# status_text = st.empty()
# chart = st.line_chart(np.random.randn(10, 2))

# for i in range(50):
#     # Update progress bar.
#     progress_bar.progress(i + 1)

#     new_rows = np.random.randn(10, 2)

#     # Update status text.
#     status_text.text(
#         'The latest random number is: %s' % new_rows[-1, 1])

#     # Append data to the chart.
#     chart.add_rows(new_rows)

#     # Pretend we're doing some computation that takes time.
#     time.sleep(0.1)
