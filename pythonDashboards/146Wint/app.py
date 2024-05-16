from ast import With
from email.policy import default
import pandas as pd
import streamlit as st
import time as tm
import math
import plotly.express as px
from dataset import df1, df2, df3, df4, diasUteis, diasDecorridos
from utils import format_number, data_semana_ini, data_semana_fim
from grafic import grafico_vend_sup, grafico_top_rca2, grafico_top_rca8

# Configuração do dashboard
st.set_page_config(page_title="Performax B.I.", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")
placeholder = st.empty()
columP1, columP2, columP3, columP4 = st.columns(4)
with columP2:
    st.title(":green[$ PERFORMAX]", help="Plataforma de Excelência para Resultados e Fornecimento de Melhorias e Análises")
    #st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/performax_.png', width=180)
with columP3:
    st.markdown("  ")
    st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/premium_transp.png', width=180)
#st.header("  ", divider="gray")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown(":arrow_double_down: Selecione uma a aba abaixo :arrow_double_down:")

aba1, aba2, aba3 = st.tabs([":dollar: VENDA", ":bar_chart: FLASH", ":lock: INATIVO"])

with aba1:
    st.header("PAINEL DE VENDAS")
    st.markdown("Legenda:")
    st.markdown(":page_with_curl: Faturado e não faturado semelhante a rotina 322 Winthor")
    st.markdown(":iphone:   Apenas pedidos digitados pelo vendedor são exibidos")
    st.markdown("  ")
    st.markdown("  ")
    aba1_1, aba1_2, aba1_3, aba1_4, aba1_5 = st.tabs([":dollar: Geral", ":bar_chart: Gráfico", ":convenience_store: Por Cliente", ":factory: Por Fornecedor", ":page_facing_up: Por Seção - Inativo :lock:"])
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #     
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
                    with st.spinner('Caregando dados...'):
                        tm.sleep(3)
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
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #
    with aba1_2:
        st.markdown("Legenda:")
        st.markdown("  1. Os dados abaixo são de vendas na semana atual.")
        st.markdown("  2. A linha branca tracejada representa o valor da média de vendas na semana atual.")
        if st.button("Carregar Dados", key='grafico_vend_sup'):
            with st.spinner('Caregando dados...'):
                tm.sleep(3)
                start_of_week = data_semana_ini()
                end_of_week = data_semana_fim()
                df2_result = df2(start_of_week, end_of_week)
                df_2 = df2_result[df2_result[df2_result.columns[0]] == 2]
                df_8 = df2_result[df2_result[df2_result.columns[0]] == 8]
            st.plotly_chart(grafico_vend_sup, use_container_width=True)
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col2: 
                st.metric(label = "TOP MELHOR VENDEDOR", value = df2_result[1].head(1).iloc[0][6:], delta = "1º")
            with metric_col3:
                st.metric(label = "PIOR VENDEDOR", value = df2_result[1].tail(1).iloc[0][6:], delta = "-24º")
            coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.plotly_chart(grafico_top_rca8, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "TOP MELHOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].head(1).iloc[0][6:], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].tail(1).iloc[0][6:], delta = "-13º")
            with coluna2:
                st.plotly_chart(grafico_top_rca2, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "TOP MELHOR VENDEDOR DO SUL NA SEMANA", value = df_2[1].head(1).iloc[0][6:], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SUL NA SEMANA", value = df_2[1].tail(1).iloc[0][6:], delta = "-11º")
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #
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
                    with st.spinner('Caregando dados...'):
                        tm.sleep(3)
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
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #
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
                    with st.spinner('Caregando dados...'):
                        tm.sleep(3)
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
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #     
with aba2:
    st.header("RELATÓRIO FLASH")
    #st.subheader("Legenda:")
    st.markdown(":rocket: Um painel completo sobre seu :blue[desempenho] de vendas ")
    st.markdown(":moneybag: Tenha controle sobre sua :green[remuneração] mensal")
    st.markdown(":building_construction: :red[Painel em construção]")
    notFatOn = st.toggle("Incluir Pedidos não Faturados", help="Selecione para exibir pedidos digitados que não foram faturados")
    st.markdown("  ")

    with st.spinner('Caregando dados...'):
        tm.sleep(2)
        aba2_1, aba2_2, aba2_3 = st.tabs([":bar_chart: Gerencial - Inativo", ":male-office-worker: Supervisor - Inativo", ":man: Vendedor"])
        dias_uteis_result = str(diasUteis()).split()[-1]
        dias_decor_result = str(diasDecorridos()).split()[-1]
    # -------------------------------- # -------------------------------- # 
    with aba2_3: # Vendedor
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        du = diasUteis().values[0][0]
        dd = diasDecorridos().values[0][0]
        velocidade = dd / du
        velStr = str(math.floor(velocidade * 100))
        with col2:
            st.markdown("   ")
            st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
            st.markdown(dias_decor_result + " DIAS DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
            st.markdown(velStr + "% - VELOCIDADE", unsafe_allow_html=False, help="Velocidade de vendas realizadas no mês.")
        with col1:
            if (velocidade == 0):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/0porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0 and velocidade <= 0.10):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/10porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.10 and velocidade <= 0.20):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/20porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.20 and velocidade <= 0.30):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/30porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.30 and velocidade <= 0.40):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/40porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.40 and velocidade <= 0.50):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/50porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.50 and velocidade <= 0.60):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/60porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.60 and velocidade <= 0.70):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/70porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.70 and velocidade <= 0.80):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/80porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.80 and velocidade <= 0.90):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/90porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.90 and velocidade <= 1):
                st.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/100porcent.png', width=200, caption='VELOCIDADE')

        with col3:
            vendedorName = st.selectbox("VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key=None, help="Selecione o vendedor", placeholder="Escolha um Vendedor", label_visibility="visible")
            if vendedorName == "LEONARDO":
                vendedorCod = st.selectbox("CÓDIGO", (140,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "EDNALDO":
                vendedorCod = st.selectbox("CÓDIGO", (141,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "VAGNER":
                vendedorCod = st.selectbox("CÓDIGO", (142,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "DEIVID":
                vendedorCod = st.selectbox("CÓDIGO", (143,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "BISMARCK":
                vendedorCod = st.selectbox("CÓDIGO", (145,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "LUCIANA":
                vendedorCod = st.selectbox("CÓDIGO", (147,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "MATHEUS":
                vendedorCod = st.selectbox("CÓDIGO", (148,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "MARCIO":
                vendedorCod = st.selectbox("CÓDIGO", (150,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "LEANDRO":
                vendedorCod = st.selectbox("CÓDIGO", (151,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "REGINALDO":
                vendedorCod = st.selectbox("CÓDIGO", (152,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "ROBSON":
                vendedorCod = st.selectbox("CÓDIGO", (153,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "JOAO":
                vendedorCod = st.selectbox("CÓDIGO", (154,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "TAYANE":
                vendedorCod = st.selectbox("CÓDIGO", (155,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "MURILO":
                vendedorCod = st.selectbox("CÓDIGO", (156,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "LUCAS":
                vendedorCod = st.selectbox("CÓDIGO", (157,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "DEYVISON":
                vendedorCod = st.selectbox("CÓDIGO", (158,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "ZEFERINO":
                vendedorCod = st.selectbox("CÓDIGO", (161,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "EPAMINONDAS":
                vendedorCod = st.selectbox("CÓDIGO", (164,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "GLAUBER":
                vendedorCod = st.selectbox("CÓDIGO", (167,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "TARCISIO":
                vendedorCod = st.selectbox("CÓDIGO", (168,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "THIAGO":
                vendedorCod = st.selectbox("CÓDIGO", (169,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "FILIPE":
                vendedorCod = st.selectbox("CÓDIGO", (170,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "ROMILSON":
                vendedorCod = st.selectbox("CÓDIGO", (172,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "VALDEME":
                vendedorCod = st.selectbox("CÓDIGO", (174,), index=0, key=None, help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
        with col4:
            with st.container(height=220, border=False):
                with st.expander("O que é o Flash?"): 
                    st.write('''
                    O FLASH é um relatório primordial para o acompanhamento de vendas e remuneração.
                    Ele foi criado com objetivo de facilitar o acompanhamento do Vendedor. 
                    Em seu modelo antigo, era necessário atualizar uma planilha Excel de forma manual
                    por alguém apto. 
                    ''')
                    st.image("/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/oldFlash.png")
        # -------------------------------- # Não Faturado Incluso
        if notFatOn:
            with st.container(border=True):
                st.write("This is inside the container " * 10)
        # -------------------------------- # Faturado
        else:
            with st.container(border=True):
                st.write("This is inside the container " * 1000)