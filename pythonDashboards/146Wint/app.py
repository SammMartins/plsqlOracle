from email.policy import default
import pandas as pd
import streamlit as st
import plotly.express as px
from dataset import df1, df2, df3
from utils import format_number
from grafic import grafico_vend_sup, grafico_top_rca, grafico_top_rca2, grafico_top_rca8

# Configuração do dashboard
st.set_page_config(page_title="Premium Dashboards", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")
st.title("Premium Dashboards :bar_chart:")
st.markdown("Este é um o projeto inicial de Dashboards em Python para a Premium Distribuidora")

aba1, aba2, aba3 = st.tabs(["Vendas Tempo Real", "Dashboard 2", "Dashboard 3"])

with aba1:
    aba1_1, aba1_2, aba1_3, aba1_4 = st.tabs(["Tabelas", "Gráficos", "Clientes", "Fornecedores"])
    with aba1_1:
        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            subcoluna1, subcoluna2 = st.columns(2)
            with subcoluna1:
                dataIni = st.date_input("Escolha uma data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_vend1')
            with subcoluna2:
                dataFim = st.date_input("Escolha uma data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_vend2')
        with coluna2:
            df2_result = df2(dataIni, dataFim)
            sup_filtro = st.multiselect(
                "Escolha um Supervisor", 
                df2_result[0].unique(), 
                key='tabela_vend3',
            )
        with coluna3:
            st.write(" ") # Espaço em branco para centralizar os widgets
            st.write(" ") # Espaço em branco para centralizar os widgets
            if st.button("Carregar Dados", key='tabela_vend'):
                df1_result = df1(dataIni, dataFim)
                df2_result = df2(dataIni, dataFim)

                # ----------------- Tabela de Vendas por Supervisor -----------------
                if sup_filtro:
                    df1_result = df1_result[df1_result[3].isin(sup_filtro)]
                    with coluna1: # -> Supervisor
                        for i in df1_result[0]:
                            st.metric("Supervisor", i)
                    with coluna2: # -> VENDIDO
                        for i in df1_result[1]:
                            st.metric("VENDIDO", format_number(i, 'R$'))
                    with coluna3: # -> DN
                        for i in df1_result[2]:
                            st.metric("DN", i)
                    if len(sup_filtro) > 1:
                        with coluna1: # -> Supervisor
                            st.metric("Total", 'TOTAL')
                        with coluna2: # -> VENDIDO
                            st.metric("Total Vendido", format_number(df1_result[1].sum(), 'R$'))
                        with coluna3: # -> DN
                            st.metric("Total DN", df1_result[2].sum())
                else:
                    with coluna1: # -> Supervisor
                        for i in df1_result[0]:
                            st.metric("Supervisor", i)
                    with coluna2: # -> VENDIDO
                        for i in df1_result[1]:
                            st.metric("VENDIDO", format_number(i, 'R$'))
                    with coluna3: # -> DN
                        for i in df1_result[2]:
                            st.metric("DN", i)
                    with coluna1: # -> Supervisor
                        st.metric("Total", 'TOTAL')
                    with coluna2: # -> VENDIDO
                        st.metric("Total Vendido", format_number(df1_result[1].sum(), 'R$'))
                    with coluna3: # -> DN
                        st.metric("Total DN", df1_result[2].sum())
                
                # ----------------- Tabela de Vendas por RCA -----------------
                if sup_filtro:
                    df2_result = df2_result[df2_result[0].isin(sup_filtro)]
                    with coluna1:
                        for i in df2_result[1]:
                            st.metric("RCA", i)
                    with coluna2:
                        for i in df2_result[2]:
                            st.metric("VENDIDO", format_number(i, 'R$'))
                    with coluna3:
                        for i in df2_result[3]:
                            st.metric("DN", i)
                else:
                    with coluna1:
                        for i in df2_result[1]:
                            st.metric("RCA", i)
                    with coluna2:
                        for i in df2_result[2]:
                            st.metric("VENDIDO", format_number(i, 'R$'))
                    with coluna3:
                        for i in df2_result[3]:
                            st.metric("DN", i)            
    with aba1_2:
        if st.button("Carregar Dados", key='grafico_vend_sup'):
            st.plotly_chart(grafico_top_rca, use_container_width=True)
            st.write("Legenda:")
            st.write("  1. A linha branca tracejada representa a média de vendas dos RCA na semana atual.")
            st.plotly_chart(grafico_vend_sup, use_container_width=True)
            coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.plotly_chart(grafico_top_rca8, use_container_width=True)
            with coluna2:
                st.plotly_chart(grafico_top_rca2, use_container_width=True)

    with aba1_3:
        coluna1, coluna2, coluna3 = st.columns(3)


# streamlit run app.py