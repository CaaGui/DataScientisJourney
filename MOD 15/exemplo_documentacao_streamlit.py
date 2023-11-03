import streamlit as st
import numpy as np
import pandas as pd

st.write('Bem Vindo')

df = np.random.randn(10,20)
st.dataframe(df)


df = pd.DataFrame(
    np.random.randn(10,20),
    columns=('col %d' % i for i in range(20))
)

st.dataframe(df.style.highlight_max(axis=0))