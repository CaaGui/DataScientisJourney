import pandas as pd
import numpy as np
import streamlit as st
from pycaret.classification import *


@st.cache_data(show_spinner=True)
def load_data(file_data):
    if file_data.name.split('.')[-1] == 'csv':
        return pd.read_csv(file_data)
    elif file_data.name.split('.')[-1] == 'xlsx':
        return pd.read_excel(file_data)
    elif file_data.name.split('.')[-1] == 'ftr':
        return pd.read_feather(file_data)


# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(page_title='Credit Risk',
                       page_icon='',
                       layout="wide",
                       initial_sidebar_state='expanded'
                       )

    st.markdown('## Model Prediction')

    sidebar = st.sidebar
    sidebar.title('Data Model')
    data_file = sidebar.file_uploader('', ['csv', 'xlsx', 'ftr'])

    if data_file != None:
        df_raw = load_data(data_file)
        st.write(df_raw)

        model_saved = load_model(
            'Quadratic Discriminant Analysis Model mod38 ex1')

        if st.button('Predict'):
            df_pred = predict_model(model_saved, data=df_raw.drop(
                columns=['data_ref', 'index']))

            st.download_button(label='📥 Download csv file',
                               data=df_pred['prediction_label'].to_csv(),
                               file_name='model_predict.csv')


if __name__ == '__main__':
    main()
