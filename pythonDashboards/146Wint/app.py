from email.policy import default
import pandas as pd
import streamlit as st
import plotly.express as px
from dataset import df1, df2, df3, df4
from utils import format_number, data_semana_ini, data_semana_fim
from grafic import grafico_vend_sup, grafico_top_rca2, grafico_top_rca8

# Configuração do dashboard
st.set_page_config(page_title="Premium Dashboards", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")
st.title("PREMIUM DASHBOARDS :bar_chart:")
st.markdown("Este é um o projeto inicial de Dashboards em Python para a Premium Distribuidora")
st.markdown("Selecione a aba desejada para visualizar os dados.")
st.markdown("  ")
st.markdown("  ")

aba1, aba2, aba3 = st.tabs(["Vendas Tempo Real", "Dashboard INATIVO", "Dashboard INATIVO"])

with aba1:
    st.subheader("PAINEL BASEADO NA 146 WINTHOR :dollar:")
    st.markdown("Apenas pedidos digitados pelo vendedor em seu aparelho.")
    st.markdown("  ")
    st.markdown("  ")

    aba1_1, aba1_2, aba1_3, aba1_4 = st.tabs(["Geral", "Gráfico", "Por Cliente", "Por Fornecedor"])
    with aba1_1:
        container = st.container(border=True)
        coluna1, coluna2, coluna3 = st.columns(3)
        with container:
            with coluna1:
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    dataIni = st.date_input("Data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_vend1')
                with subcoluna2:
                    dataFim = st.date_input("Data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_vend2')
            with coluna2:
                df2_result = df2(dataIni, dataFim)
                sup_filtro = st.multiselect(
                    "Escolha o Supervisor", 
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
                        with coluna1: 
                            for i in (df1_result[0]):
                                st.metric("Supervisor", i)
                        with coluna2: 
                            subcol1, subcol2 = st.columns([2,1])
                            with subcol1:
                                for i in df1_result[1]:
                                    st.metric("VENDIDO", format_number(i, 'R$'))
                            with subcol2:
                                for i in df1_result[2]:
                                    st.metric("DN", i)
                        if len(sup_filtro) > 1:
                            with coluna1: 
                                st.metric("Total", 'TOTAL')
                            with coluna2: 
                                subcol1, subcol2 = st.columns([2,1])
                                with subcol1:
                                    st.metric("TOTAL VENDIDO", format_number(df1_result[1].sum(), 'R$'))
                                with subcol2:
                                    st.metric("TOTAL DN", df1_result[2].sum())
                    else:
                        with coluna1: 
                            for i in (df1_result[0]):
                                st.metric("Supervisor", i)
                        with coluna2: 
                            subcol1, subcol2 = st.columns([2,1])
                            with subcol1:
                                for i in df1_result[1]:
                                    st.metric("VENDIDO", format_number(i, 'R$'))
                            with subcol2:
                                for i in df1_result[2]:
                                    st.metric("DN", i)
                        with coluna1: 
                            st.metric("Total", 'TOTAL')
                        with coluna2: 
                                subcol1, subcol2 = st.columns([2,1])
                                with subcol1:
                                    st.metric("TOTAL VENDIDO", format_number(df1_result[1].sum(), 'R$'))
                                with subcol2:
                                    st.metric("TOTAL DN", df1_result[2].sum())
                    
                    # ----------------- Tabela de Vendas por RCA -----------------
                    if sup_filtro:
                        df2_result = df2_result[df2_result[0].isin(sup_filtro)]
                        with coluna1:
                            for i in df2_result[1]:
                                st.metric("RCA", i)
                        with coluna2:
                            subcol1, subcol2 = st.columns([2,1])
                            with subcol1:
                                for i in df2_result[2]:
                                    st.metric("VENDIDO", format_number(i, 'R$'))
                            with subcol2:
                                for i in df2_result[3]:
                                    st.metric("DN", i)
                    else:
                        with coluna1:
                            for i in df2_result[1]:
                                st.metric("RCA", i)
                        with coluna2:
                            subcol1, subcol2 = st.columns([2,1])
                            with subcol1:
                                for i in df2_result[2]:
                                    st.metric("VENDIDO", format_number(i, 'R$'))
                            with subcol2:
                                for i in df2_result[3]:
                                    st.metric("DN", i)    

    with aba1_2:
        st.subheader("Legenda:")
        st.markdown("  1. Os dados abaixo são de vendas na semana atual.")
        st.markdown("  2. A linha branca tracejada representa o valor da média de vendas na semana atual.")
        if st.button("Carregar Dados", key='grafico_vend_sup'):
            start_of_week = data_semana_ini()
            end_of_week = data_semana_fim()
            df2_result = df2(start_of_week, end_of_week)
            st.plotly_chart(grafico_vend_sup, use_container_width=True)
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col2: 
                st.metric(label = "TOP MELHOR VENDEDOR", value = df2_result[1].head(1).iloc[0], delta = "1º")
            with metric_col3:
                st.metric(label = "PIOR VENDEDOR", value = df2_result[1].tail(1).iloc[0], delta = "-24º")
            coluna1, coluna2 = st.columns(2)
            df_2 = df2_result[df2_result[df2_result.columns[0]] == 2]
            df_8 = df2_result[df2_result[df2_result.columns[0]] == 8]
            with coluna1:
                st.plotly_chart(grafico_top_rca8, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "TOP MELHOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].head(1).iloc[0], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].tail(1).iloc[0], delta = "-13º")
            with coluna2:
                st.plotly_chart(grafico_top_rca2, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "TOP MELHOR VENDEDOR DO SUL NA SEMANA", value = df_2[1].head(1).iloc[0], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SUL NA SEMANA", value = df_2[1].tail(1).iloc[0], delta = "-11º")


    with aba1_3: # add média de venda por cliente
        container = st.container(border=True)
        col = st.columns(1)
        coluna1, coluna2, coluna3 = st.columns(3)
        with container:
            with coluna1:
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    dataIni_cli = st.date_input("Data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_cli1')
                with subcoluna2:
                    dataFim_cli = st.date_input("Data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_cli2')
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
                                st.metric("Cliente", i[:25])
                        with coluna2:
                            for i in df3_result[2]:
                                st.metric("RCA", i)
                        with coluna3:
                            for i in df3_result[3]:
                                st.metric("VENDIDO", format_number(i, 'R$'))

    with aba1_4:
        container = st.container(border=False)
        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                dataIni_fornec = st.date_input("Data inicial", 
                                            value=pd.to_datetime('today'), 
                                            format='DD/MM/YYYY', 
                                            key='tabela_fornec1')
            with subcol2:
                dataFim_fornec = st.date_input("Data final", 
                                            value=pd.to_datetime('today'), 
                                            format='DD/MM/YYYY', 
                                            key='tabela_fornec2')
        df4_result = df4(dataIni_fornec, dataFim_fornec)
        with coluna2:
            df4_resultF = df4(dataIni_fornec, dataFim_fornec)
            fornec_filtro = st.selectbox(
                "Filtro Fornecedor", 
                df4_resultF[1].unique(), 
                index=None, 
                key='tabela_fornec3',
                placeholder="Selecione o Fornecedor...",
            )
        with coluna3:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                st.write(" ") # Espaço em branco para centralizar os widgets
                st.write(" ") # Espaço em branco para centralizar os widgets
                if st.button("Carregar", key='tabela_fornec'):
                    if fornec_filtro:
                        df4_result = df4_result[df4_result[1].isin([fornec_filtro])]
        df4_result = df4_result.iloc[:, [0, 1, 3, 4, 5, 7]]
        df4_result.iloc[:, 5] = df4_result.iloc[:, 5].astype(float).map(lambda x: 'R${:,.2f}'.format(x))
        # Renomear colunas
        df4_result = df4_result.rename(columns={
            0: 'Cód',
            1: 'Fornecedor',
            3: 'Supervisor',
            4: 'Cód',
            5: 'RCA',
            7: 'Valor R$'
        })
        html_table = df4_result.to_html() # Convertendo o DataFrame para HTML
        st.markdown(html_table, unsafe_allow_html=True) # Exibindo a tabela no Streamlit