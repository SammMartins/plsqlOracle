from email.policy import default
import pandas as pd
import streamlit as st
import plotly.express as px
from dataset import df1, df2, df3
from utils import format_number, data_semana_ini, data_semana_fim
from grafic import grafico_vend_sup, grafico_top_rca2, grafico_top_rca8

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
                key='tabela_vend3'
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
                        for index, i in enumerate(df1_result[0]):
                            st.metric("Supervisor", i, delta=index+1, delta_color='off')
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
                        for index, i in enumerate(df1_result[0]):
                            st.metric("Supervisor", i, delta=index+1, delta_color='off')
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
            st.plotly_chart(grafico_vend_sup, use_container_width=True)
            st.subheader("Legenda:")
            st.subheader("  1. A linha branca tracejada representa o valor da média de vendas na semana atual.")
            coluna1, coluna2 = st.columns(2)
            start_of_week = data_semana_ini()
            end_of_week = data_semana_fim()
            df2_result = df2(start_of_week, end_of_week)
            df_2 = df2_result[df2_result[df2_result.columns[0]] == 2]
            df_8 = df2_result[df2_result[df2_result.columns[0]] == 8]
            with coluna1:
                st.plotly_chart(grafico_top_rca8, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "TOP VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].head(1).iloc[0], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].tail(1).iloc[0], delta = "-13º")
            with coluna2:
                st.plotly_chart(grafico_top_rca2, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "TOP VENDEDOR DO SUL NA SEMANA", value = df_2[1].head(1).iloc[0], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SUL NA SEMANA", value = df_2[1].tail(1).iloc[0], delta = "-12º")


    with aba1_3: # add média de venda por cliente
        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            subcoluna1, subcoluna2 = st.columns(2)
            with subcoluna1:
                dataIni_cli = st.date_input("Escolha uma data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_cli1')
            with subcoluna2:
                dataFim_cli = st.date_input("Escolha uma data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_cli2')
        with coluna2:
            df3_result = df3(dataIni, dataFim)
            rca_filtro = st.multiselect(
                "Escolha um RCA", 
                df3_result[2].unique(), 
                default=[],
                key='tabela_cli3'
            )
        with coluna3:
            st.write(" ") # Espaço em branco para centralizar os widgets
            st.write(" ") # Espaço em branco para centralizar os widgets
            if st.button("Carregar Dados", key='tabela_cli'):
                df3_result = df3(dataIni_cli, dataFim_cli)
                if rca_filtro:
                    df3_result = df3_result[df3_result[2].isin(rca_filtro)]
                    with coluna1:
                        for i in df3_result[0]:
                            st.metric("Cliente", i[:20])




# streamlit run app.py