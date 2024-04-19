import pandas as pd
import streamlit as st
import plotly.express as px
from dataset import load_df

# Configuração do dashboard
st.set_page_config(page_title="Premium Dashboards", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")
st.title("Premium Dashboards :bar_chart:")
st.markdown("Este é um o projeto inicial de Dashboards em Python para a Premium Distribuidora")

aba1, aba2, aba3 = st.tabs(["Vendas Tempo Real", "Dashboard 2", "Dashboard 3"])

with aba1:
    dataIni = st.date_input("Escolha uma data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY')
    dataFim = st.date_input("Escolha uma data final", value=pd.to_datetime('today'), format='DD/MM/YYYY')

    df = load_df(dataIni, dataFim)

    st.dataframe(df)

# streamlit run app.py