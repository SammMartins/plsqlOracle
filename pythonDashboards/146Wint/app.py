# Módulos da biblioteca padrão
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
import time as tm
import numpy as np

# Módulos Dashboards e outros
import numpy as np
import pandas as pd
import streamlit as st
import bleach 

# Módulos da aplicação/locais 
from dataset import (df1, df2, df3, df4, diasUteis, diasDecorridos, flash322RCA, flashDN322RCA, flash1464RCA, 
                     flash322RCA_semDev, flashDN1464RCA, flash1464SUP, flashDN1464SUP, flash322SUP, flashDN322SUP, 
                     top100Cli, top100Cli_comparativo, metaCalc, metaSupCalc, verbas, trocaRCA, top10CliRCA, 
                     pedErro, devolucao, campanhaDanone, inad, pedCont, estoque266, qtdVendaProd, prodSemVenda)
from grafic import grafico_vend_sup, grafico_top_rca2, grafico_top_rca8
from utils import format_number, data_semana_ini, data_semana_fim, getTableXls



meses = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARÇO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO"
}
path = '/home/ti_premium/PyDashboards/PremiumDashboards/'

# ----------------------- Configuração do dashboard
st.set_page_config(page_title="PREMIUM DASH", page_icon= path + 'Imagens/DataAdvisor.png', layout="wide", initial_sidebar_state="expanded")
                        
# Cria o Cabeçalho
header = f"""
<body>
    <header>
        <div class="header-container">
            <img src="https://sammmartins.github.io/premiumdistribuidoravca/premium_pqna.png" class="logoPremium" alt="Logo Premium">
        </div>
    </header>
</body>
"""
# ------ Estilos CSS personalizados
with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/header.css', "r") as file:
    cssHeader = file.read()
cssHeader = f"""
    <style>
        {cssHeader}
    </style>
"""

# Exibe o Cabeçalho
st.markdown(header, unsafe_allow_html=True)
st.markdown(cssHeader, unsafe_allow_html=True) # Aplicando os estilos CSS

# Função de formatação personalizada
def custom_format(x):
    return '{:,.2f}'.format(x).replace(",", "@").replace(".", ",").replace("@", ".")

# Alterar a formatação de exibição para usar ponto como separador de milhares e vírgula como separador decimal
pd.options.display.float_format = custom_format

# ----------------------- Dashboard Layout ----------------------- #
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([":dollar: VENDA", ":bar_chart: FLASH", ":dart: META", ":department_store: CLIENTES", ":bank: VERBAS", ":point_up: DEDO DURO", ":notebook:"])

with aba1:
    c1, c2 = st.columns([0.300, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/1358/1358684.png', width=180)
    with c2:
        st.title("PAINEL DE VENDAS")
        st.markdown(":page_with_curl: Faturado e não faturado semelhante a rotina 322 Winthor Totvs")
        st.markdown(":iphone: Apenas pedidos digitados pelo vendedor são exibidos")
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    aba1_1, aba1_2, aba1_3, aba1_4, aba1_5 = st.tabs([":dollar: Geral", ":bar_chart: Gráfico", ":convenience_store: Por Cliente", ":factory: Por Fornecedor", ":page_facing_up: Por Seção - Inativo :lock:"])
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #     
    with aba1_1:
        container = st.container(border=True)
        coluna1, coluna2, coluna3 = st.columns([0.6,0.5,1])
        col1, col2, col3 = st.columns([0.1, 1.1, 2])
        with container:
            with coluna1:
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    dataIni = st.date_input(":date: Data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_vend1')
                with subcoluna2:
                    dataFim = st.date_input(":date: Data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_vend2')
            with coluna2:
                df2_result = df2(dataIni, dataFim)
                if df2_result.empty:
                    st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos.")
                else:
                    sup_filtro = st.multiselect(
                        ":male-office-worker: Escolha o Supervisor", 
                        df2_result[0].unique(), 
                        key='tabela_vend3'
                    )
            with coluna3:
                c1, c2 = st.columns([0.5, 1])
                with c1:
                    st.markdown("<br>", unsafe_allow_html=True)

                    dfStyle = st.toggle(":red[Modo Tabela]", help="Selecione para exibir valores em formato de tabela")
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    # --------------- Modo Tabela --------------- #
                    if st.button("Carregar Dados", key='tabela_vend'):
                        if dfStyle:
                            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                                df1_result = df1(dataIni, dataFim)
                                df2_result = df2(dataIni, dataFim)

                            if sup_filtro and len(sup_filtro) < 2:
                                formatarMoeda = ["VENDIDO"]

                                df1_result = df1_result[df1_result[3].isin(sup_filtro)]
                                df1_result = df1_result.iloc[:, [0, 1, 2,]].rename(columns={
                                    0: "SUPERVISOR",
                                    1: "VENDIDO",
                                    2: "DN"
                                })
                                
                                
                                df2_result = df2_result[df2_result[0].isin(sup_filtro)]
                                df2_result = df2_result.iloc[:, [0, 1, 2, 3, 4]].rename(columns={
                                    0: "SUP",
                                    1: "VENDEDOR",
                                    2: "VENDIDO",
                                    3: "DN",
                                    4: "BASE"
                                })
                                df2_result = df2_result.drop(columns=["SUP", "BASE"])

                                for coluna in formatarMoeda:
                                    df1_result[coluna] = df1_result[coluna].apply(format_number)
                                    df2_result[coluna] = df2_result[coluna].apply(format_number)
                                
                                with col2:
                                    st.dataframe(df1_result)
                                    st.dataframe(df2_result)
                            else:
                                formatarMoeda = ["VENDIDO"]

                                df1_result = df1_result.iloc[:, [0, 1, 2,]].rename(columns={
                                    0: "SUPERVISOR",
                                    1: "VENDIDO",
                                    2: "DN"
                                })
                                subtotal = df1_result[["VENDIDO", "DN"]].sum()
                                subtotal_df = pd.DataFrame(subtotal).transpose()
                                subtotal_df.index = ["total"]
                                subtotal_df["SUPERVISOR"] = "Total"
                                df1_result = pd.concat([df1_result, subtotal_df])
                                
                                df2_result = df2_result.iloc[:, [0, 1, 2, 3, 4]].rename(columns={
                                    0: "SUP",
                                    1: "VENDEDOR",
                                    2: "VENDIDO",
                                    3: "DN",
                                    4: "BASE"
                                })
                                df2_result = df2_result.drop(columns=["SUP", "BASE"])

                                for coluna in formatarMoeda:
                                    df1_result[coluna] = df1_result[coluna].apply(format_number)
                                    df2_result[coluna] = df2_result[coluna].apply(format_number)

                                with col2:
                                    st.dataframe(df1_result)
                                    st.dataframe(df2_result)


                        # --------------- Modo Metric --------------- #
                        else:
                            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                                df1_result = df1(dataIni, dataFim)
                                df2_result = df2(dataIni, dataFim)

                            # -------- Tabela de Vendas por Supervisor --------
                            if sup_filtro:
                                df1_result = df1_result[df1_result[3].isin(sup_filtro)]
                                with coluna1: 
                                    for i in (df1_result[0]):
                                        st.metric("Supervisor", i)
                                with coluna2: 
                                    subcol1, subcol2 = st.columns([2,1])
                                    with subcol1:
                                        for i in df1_result[1]:
                                            st.metric("VENDIDO", format_number(i))
                                    with subcol2:
                                        for i in df1_result[2]:
                                            st.metric("DN", i)
                                if len(sup_filtro) > 1:
                                    with coluna1: 
                                        st.metric("Total", 'TOTAL')
                                    with coluna2: 
                                        subcol1, subcol2 = st.columns([2,1])
                                        with subcol1:
                                            st.metric("TOTAL VENDIDO", format_number(df1_result[1].sum()))
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
                                            st.metric("VENDIDO", format_number(i))
                                    with subcol2:
                                        for i in df1_result[2]:
                                            st.metric("DN", i)
                                with coluna1: 
                                    st.metric("Total", 'TOTAL')
                                with coluna2: 
                                        subcol1, subcol2 = st.columns([2,1])
                                        with subcol1:
                                            st.metric("TOTAL VENDIDO", format_number(df1_result[1].sum()))
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
                                            st.metric("VENDIDO", format_number(i))
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
                                            st.metric("VENDIDO", format_number(i))
                                    with subcol2:
                                        for i in df2_result[3]:
                                            st.metric("DN", i)                                                
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #
    with aba1_2:
        st.markdown("Legenda:")
        st.markdown("  1. Os dados abaixo são de vendas na semana atual.")
        st.markdown("  2. A linha branca tracejada representa o valor da média de vendas na semana atual.")
        if st.button("Carregar Dados", key='grafico_vend_sup'):
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                start_of_week = data_semana_ini()
                end_of_week = data_semana_fim()
                df2_result = df2(start_of_week, end_of_week)
                df_2 = df2_result[df2_result[df2_result.columns[0]] == 2]
                df_8 = df2_result[df2_result[df2_result.columns[0]] == 8]
            st.plotly_chart(grafico_vend_sup, use_container_width=True)
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col2: 
                st.metric(label = "MELHOR VENDEDOR", value = df2_result[1].head(1).iloc[0][6:], delta = "1º")
            with metric_col3:
                st.metric(label = "PIOR VENDEDOR", value = df2_result[1].tail(1).iloc[0][6:], delta = "-24º")
            coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.plotly_chart(grafico_top_rca8, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "MELHOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].head(1).iloc[0][6:], delta = "1º")
                with subcoluna2:
                    st.metric(label = "PIOR VENDEDOR DO SERTÃO NA SEMANA", value = df_8[1].tail(1).iloc[0][6:], delta = "-13º")
            with coluna2:
                st.plotly_chart(grafico_top_rca2, use_container_width=True)
                subcoluna1, subcoluna2 = st.columns(2)
                with subcoluna1:
                    st.metric(label = "MELHOR VENDEDOR DO SUL NA SEMANA", value = df_2[1].head(1).iloc[0][6:], delta = "1º")
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
                    dataIni_cli = st.date_input(":date: Data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_cli1')
                with subcoluna2:
                    dataFim_cli = st.date_input(":date: Data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='tabela_cli2')
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
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
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
                                st.metric("VENDIDO", format_number(i))
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #
    with aba1_4:
        container = st.container(border=False)
        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                dataIni_fornec = st.date_input(":date: Data inicial", 
                                            value=pd.to_datetime('today'), 
                                            format='DD/MM/YYYY', 
                                            key='tabela_fornec1')
            with subcol2:
                dataFim_fornec = st.date_input(":date: Data final", 
                                            value=pd.to_datetime('today'), 
                                            format='DD/MM/YYYY', 
                                            key='tabela_fornec2')
        df4_result = df4(dataIni_fornec, dataFim_fornec)
        with coluna2:
            df4_resultF = df4(dataIni_fornec, dataFim_fornec)
            if df4_resultF.empty:
                st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos.")
            else: 
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
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                        if fornec_filtro:
                            df4_result = df4_result[df4_result[1].isin([fornec_filtro])]
        if df4_resultF.empty:
            st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos.")
        else: 
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
            html_table = df4_result.to_html(index=False) # Convertendo o DataFrame para HTML
            st.markdown(html_table, unsafe_allow_html=True) # Exibindo a tabela no Streamlit
# -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #     
with aba2:
    c1, c2 = st.columns([0.300, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/7890/7890470.png', width=180)
    with c2:
        st.title("RELATÓRIO FLASH")
        st.markdown(":rocket: Um painel completo sobre seu :blue[desempenho] de vendas")
        st.markdown(":moneybag: Tenha controle sobre sua :green[remuneração] mensal")
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    col_1, col_2 = st.columns([0.70, 1])
    with col_1:
        with st.expander("SELEÇÃO DE PARÂMETROS"): 
            notFatOn = st.toggle(":red[CONSIDERAR PEDIDOS NÃO FATURADOS NO RESULTADO]", help="Selecione para exibir pedidos digitados que não foram faturados")
            if notFatOn == True:
                devOn = st.toggle(":red[ABATER DEVOLUÇÃO DO RESULTADO]", help="Selecione para abater devoluções dos pedidos não faturados.", value=True)
            
    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
        tm.sleep(2)
        aba2_1, aba2_2, aba2_3 = st.tabs([":bar_chart: :red[Gerencial - Inativo]", ":male-office-worker: :blue[Supervisor]", ":man: :green[Vendedor]"])
        dias_uteis_result = str(diasUteis()).split()[-1]
        dias_decor_result = str(diasDecorridos()).split()[-1]
    # -------------------------------- GERENCIAL -------------------------------- # -------------------------------- #
    with aba2_1:
        st.title(":building_construction: :red[Painel em construção]")
    # -------------------------------- SUPERVISOR -------------------------------- # -------------------------------- #
    with aba2_2:
        col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1.60])
        du = diasUteis().values[0][0]
        dd = diasDecorridos().values[0][0]
        velocidade = dd / du
        velStr = str(math.floor(velocidade * 100)) 
        # ------ Estilos CSS personalizados
        with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
            flash_css = file.read()
        css = f"""
            <style>
                {flash_css}
            </style>
        """
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
            st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
            st.markdown(velStr + "% - VELOCIDADE", unsafe_allow_html=False, help="Velocidade de vendas realizadas no mês.")
        with col1:
            if (velocidade == 0):
                st.image(path + 'Imagens/0porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0 and velocidade <= 0.10):
                st.image(path + 'Imagens/10porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.10 and velocidade <= 0.20):
                st.image(path + 'Imagens/20porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.20 and velocidade <= 0.30):
                st.image(path + 'Imagens/30porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.30 and velocidade <= 0.40):
                st.image(path + 'Imagens/40porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.40 and velocidade <= 0.50):
                st.image(path + 'Imagens/50porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.50 and velocidade <= 0.60):
                st.image(path + 'Imagens/60porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.60 and velocidade <= 0.70):
                st.image(path + 'Imagens/70porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.70 and velocidade <= 0.80):
                st.image(path + 'Imagens/80porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.80 and velocidade <= 0.90):
                st.image(path + 'Imagens/90porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.90 and velocidade <= 1):
                st.image(path + 'Imagens/100porcent.png', width=200, caption='VELOCIDADE')

        with col3:
            supName = st.selectbox(":male-office-worker: SUPERVISOR", ("ADAILTON", "VILMAR JR"), index=0, key='sup', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
            if supName == "ADAILTON":
                supCod = st.selectbox("CÓDIGO WINTHOR", (2,),index=0, key='adailton', help="Código de Supervisor preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif supName == "VILMAR JR":
                supCod = st.selectbox("CÓDIGO WINTHOR", (8,),index=0, key='vilmar', help="Código de Supervisor preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            else:
                supCod = st.selectbox("ERRO", (0,),index=0, key='erro', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
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
        
        # ------------------ Faturado Apenas ------------------
        if notFatOn == False:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Faturado", help="Apenas pedidos faturados. Essa opção trás um resultados real das vendas. Sempre abatendo devoluções.")
            with col1:
                if st.button("CARREGAR", key="flash1464SUP"):
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                        # --------------- FAT -----------------------
                        flash_result = flash1464SUP(supCod)
                        # --------------- DN  -----------------------
                        formatarPorcent = ['ATINGIDO']
                        # --- DANONE
                        dnFlashDanone = flashDN1464SUP(supCod, 588)
                        if dnFlashDanone.empty:
                            dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- NESTLE
                        dnFlashNestle = flashDN1464SUP(supCod, 1841)
                        if dnFlashNestle.empty:
                            dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DANILLA
                        dnFlashDanilla = flashDN1464SUP(supCod, 1658)
                        if dnFlashDanilla.empty:
                            dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SANTA MASSA
                        dnFlashSantaMassa = flashDN1464SUP(supCod, 1623)
                        if dnFlashSantaMassa.empty:
                            dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FINI
                        dnFlashFini =flashDN1464SUP(supCod, 1488)
                        if dnFlashFini.empty:
                            dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SULMINAS
                        dnFlashSulMinas = flashDN1464SUP(supCod, 1321)
                        if dnFlashSulMinas.empty:
                            dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- GULOZITOS
                        dnFlashGulozitos = flashDN1464SUP(supCod, 1719)
                        if dnFlashGulozitos.empty:
                            dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- HYTS
                        dnFlashHyts = flashDN1464SUP(supCod, 1607)
                        if dnFlashHyts.empty:
                            dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FRUTAP
                        dnFlashFrutap = flashDN1464SUP(supCod, 1728)
                        if dnFlashFrutap.empty:
                            dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                        else:
                            dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DAFRUTA
                        dnFlashDaFruta = flashDN1464SUP(supCod, 1225)
                        if dnFlashDaFruta.empty:
                            dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Seara
                        dnFlashSeara = flashDN1464SUP(supCod, 1541)
                        if dnFlashSeara.empty:
                            dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Eco fresh
                        dnFlashEcofresh = flashDN1464SUP(supCod, 1894)
                        if dnFlashEcofresh.empty:
                            dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        
                        dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh]
                        if any(df.empty for df in dataframes):
                            st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                        else:
                            with st.container(border=False):
                                # ----------------- Formatação da tabela -----------------
                                flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                    1: "SEÇÃO",
                                    2: "OBJETIVO",
                                    3: "REALIZADO",
                                    4: "ATINGIDO",
                                    5: "TENDÊNCIA",
                                    6: " R. A. F. ",
                                    7: "NECESS. DIA",
                                    8: "MÉDIA DIA",
                                    9: "STATUS"
                                })

                                formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                for coluna in formatarMoeda:
                                    flash_result[coluna] = flash_result[coluna].apply(format_number)

                                formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                for coluna in formatarPorcent:
                                    flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                # ------ DataFrame para HTML 
                                table_html = flash_result.to_html(classes='table-style', index=False)
                                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                # --- DN
                                dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                # ----------------- Exibição da tabela -----------------
                                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                                st.markdown("<h3 class='dnH3'>TABELA FLASH SUPERVISOR</h3>", unsafe_allow_html=True) # Título da seção
                                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit 

                                # ------------- Tabela Distribuição Numérica ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown("<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA SUPERVISOR</h3>", unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFini, unsafe_allow_html=True)

                                with col2:
                                    st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                with col3:
                                    st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFrutap, unsafe_allow_html=True) 


        
        # ------------------ Não Faturado ABATENDO DEVOLUÇÃO ------------------
        else:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Não Faturado", help="Pedidos digitados que não foram faturados. Abatendo devoluções.")
            with col1:
                if st.button("CARREGAR", key="flash1464SUPnotFat"):
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                        # --------------- FAT -----------------------
                        flash_result = flash322SUP(supCod)
                        # --------------- DN  -----------------------
                        formatarPorcent = ['ATINGIDO']
                        # --- DANONE
                        dnFlashDanone = flashDN322SUP(supCod, 588)
                        if dnFlashDanone.empty:
                            dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100)) 
                        # --- NESTLE
                        dnFlashNestle = flashDN322SUP(supCod, 1841)
                        if dnFlashNestle.empty:
                            dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DANILLA
                        dnFlashDanilla = flashDN322SUP(supCod, 1658)
                        if dnFlashDanilla.empty:
                            dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SANTA MASSA
                        dnFlashSantaMassa = flashDN322SUP(supCod, 1623)
                        if dnFlashSantaMassa.empty:
                            dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FINI
                        dnFlashFini = flashDN322SUP(supCod, 1488)
                        if dnFlashFini.empty:
                            dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SULMINAS
                        dnFlashSulMinas = flashDN322SUP(supCod, 1321)
                        if dnFlashSulMinas.empty:
                            dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- GULOZITOS
                        dnFlashGulozitos = flashDN322SUP(supCod, 1719)
                        if dnFlashGulozitos.empty:
                            dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- HYTS
                        dnFlashHyts = flashDN322SUP(supCod, 1607)
                        if dnFlashHyts.empty:
                            dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FRUTAP
                        dnFlashFrutap = flashDN322SUP(supCod, 1728)
                        if dnFlashFrutap.empty:
                            dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DAFRUTA
                        dnFlashDaFruta = flashDN322SUP(supCod, 1225)
                        if dnFlashDaFruta.empty:
                            dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Seara
                        dnFlashSeara = flashDN322SUP(supCod, 1541)
                        if dnFlashSeara.empty:
                            dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Eco fresh
                        dnFlashEcofresh = flashDN322SUP(supCod, 1894)
                        if dnFlashEcofresh.empty:
                            dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))



                        dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh]
                        if any(df.empty for df in dataframes):
                            st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                        else:
                            with st.container(border=False):
                                # ----------------- Formatação da tabela -----------------
                                flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                    1: "SEÇÃO",
                                    2: "OBJETIVO",
                                    3: "REALIZADO",
                                    4: "ATINGIDO",
                                    5: "TENDÊNCIA",
                                    6: " R. A. F. ",
                                    7: "NECESS. DIA",
                                    8: "MÉDIA DIA",
                                    9: "STATUS"
                                })

                                formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                for coluna in formatarMoeda:
                                    flash_result[coluna] = flash_result[coluna].apply(format_number)

                                formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                for coluna in formatarPorcent:
                                    flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                # ------ DataFrame para HTML 
                                table_html = flash_result.to_html(classes='table-style', index=False)
                                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                # --- DN
                                dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                # ----------------- Exibição da tabela -----------------
                                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                                st.markdown("<h3 class='dnH3'>TABELA FLASH SUPERVISOR</h3>", unsafe_allow_html=True) # Título da seção
                                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit 

                                # ------------- Tabela Distribuição Numérica ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown("<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA SUPERVISOR</h3>", unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFini, unsafe_allow_html=True)

                                with col2:
                                    st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                with col3:
                                    st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFrutap, unsafe_allow_html=True) 
                    



    # -------------------------------- VENDEDOR -------------------------------- # -------------------------------- #
    with aba2_3:
        col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1.60])
        du = diasUteis().values[0][0]
        dd = diasDecorridos().values[0][0]
        velocidade = dd / du
        velStr = str(math.floor(velocidade * 100)) 
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
            st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
            st.markdown(velStr + "% - VELOCIDADE", unsafe_allow_html=False, help="Velocidade de vendas realizadas no mês.")
        with col1:
            if (velocidade == 0):
                st.image(path + 'Imagens/0porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0 and velocidade <= 0.10):
                st.image(path + 'Imagens/10porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.10 and velocidade <= 0.20):
                st.image(path + 'Imagens/20porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.20 and velocidade <= 0.30):
                st.image(path + 'Imagens/30porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.30 and velocidade <= 0.40):
                st.image(path + 'Imagens/40porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.40 and velocidade <= 0.50):
                st.image(path + 'Imagens/50porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.50 and velocidade <= 0.60):
                st.image(path + 'Imagens/60porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.60 and velocidade <= 0.70):
                st.image(path + 'Imagens/70porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.70 and velocidade <= 0.80):
                st.image(path + 'Imagens/80porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.80 and velocidade <= 0.90):
                st.image(path + 'Imagens/90porcent.png', width=200, caption='VELOCIDADE')
            elif (velocidade > 0.90 and velocidade <= 1):
                st.image(path + 'Imagens/100porcent.png', width=200, caption='VELOCIDADE')

        with col3:
            vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
            if vendedorName == "LEONARDO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (140,),index=0, key='140', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "EDNALDO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (141,),index=0, key='141', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "VAGNER":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (142,),index=0, key='142', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "DEIVID":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (143,),index=0, key='143', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "BISMARCK":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (145,),index=0, key='145', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "LUCIANA":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (147,),index=0, key='147', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "MATHEUS":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (148,),index=0, key='148', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "MARCIO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (150,),index=0, key='150', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "LEANDRO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (151,),index=0, key='151', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "REGINALDO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (152,),index=0, key='152', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "ROBSON":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (153,),index=0, key='153', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "JOAO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (154,),index=0, key='154', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "TAYANE":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (155,),index=0, key='155', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "MURILO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (156,),index=0, key='156', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "LUCAS":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (157,),index=0, key='157', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "DEYVISON":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (158,),index=0, key='158', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "ZEFERINO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (161,),index=0, key='161', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "EPAMINONDAS":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (164,),index=0, key='164', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "GLAUBER":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (167,),index=0, key='167', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "TARCISIO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (168,),index=0, key='168', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "THIAGO":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (169,),index=0, key='169', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "FILIPE":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (170,),index=0, key='170', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "ROMILSON":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (172,),index=0, key='172', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            elif vendedorName == "VALDEME":
                vendedorCod = st.selectbox("CÓDIGO WINTHOR", (174,),index=0, key='174', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
            else:
                vendedorCod = st.selectbox("ERRO", (0,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
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
        # -------------------------------- Faturado Apenas ----------------------------------------------
        if notFatOn == False:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Faturado", help="Apenas pedidos faturados. Essa opção trás um resultados real das vendas. Sempre abatendo devoluções.")
            with col1:
                if st.button("CARREGAR"):
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                        # --------------- FAT -----------------------
                        flash_result = flash1464RCA(vendedorCod)
                        # --------------- Troca ---------------------
                        troca_result = trocaRCA(vendedorCod)
                        # --------------- DN  -----------------------
                        formatarPorcent = ['ATINGIDO']
                        # --- DANONE
                        dnFlashDanone = flashDN1464RCA(vendedorCod, 588)
                        if dnFlashDanone.empty:
                            dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- NESTLÉ
                        dnFlashNestle = flashDN1464RCA(vendedorCod, 1841)
                        if dnFlashNestle.empty:
                            dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DANILLA
                        dnFlashDanilla = flashDN1464RCA(vendedorCod, 1658) # Problema com indústrias com mais de 1 CNPJ
                        if dnFlashDanilla.empty:
                            dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SANTA MASSA
                        dnFlashSantaMassa = flashDN1464RCA(vendedorCod, 1623)
                        if dnFlashSantaMassa.empty:
                            dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FINI
                        dnFlashFini = flashDN1464RCA(vendedorCod, 1488)
                        if dnFlashFini.empty:
                            dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SULMINAS
                        dnFlashSulMinas = flashDN1464RCA(vendedorCod, 1321)
                        if dnFlashSulMinas.empty:
                            dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- GULOZITOS
                        dnFlashGulozitos = flashDN1464RCA(vendedorCod, 1719)
                        if dnFlashGulozitos.empty:
                            dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- HYTS
                        dnFlashHyts = flashDN1464RCA(vendedorCod, 1607)
                        if dnFlashHyts.empty:
                            dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FRUTAP
                        dnFlashFrutap = flashDN1464RCA(vendedorCod, 1728)
                        if dnFlashFrutap.empty:
                            dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                        else:
                            dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DAFRUTA
                        dnFlashDaFruta = flashDN1464RCA(vendedorCod, 1225)
                        if dnFlashDaFruta.empty:
                            dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Seara
                        dnFlashSeara = flashDN1464RCA(vendedorCod, 1541)
                        if dnFlashSeara.empty:
                            dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Eco fresh
                        dnFlashEcofresh = flashDN1464RCA(vendedorCod, 1894)
                        if dnFlashEcofresh.empty:
                            dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        
                        dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh, troca_result]
                        if any(df.empty for df in dataframes):
                            st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                        else:
                            with st.container(border=False):
                                # ----------------- Formatação da tabela -----------------
                                flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                    1: "SEÇÃO",
                                    2: "OBJETIVO",
                                    3: "REALIZADO",
                                    4: "ATINGIDO",
                                    5: "TENDÊNCIA",
                                    6: " R. A. F. ",
                                    7: "NECESS. DIA",
                                    8: "MÉDIA DIA",
                                    9: "STATUS"
                                })

                                formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                for coluna in formatarMoeda:
                                    flash_result[coluna] = flash_result[coluna].apply(format_number)

                                formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                for coluna in formatarPorcent:
                                    flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                # ------ Troca
                                troca_result = troca_result.iloc[:, [1, 2,]].rename(columns={
                                    1: " ",
                                    2: "↓"
                                })

                                # ------ DataFrame para HTML 
                                table_html = flash_result.to_html(classes='table-style', index=False)
                                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                # --- TROCA
                                troca_result = troca_result.to_html(classes='table-dn', index=False)
                                # --- DN
                                dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                # ------ Estilos CSS personalizados
                                with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                                    flash_css = file.read()
                                css = f"""
                                <style>
                                    {flash_css}
                                </style>
                                """

                                # ----------------- Exibição da tabela -----------------
                                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

                                st.markdown(f"<h3 class='dnH3'>TABELA FLASH VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção

                                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit  

                                # ------------- Tabela Distribuição Numérica ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown(f"<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFini, unsafe_allow_html=True)

                                with col2:
                                    st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                with col3:
                                    st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFrutap, unsafe_allow_html=True)

                                # ------------- ITENS DE PERFORMANCE ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown(f"<h3 class='dnH3'>ITENS DE PERFORMANCE VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)
                                col4, col5, col6 = st.columns(3)
                                with col5:
                                    st.markdown(f"<p class='dn'>ÍNDICE TROCA {vendedorName}</p>", unsafe_allow_html=True)
                                    st.markdown(troca_result, unsafe_allow_html=True)





        # -------------------------------- Não Faturado incluso ABATENDO DEVOLUÇÃO ----------------------------------
        elif notFatOn == True and devOn == True:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Todos", help="Todos os pedidos digitados abatendo devolução (se houver). Essa opção apresenta um resultados mais completo das vendas, mas com sofrerá alterações caso algum pedido não seja faturado, cancelado, ou sofra algum corte.")
            with col1:
                if st.button("CARREGAR"):
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                        # --------------- NOTFAT -----------------------
                        flash_result = flash322RCA_semDev(vendedorCod)
                        # --------------- Troca ---------------------
                        troca_result = trocaRCA(vendedorCod)
                        # --------------- DN ---------------------------
                        formatarPorcent = ['ATINGIDO']
                        # --- DANONE
                        dnFlashDanone = flashDN322RCA(vendedorCod, 588)
                        if dnFlashDanone.empty:
                            dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- NESTLÉ
                        dnFlashNestle = flashDN322RCA(vendedorCod, 1841)
                        if dnFlashNestle.empty:
                            dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DANILLA
                        dnFlashDanilla = flashDN322RCA(vendedorCod, 1658) # Problema com indústrias com mais de 1 CNPJ
                        if dnFlashDanilla.empty:
                            dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SANTA MASSA
                        dnFlashSantaMassa = flashDN322RCA(vendedorCod, 1623)
                        if dnFlashSantaMassa.empty:
                            dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FINI
                        dnFlashFini = flashDN322RCA(vendedorCod, 1488)
                        if dnFlashFini.empty:
                            dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SULMINAS
                        dnFlashSulMinas = flashDN322RCA(vendedorCod, 1321)
                        if dnFlashSulMinas.empty:
                            dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- GULOZITOS
                        dnFlashGulozitos = flashDN322RCA(vendedorCod, 1719)
                        if dnFlashGulozitos.empty:
                            dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- HYTS
                        dnFlashHyts = flashDN322RCA(vendedorCod, 1607)
                        if dnFlashHyts.empty:
                            dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FRUTAP
                        dnFlashFrutap = flashDN322RCA(vendedorCod, 1728)
                        if dnFlashFrutap.empty:
                            dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                        else:
                            dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DAFRUTA
                        dnFlashDaFruta = flashDN322RCA(vendedorCod, 1225)
                        if dnFlashDaFruta.empty:
                            dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Seara
                        dnFlashSeara = flashDN322RCA(vendedorCod, 1541)
                        if dnFlashSeara.empty:
                            dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Eco fresh
                        dnFlashEcofresh = flashDN322RCA(vendedorCod, 1894)
                        if dnFlashEcofresh.empty:
                            dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        
                        dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh, troca_result]
                        if any(df.empty for df in dataframes):
                            st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                        else:
                            with st.container(border=False):
                                # ----------------- Formatação da tabela -----------------
                                flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                    1: "SEÇÃO",
                                    2: "OBJETIVO",
                                    3: "REALIZADO",
                                    4: "ATINGIDO",
                                    5: "TENDÊNCIA",
                                    6: " R. A. F. ",
                                    7: "NECESS. DIA",
                                    8: "MÉDIA DIA",
                                    9: "STATUS"
                                })

                                formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                for coluna in formatarMoeda:
                                    flash_result[coluna] = flash_result[coluna].apply(format_number)

                                formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                for coluna in formatarPorcent:
                                    flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                # ------ Troca
                                troca_result = troca_result.iloc[:, [1, 2,]].rename(columns={
                                    1: " ",
                                    2: "↓"
                                })


                                # ------ DataFrame para HTML 
                                table_html = flash_result.to_html(classes='table-style', index=False)
                                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                # --- TROCA
                                troca_result = troca_result.to_html(classes='table-dn', index=False)
                                # --- DN
                                dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                # ------ Estilos CSS personalizados
                                with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                                    flash_css = file.read()
                                css = f"""
                                <style>
                                    {flash_css}
                                </style>
                                """

                                # ----------------- Exibição da tabela -----------------
                                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

                                st.markdown(f"<h3 class='dnH3'>TABELA FLASH VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção

                                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit  

                                # ------------- Tabela Distribuição Numérica ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown(f"<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFini, unsafe_allow_html=True)

                                with col2:
                                    st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                with col3:
                                    st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFrutap, unsafe_allow_html=True)

                                # ------------- ITENS DE PERFORMANCE ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown(f"<h3 class='dnH3'>ITENS DE PERFORMANCE VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)
                                col4, col5, col6 = st.columns(3)
                                with col5:
                                    st.markdown(f"<p class='dn'>ÍNDICE TROCA {vendedorName}</p>", unsafe_allow_html=True)
                                    st.markdown(troca_result, unsafe_allow_html=True)                                    


        # -------------------------------- Não Faturado incluso COM DEVOLUÇÃO ----------------------------------
        else:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Irreal", help="Todos os pedidos digitados sem abater devolução. Essa opção apresenta um resultados mais completo das vendas, mas com sofrerá alterações caso algum pedido não seja faturado, cancelado, ou sofra algum corte.")
            with col1:
                if st.button("CARREGAR"):
                    with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                        # --------------- NOTFAT -----------------------
                        flash_result = flash322RCA(vendedorCod)
                        # --------------- DN ---------------------------
                        formatarPorcent = ['ATINGIDO']
                        # --- DANONE
                        dnFlashDanone = flashDN322RCA(vendedorCod, 588)
                        if dnFlashDanone.empty:
                            dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- NESTLÉ
                        dnFlashNestle = flashDN322RCA(vendedorCod, 1841)
                        if dnFlashNestle.empty:
                            dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DANILLA
                        dnFlashDanilla = flashDN322RCA(vendedorCod, 1658) # Problema com indústrias com mais de 1 CNPJ
                        if dnFlashDanilla.empty:
                            dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SANTA MASSA
                        dnFlashSantaMassa = flashDN322RCA(vendedorCod, 1623)
                        if dnFlashSantaMassa.empty:
                            dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FINI
                        dnFlashFini = flashDN322RCA(vendedorCod, 1488)
                        if dnFlashFini.empty:
                            dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- SULMINAS
                        dnFlashSulMinas = flashDN322RCA(vendedorCod, 1321)
                        if dnFlashSulMinas.empty:
                            dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- GULOZITOS
                        dnFlashGulozitos = flashDN322RCA(vendedorCod, 1719)
                        if dnFlashGulozitos.empty:
                            dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- HYTS
                        dnFlashHyts = flashDN322RCA(vendedorCod, 1607)
                        if dnFlashHyts.empty:
                            dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- FRUTAP
                        dnFlashFrutap = flashDN322RCA(vendedorCod, 1728)
                        if dnFlashFrutap.empty:
                            dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                        else:
                            dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- DAFRUTA
                        dnFlashDaFruta = flashDN322RCA(vendedorCod, 1225)
                        if dnFlashDaFruta.empty:
                            dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Seara
                        dnFlashSeara = flashDN322RCA(vendedorCod, 1541)
                        if dnFlashSeara.empty:
                            dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        # --- Eco fresh
                        dnFlashEcofresh = flashDN322RCA(vendedorCod, 1894)
                        if dnFlashEcofresh.empty:
                            dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                        else:
                            dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                            for coluna in formatarPorcent:
                                dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        
                        dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh]
                        if any(df.empty for df in dataframes):
                            st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                        else:
                            with st.container(border=False):
                                # ----------------- Formatação da tabela -----------------
                                flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                    1: "SEÇÃO",
                                    2: "OBJETIVO",
                                    3: "REALIZADO",
                                    4: "ATINGIDO",
                                    5: "TENDÊNCIA",
                                    6: " R. A. F. ",
                                    7: "NECESS. DIA",
                                    8: "MÉDIA DIA",
                                    9: "STATUS"
                                })

                                formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                for coluna in formatarMoeda:
                                    flash_result[coluna] = flash_result[coluna].apply(format_number)

                                formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                for coluna in formatarPorcent:
                                    flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                # ------ DataFrame para HTML 
                                table_html = flash_result.to_html(classes='table-style', index=False)
                                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>')
                                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>')
                                table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                # --- DN
                                dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                # ------ Estilos CSS personalizados
                                with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                                    flash_css = file.read()
                                css = f"""
                                <style>
                                    {flash_css}
                                </style>
                                """

                                # ----------------- Exibição da tabela -----------------
                                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

                                st.markdown("<h3 class='dnH3'>TABELA FLASH</h3>", unsafe_allow_html=True) # Título da seção

                                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit  

                                # ------------- Tabela Distribuição Numérica ----------
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown("<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA</h3>", unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFini, unsafe_allow_html=True)

                                with col2:
                                    st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                with col3:
                                    st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                    st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                    st.markdown(dnFlashFrutap, unsafe_allow_html=True)


# ------------------------------- META --------------------------------------- #
with aba3:
    c1, c2 = st.columns([0.300, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/8213/8213190.png', width=180)
    with c2:
        st.title("CONSULTAR META")
        st.markdown("Painel destinado a :blue[CONSULTA] das metas")
        st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    aba3_1, aba3_2 = st.tabs(["VENDEDOR", "SUPERVISOR"])
    # ------------------------------- VENDEDOR --------------------------------------- #
    with aba3_1:
        col1, col2, col3, col4 = st.columns([0.55, 1, 1, 2])
        with col1:
                st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
                st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
        with col2:
                vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_2', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                if vendedorName == "LEONARDO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (140,),index=0, key='140_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EDNALDO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (141,),index=0, key='141_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VAGNER":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (142,),index=0, key='142_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEIVID":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (143,),index=0, key='143_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "BISMARCK":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (145,),index=0, key='145_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCIANA":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (147,),index=0, key='147_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MATHEUS":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (148,),index=0, key='148_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MARCIO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (150,),index=0, key='150_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LEANDRO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (151,),index=0, key='151_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "REGINALDO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (152,),index=0, key='152_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROBSON":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (153,),index=0, key='153_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "JOAO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (154,),index=0, key='154_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TAYANE":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (155,),index=0, key='155_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MURILO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (156,),index=0, key='156_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCAS":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (157,),index=0, key='157_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEYVISON":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (158,),index=0, key='158_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ZEFERINO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (161,),index=0, key='161_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EPAMINONDAS":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (164,),index=0, key='164_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "GLAUBER":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (167,),index=0, key='167_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TARCISIO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (168,),index=0, key='168_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "THIAGO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (169,),index=0, key='169_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "FILIPE":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (170,),index=0, key='170_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROMILSON":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (172,),index=0, key='172_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VALDEME":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (174,),index=0, key='174_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                else:
                    vendedorCod = st.selectbox("ERRO", (0,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("Como é calculada a meta?", expanded=False):
                st.markdown("A meta é calculada com base no histórico de vendas do vendedor dos ultimos 2 meses e considerando a quantidade de dias úteis desses meses.")
        if st.button("CARREGAR", key=2):
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                # --------------------------- DADOS META --------------------------- #
                meta_result = metaCalc(vendedorCod)
                if meta_result.empty:
                    st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                else:
                    with st.container(border=False):
                        # ----------------- Formatação da tabela -----------------
                        meta_result = meta_result.iloc[:, [0, 1, 2, 3, 4, 5, 6]].rename(columns={
                            0: "CODSEC",
                            1: "SECAO",
                            2: "CODSUPERVISOR",
                            3: "RCA",
                            4: "TOTAL VENDIDO",
                            5: "META MÊS",
                            6: "META DIA"
                        })

                        # -------- Formatação para Metric
                        meta_mes_total = format_number(meta_result["META MÊS"].sum())
                        meta_dia_total = format_number(meta_result["META DIA"].sum())

                        formatarMoeda = ["TOTAL VENDIDO", "META MÊS", "META DIA"]
                        for coluna in formatarMoeda:
                            meta_result[coluna] = meta_result[coluna].apply(format_number)

                        meta_result = meta_result.drop(columns=["CODSUPERVISOR","RCA"]) # Removendo colunas desnecessárias

                        # ------ DataFrame para HTML 
                        table_html = meta_result.to_html(classes='table-style', index=False)
                        table_html = table_html.replace('<td>', '<td class="linha-table">')

                        # ------ Estilos CSS personalizados
                        with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                            cli_css = file.read()
                        css = f"""
                        <style>
                            {cli_css}
                        </style>
                        """       
                        # ----------------- Exibição da tabela -----------------
                        mes_atual = datetime.now().month # Obtém o mês atual
                        mes = meses[mes_atual] # Obtém o nome do mês atual
                        st.markdown(f"<h3 class='dnH3'>META {mes} VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção

                        st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                        st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                        
                        # Cria a tabela HTML
                        html_table = f"""
                        <table class='table-style'>
                            <tr>
                                <th>META TOTAL</th>
                                <th>META DIA TOTAL</th>
                            </tr>
                            <tr>
                                <td class="linha-table">{meta_mes_total}</td>
                                <td class="linha-table">{meta_dia_total}</td>
                            </tr>
                        </table>
                        """
                        # Exibe a tabela HTML
                        st.markdown(html_table, unsafe_allow_html=True)

    with aba3_2:
        col1, col2, col3, col4 = st.columns([0.55, 1, 1, 2])
        with col1:
            st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
            st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
        with col2:
            supName = st.selectbox(":male-office-worker: SUPERVISOR", ("ADAILTON", "VILMAR JR"), index=0, key='sup_2', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
            if supName == "ADAILTON":
                with col3:
                    supCod = st.selectbox("CÓDIGO WINTHOR", (2,), index=0, key='adailton_2', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
            elif supName == "VILMAR JR":
                with col3:
                    supCod = st.selectbox("CÓDIGO WINTHOR", (8,), index=0, key='vilmar_2', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
            else:
                with col3:
                    supCod = st.selectbox("ERRO", (0,), index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("Como é calculada a meta?", expanded=False):
                st.markdown("A meta é calculada com base no histórico de vendas do vendedor dos ultimos 2 meses e considerando a quantidade de dias úteis desses meses.")
        if st.button("CARREGAR", key=3):
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                # --------------------------- DADOS META --------------------------- #
                meta_result = metaSupCalc(supCod)
                if meta_result.empty:
                    st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                else:
                    with st.container(border=False):
                        # ----------------- Formatação da tabela -----------------
                        meta_result = meta_result.iloc[:, [0, 1, 2, 3, 4, 5]].rename(columns={
                            0: "CODSEC",
                            1: "SECAO",
                            2: "CODSUPERVISOR",
                            3: "TOTAL VENDIDO",
                            4: "META MÊS",
                            5: "META DIA"
                        })

                        # -------- Formatação para Metric
                        meta_mes_total = format_number(meta_result["META MÊS"].sum())
                        meta_dia_total = format_number(meta_result["META DIA"].sum())

                        formatarMoeda = ["TOTAL VENDIDO", "META MÊS", "META DIA"]
                        for coluna in formatarMoeda:
                            meta_result[coluna] = meta_result[coluna].apply(format_number)

                        meta_result = meta_result.drop(columns=["CODSUPERVISOR"]) # Removendo colunas desnecessárias

                        # ------ DataFrame para HTML 
                        table_html = meta_result.to_html(classes='table-style', index=False)
                        table_html = table_html.replace('<td>', '<td class="linha-table">')

                        # ------ Estilos CSS personalizados
                        with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                            cli_css = file.read()
                        css = f"""
                        <style>
                            {cli_css}
                        </style>
                        """       
                        # ----------------- Exibição da tabela -----------------
                        mes_atual = datetime.now().month # Obtém o mês atual
                        mes = meses[mes_atual] # Obtém o nome do mês atual
                        st.markdown(f"<h3 class='dnH3'>META {mes} SUPERVISOR {supName}</h3>", unsafe_allow_html=True) # Título da seção

                        st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                        st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                        
                        # Cria a tabela HTML
                        html_table = f"""
                        <table class='table-style'>
                            <tr>
                                <th>META TOTAL</th>
                                <th>META DIA TOTAL</th>
                            </tr>
                            <tr>
                                <td class="linha-table">{meta_mes_total}</td>
                                <td class="linha-table">{meta_dia_total}</td>
                            </tr>
                        </table>
                        """
                        # Exibe a tabela HTML
                        st.markdown(html_table, unsafe_allow_html=True)


# --------------------------- CLIENTES ----------------------------------- #
with aba4:
    c1, c2 = st.columns([0.300, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/5434/5434400.png', width=180)
    with c2:
        st.title("RELATÓRIO CLIENTES")
        st.markdown("Painel destinado a :blue[análise detalhada] dos principais clientes")
        st.markdown("<br>", unsafe_allow_html=True)
    aba4_1, aba4_2 = st.tabs([':convenience_store: GERAL', ':man: POR VENDEDOR'])
    # --------------------------------- GERAL --------------------------------- #
    with aba4_1:
        st.header(":top: 100 CLIENTES")
        dtIni = datetime.today() - timedelta(days=60)
        dtIni = dtIni.strftime("%d/%m/%Y")
        st.caption(" - " + ":blue[60] DIAS CORRIDOS:" + f" :blue[{dtIni}] ATÉ HOJE")
        st.markdown("    ")

        # --------------------------------- RANK TOP 100 --------------------------------- #
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR RANK TOP 100"):
            # --------------------- Cabeçalho de itens ---------------------
            col1, col2, col3, col4 = st.columns([1, 1, 2, 0.55])
            with col1:
                supName = st.selectbox(":male-office-worker: SUPERVISOR", ("TODOS", "ADAILTON", "VILMAR JR"), index=0, key='sup_3', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                if supName == "ADAILTON":
                    with col2:
                        supCod = st.selectbox("CÓDIGO WINTHOR", (2,), index=0, key='adailton_3', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                        supOffOn = "IN"     # -- Está em 2
                elif supName == "VILMAR JR":
                    with col2:
                        supCod = st.selectbox("CÓDIGO WINTHOR", (8,), index=0, key='vilmar_3', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                        supOffOn = "IN"     # -- Está em 8
                elif supName == "TODOS":
                    with col2:
                        supCod = st.selectbox("CÓDIGO WINTHOR", (0,), index=0, key='todos_3', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                        supOffOn = "NOT IN" # -- Não está em 0
                else:
                    with col2:
                        supCod = st.selectbox("ERRO", (0,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
            
            with col3:
                st.write("   ")
                st.write("   ")
                sorveteOn = st.toggle(":blue[CONSIDERAR PEDIDOS DE SORVETES NO RESULTADO]", help="Selecione para EXIBIR Sorvete e Açaí no resultado", key='sorveteOn')
            st.divider()

            # --------------- Dados Top CLI -----------------------
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                if sorveteOn == False:
                    topCli_result = top100Cli(supCod, 0, 0, 0, supOffOn) #-- Sorvete NÃO Incluso
                else:
                    topCli_result = top100Cli(supCod, 120430, 120432, 120427, supOffOn) #-- Sorvete Incluso

            # ----------------- Formatação da tabela -----------------
            topCli_result = topCli_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7]].rename(columns={
                0: "RANK",
                1: "CODCLI",
                2: "CLIENTE",
                3: "VENDEDOR",
                4: "FATURADO",
                5: "MÉDIA",
                6: "BONIFICADO",
                7: "% BNF"
            })

            formatarMoeda = ["FATURADO", "BONIFICADO", "MÉDIA"]
            for coluna in formatarMoeda:
                topCli_result[coluna] = topCli_result[coluna].apply(format_number)

            formatarPorcent = ["% BNF"]
            for coluna in formatarPorcent:
                topCli_result[coluna] = topCli_result[coluna].apply(lambda x: '{:.1f}%'.format(x))
            
            # ------ DataFrame para HTML 
            table_html = topCli_result.to_html(classes='table-styleCli', index=False)

            for i in range(1, 4): # Definindo a classe rank para aplicar estilos
                table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank{i}">{i}</td>')
            for i in range(4, 11):
                table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank">{i}</td>')
            

            # ------ Estilos CSS personalizados
            with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                cli_css = file.read()
            css = f"""
            <style>
                {cli_css}
            </style>
            """

            # ----------------- Exibição da tabela -----------------
            st.markdown("<h3 class='dnH3'>RANK TOP 100 CLIENTES</h3>", unsafe_allow_html=True) # Título da seção

            st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

            st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS



        # --------------------------------- COMPARATIVO --------------------------------- #
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR RANK TOP 100 - COMPARATIVO"):
            # --------------------- Cabeçalho de itens ---------------------
            col1, col2, col3, col4 = st.columns([1, 1, 2, 0.55])
            with col1:
                supName = st.selectbox(":male-office-worker: SUPERVISOR", ("TODOS", "ADAILTON", "VILMAR JR"), index=0, key='sup_4', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                if supName == "ADAILTON":
                    with col2:
                        supCod = st.selectbox("CÓDIGO WINTHOR", (2,), index=0, key='adailton_4', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                        supOffOn = "IN"     # -- Está em 2
                elif supName == "VILMAR JR":
                    with col2:
                        supCod = st.selectbox("CÓDIGO WINTHOR", (8,), index=0, key='vilmar_4', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                        supOffOn = "IN"     # -- Está em 8
                elif supName == "TODOS":
                    with col2:
                        supCod = st.selectbox("CÓDIGO WINTHOR", (0,), index=0, key='todos_4', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                        supOffOn = "NOT IN" # -- Não está em 0
                else:
                    with col2:
                        supCod = st.selectbox("ERRO", (0,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
            
            with col3:
                st.write("   ")
                st.write("   ")
                sorveteOn = st.toggle(":blue[CONSIDERAR PEDIDOS DE SORVETES NO RESULTADO]", help="Selecione para EXIBIR Sorvete e Açaí no resultado", key='sorveteOn2')
            st.divider()

            # --------------- Dados Top CLI -----------------------
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                if sorveteOn == False:
                    topCli_result = top100Cli(supCod, 0, 0, 0, supOffOn) #-- Sorvete NÃO Incluso
                    topCliOld_result = top100Cli_comparativo(supCod, 0, 0, 0, supOffOn)
                else:
                    topCli_result = top100Cli(supCod, 120430, 120432, 120427, supOffOn) #-- Sorvete Incluso
                    topCliOld_result = top100Cli_comparativo(supCod, 120430, 120432, 120427, supOffOn)
                

            # ----------------- Formatação da tabela -----------------
            topCli_result = topCli_result.iloc[:, [0, 1, 2, 3, 4, 5, 6,]].rename(columns={
                0: "RANK",
                1: "CODCLI",
                2: "CLIENTE",
                3: "VENDEDOR",
                4: "ANO ATUAL",
                5: "INVESTIDO",
                6: "% INVESTIDA"
            })

            topCliOld_result = topCliOld_result.rename(columns={1: "CODCLI", 4: "ANO ANTERIOR"})

            # Seleção das colunas desejadas de cada dataframe para unir
            topCli_result_selected = topCli_result.iloc[:, [0, 1, 2, 3, 4]]
            topCliOld_result_selected = topCliOld_result.iloc[:, [1, 4]]

            # Une os dois dataframes
            merge_result = pd.merge(topCli_result_selected, topCliOld_result_selected, on="CODCLI")

            # Adiciona uma nova coluna 'GAP' que calcula a diferença entre as colunas 'ANO ATUAL' e 'ANO ANTERIOR'
            merge_result['GAP'] = merge_result['ANO ATUAL'] - merge_result['ANO ANTERIOR']
            # Adiciona uma nova coluna 'TENDENCIA' que compara as colunas 'ANO ATUAL' e 'ANO ANTERIOR'
            merge_result['TENDENCIA'] = np.where(merge_result['ANO ATUAL'] > merge_result['ANO ANTERIOR'], '↑↑↑', '↓↓↓')

            # ------ Formatar Linha
            formatarMoeda = ["ANO ATUAL", "ANO ANTERIOR", 'GAP']
            for coluna in formatarMoeda:
                merge_result[coluna] = merge_result[coluna].apply(format_number)
            
            # ------ DataFrame para HTML 
            table_html = merge_result.to_html(classes='table-style', index=False)

            for i in range(1, 4): # Definindo a classe rank para aplicar estilos
                table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank{i}">{i}</td>')
            for i in range(4, 11):
                table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank">{i}</td>')

            table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivoCli">↑↑↑</td>')
            table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativoCli">↓↓↓</td>')
            

            # ------ Estilos CSS personalizados
            with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                cli_css = file.read()
            css = f"""
            <style>
                {cli_css}
            </style>
            """

            # ----------------- Exibição da tabela -----------------
            st.markdown("<h3 class='dnH3'>RANK TOP 100 CLIENTES - COMPARATIVO</h3>", unsafe_allow_html=True) # Título da seção

            st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

            st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS



    # ------------------------------- POR VENDEDOR ------------------------------ #
    with aba4_2:
        # --------------------------- RANK TOP 10 RCA --------------------------- #
        col1, col2, col3, col4 = st.columns([1.90, 0.75, 0.75, 2.10])
        with col2:
                vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_3', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                if vendedorName == "LEONARDO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (140,),index=0, key='140_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EDNALDO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (141,),index=0, key='141_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VAGNER":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (142,),index=0, key='142_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEIVID":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (143,),index=0, key='143_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "BISMARCK":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (145,),index=0, key='145_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCIANA":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (147,),index=0, key='147_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MATHEUS":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (148,),index=0, key='148_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MARCIO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (150,),index=0, key='150_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LEANDRO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (151,),index=0, key='151_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "REGINALDO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (152,),index=0, key='152_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROBSON":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (153,),index=0, key='153_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "JOAO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (154,),index=0, key='154_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TAYANE":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (155,),index=0, key='155_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MURILO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (156,),index=0, key='156_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCAS":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (157,),index=0, key='157_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEYVISON":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (158,),index=0, key='158_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ZEFERINO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (161,),index=0, key='161_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EPAMINONDAS":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (164,),index=0, key='164_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "GLAUBER":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (167,),index=0, key='167_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TARCISIO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (168,),index=0, key='168_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "THIAGO":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (169,),index=0, key='169_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "FILIPE":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (170,),index=0, key='170_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROMILSON":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (172,),index=0, key='172_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VALDEME":
                    with col3:
                        vendedorCod = st.selectbox("CÓDIGO WINTHOR", (174,),index=0, key='174_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                else:
                    vendedorCod = st.selectbox("ERRO", (0,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
        # --------------- Dados Top CLI -----------------------
        with st.expander(f"RANK TOP 10 - {vendedorName}"):
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                # ------------- RANK TOP 10 ------------ #
                topCli2_result = top10CliRCA(vendedorCod)

                # ------------- Formatação da tabela --- #
                topCli2_result = topCli2_result.iloc[:, [0, 1, 2, 3, 4, 5, ]].rename(columns={
                    0: "RANK",
                    1: "CODCLI",
                    2: "CLIENTE",
                    3: "FATURADO 60 DIAS",
                    4: "BONIFICADO",
                    5: "% BONIFICADO"
                })

                # ------ Formatar REAL e %
                formatarMoeda = ["FATURADO 60 DIAS", "BONIFICADO"]
                for coluna in formatarMoeda:
                    topCli2_result[coluna] = topCli2_result[coluna].apply(format_number)

                formatarPorcent = ["% BONIFICADO"]
                for coluna in formatarPorcent:
                    topCli2_result[coluna] = topCli2_result[coluna].apply(lambda x: '{:.1f}%'.format(x))

                # ------ DataFrame para HTML 
                table_html = topCli2_result.to_html(classes='table-style', index=False)

                for i in range(1, 4): # Definindo a classe rank para aplicar estilos
                    table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank{i}">{i}</td>')
                for i in range(4, 11):
                    table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank">{i}</td>')

                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>')
                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>')

                # ------ Estilos CSS personalizados
                with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                    cli_css = file.read()
                css = f"""
                <style>
                    {cli_css}
                </style>
                """

                # ----------------- Exibição da tabela -----------------
                st.markdown(f"<h3 class='dnH3'>RANK TOP 10 CLIENTES - VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção
                
                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit
                
                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS




# -------------------------------------- VERBAS -------------------------------------- #
with aba5:
    c1, c2 = st.columns([0.300, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/1649/1649628.png', width=180)
    with c2:
        st.title("CONSULTAR VERBA")
        st.markdown("Painel destinado a consultar :green[VERBAS]")
        st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 1, 3.75])
    with col1:
        btn1 = st.button("CARREGAR", key=4, type="primary")
    with col2:
        senhaSemTratamento = st.text_input("Senha", "", max_chars = 6, type = "password", label_visibility="collapsed", help="Digite a senha numérica para acessar as informações")
    
    senha = bleach.clean(senhaSemTratamento) # Limpa a senha para evitar injeção de código
    
    with col3:
        if senha == "" or len(senha) < 6:
            st.warning("Sem dados para exibir. Verifique a senha inserida.")
        else:
            pass
    if btn1:
        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
            # ------------ Execução da Consulta -----------------
            verbas_result = verbas(senha)

            # ------------ Formatação da tabela -----------------
            verbas_result = verbas_result.iloc[:, [0, 1, 2,]].rename(columns={
                0: "COD",
                1: "VENDEDOR",
                2: "VERBA"
            }).reset_index(drop=True)
            
            formatarMoeda = ["VERBA"]
            for coluna in formatarMoeda:
                verbas_result[coluna] = verbas_result[coluna].apply(format_number)

            verbas_result = pd.DataFrame(verbas_result.to_dict())

            if verbas_result.empty:
                with col3:
                    st.warning("Sem dados para exibir. Verifique a senha inserida.")
            else:
                col1, col2, col3 = st.columns([0.5, 2, 2])
                with col2:
                    st.dataframe(verbas_result)
            tm.sleep(1.5)

# --------------------------- DEDO DURO ----------------------------------- #
with aba6: 
    c1, c2 = st.columns([0.300, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/4380/4380709.png', width=180)
    with c2:    
        st.title(":point_up: DEDO DURO")
        st.markdown("Painel destinado a apontar :red[ERROS] e :red[PROBLEMAS] diversos")
        st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- Botão de Recarregar -----------------
        recarregarDados = st.button("RECARREGAR DADOS", key=5, type="primary")

    if recarregarDados:
        pedErro_result = pedErro()
        pedCont_result = pedCont()
        inad_result = inad(vendedorCod)
        devolucao_result = devolucao(dataIni, dataFim)

    aba6_1, aba6_2, aba6_3, aba6_4, aba6_5 = st.tabs([":warning: Erros", ":pencil: Pedidos", ":small_red_triangle_down: Devoluções", ":rotating_light: Inadimplência", ":package: Estoque"])
    # ---------- ERROS ---------- #
    with aba6_1:
        st.header(":warning: Erros Diversos")
        st.markdown("    ")
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:"):
            st.divider()
            c1,c2,c3 = st.columns([0.7,1.3,1])
            with c3:
                pedErro_result = pedErro()
                pedErro_result = pedErro_result.iloc[:, [0, 1, 2, 3]].rename(columns={
                    0: "CODCLI",
                    1: "RCA",
                    2: "TIPO ERRO",
                    3: "POSIÇÃO"
                })
                st.markdown("    ")
                selected_errors = st.multiselect(label="Filtro de Erros", options = pedErro_result['TIPO ERRO'].unique().tolist(), default = pedErro_result['TIPO ERRO'].unique().tolist(), placeholder="Filtro de erros", help="Selecione o tipo de erro para filtrar na tabela")
            # ------ Fora da Coluna
            filtered_pedErro_result = pedErro_result[pedErro_result['TIPO ERRO'].isin(selected_errors)]
            with c3:
            # ------ Retorna para Coluna
                st.divider()
                if st.button('GERAR EXCEL', key="excel_pedErro"): # ---- Convertendo para Excel
                    st.markdown(getTableXls(filtered_pedErro_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download


            with c1:
                st.write("Legenda:")
                container1 = st.container(border=True)
                container1.caption(":red[Possível Duplicidade] significa que existe 1 ou mais pedidos do cliente com 1 ou mais itens repetidos.")
                container2 = st.container(border=True)
                container2.caption(":red[BNF SEM PEDIDO] se refere a bonificações enviadas, mas sem pedidos de venda no sistema.")
                container3 = st.container(border=True)
                container3.caption(":red[PEDIDO ABAIXO DO MÍNIMO] são pedidos que sofreram corte e ficaram com seu valor abaixo de R$100 e por isso não serão enviados ao cliente.")
                container4 = st.container(border=True)
                container4.caption(":red[CODCOB != CODPLPAG] significa que a cobrança do cliente está Boleto a Vista.")
                container5 = st.container(border=True)
                container5.caption(":red[X Liberado(s), Y BLOQUEADO(s)] se refere a pedidos bloqueados e liberados do mesmo cliente. Onde X é a quantidade de pedidos liberados e Y a quantidade de pedidos bloqueados.")

            with c2:
                st.write("Tabela de Erros:")
                if filtered_pedErro_result.empty:
                    st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                else:
                    st.dataframe(filtered_pedErro_result)


    # ---------- Pedidos -------- #
    with aba6_2:
        st.header(":pencil: Pedidos com Erros")
        st.markdown("    ")
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:"):
            pedCont_result = pedCont()
            st.markdown(f"<h3 class='dnH3'>QUANTIDADE DE PEDIDOS BLOQUEADOS</h3>", unsafe_allow_html=True)
            subcoluna1, subcoluna2, subcoluna3= st.columns([1, 1.5, 1])
            with subcoluna2:
                # ----------------- Formatação da tabela -----------------
                pedCont_result = pedCont_result.iloc[:, [0, 1, 2,]].rename(columns={
                    0: "BLOQUEADOS",
                    1: "PENDENTES",
                    2: "BLOQ. + PEND."
                })    

                # ------ Exibindo DataFrame para HTML 
                table_html = pedCont_result.to_html(classes='table-style-bloq', index=False)
                table_html = table_html.replace('<td>', '<td class="linha-table-bloq">')
                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit
            c1,c2,c3 = st.columns([0.7,2,0.7])
            

    # ---------- Devoluções ----- #
    with aba6_3:
        st.header(":small_red_triangle_down: Devoluções por período")
        st.markdown("    ")
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:"):
            subcoluna1, subcoluna2, subcoluna3, subcoluna4 = st.columns([0.5, 0.5, 1, 1])
            with subcoluna1:
                dataIni = st.date_input(":date: Data inicial", value=pd.to_datetime('today') - pd.offsets.MonthBegin(1), format='DD/MM/YYYY', key='DEV1')
            with subcoluna2:
                dataFim = st.date_input(":date: Data final", value=pd.to_datetime('today'), format='DD/MM/YYYY', key='DEV2')
            st.divider()
            c1,c2,c3 = st.columns([0.7,2,0.7])
            with c3:
                devolucao_result = devolucao(dataIni, dataFim)
                devolucao_result = devolucao_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]].rename(columns={
                    0: "NUMNOTA",
                    1: "NUMCAR",
                    2: "SUP",
                    3: "RCA",
                    4: "CLIENTE",
                    5: "MOTORISTA",
                    6: "VALOR",
                    7: "DEBITO RCA",
                    8: "BNF?",
                    9: "MOTIVO",
                    10: "TIPO",
                    11: "OBSERVAÇÃO"
                })
                formatarMoeda = ["VALOR", "DEBITO RCA"]
                for coluna in formatarMoeda:
                    devolucao_result[coluna] = devolucao_result[coluna].apply(format_number)
                st.markdown("    ")
                selected_errors = st.multiselect(label="Filtro de Tipo", key="selected_errors", options = devolucao_result['TIPO'].unique().tolist(), default = devolucao_result['TIPO'].unique().tolist(), placeholder="Filtro de Tipo", help="Selecione o tipo de devolução para filtrar na tabela")
            # ------ Fora da Coluna
            filtered_devolucao_result = devolucao_result[devolucao_result['TIPO'].isin(selected_errors)]
            with c3:
            # ------ Retorna para Coluna
                st.divider()
                if st.button('GERAR EXCEL', key="excel_devolucao"): # ---- Convertendo para Excel
                    st.markdown(getTableXls(filtered_devolucao_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download

            with c1:
                st.write("Legenda:")
                container1 = st.container(border=True)
                container1.caption("Selecione uma data acima para visualizar as devoluções desse período.")
                container2 = st.container(border=True)
                container2.caption(":red[Tipo C] significa devoluções por desacordos ou erros :red[Comerciais].")
                container3 = st.container(border=True)
                container3.caption(":blue[Tipo L] são devoluções por :blue[Logística].")
                container4 = st.container(border=True)
                container4.caption(":green[Tipo F] são devoluções por erros :green[Financeiros].")
                container5 = st.container(border=True)
                container5.caption(":orange[Tipo A] se refere a erros :orange[Administrativos].")
                container6 = st.container(border=True)
                container6.caption("Tipo O :grey[são devoluções por] Outros Motivos.")
            
            with c2:
                st.write("Tabela de Erros:")
                if filtered_devolucao_result.empty:
                    st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                else:
                    st.dataframe(filtered_devolucao_result)


    # ---------- Inadimplência -- #
    with aba6_4:
        st.header(":rotating_light: Inadimplência por Cliente")
        st.markdown("    ")
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:"):
            col1, col2, col3, col4 = st.columns([1, 1, 0.55, 2])
            with col1:
                    vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_4', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                    if vendedorName == "LEONARDO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (140,),index=0, key='140_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EDNALDO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (141,),index=0, key='141_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VAGNER":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (142,),index=0, key='142_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEIVID":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (143,),index=0, key='143_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "BISMARCK":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (145,),index=0, key='145_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCIANA":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (147,),index=0, key='147_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MATHEUS":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (148,),index=0, key='148_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MARCIO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (150,),index=0, key='150_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LEANDRO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (151,),index=0, key='151_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "REGINALDO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (152,),index=0, key='152_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROBSON":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (153,),index=0, key='153_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "JOAO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (154,),index=0, key='154_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TAYANE":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (155,),index=0, key='155_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MURILO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (156,),index=0, key='156_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCAS":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (157,),index=0, key='157_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEYVISON":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (158,),index=0, key='158_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ZEFERINO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (161,),index=0, key='161_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EPAMINONDAS":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (164,),index=0, key='164_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "GLAUBER":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (167,),index=0, key='167_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TARCISIO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (168,),index=0, key='168_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "THIAGO":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (169,),index=0, key='169_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "FILIPE":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (170,),index=0, key='170_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROMILSON":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (172,),index=0, key='172_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VALDEME":
                        with col2:
                            vendedorCod = st.selectbox("CÓDIGO WINTHOR", (174,),index=0, key='174_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    else:
                        vendedorCod = st.selectbox("ERRO", (0,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 

            st.divider()
            c1,c2 = st.columns([0.5,2])
            inad_result = inad(vendedorCod)
            inad_result = inad_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]].rename(columns={
                0: "SUP",
                1: "RCA",
                2: "CLIENTE",
                3: "PED. NO SISTEMA?",
                4: "TÍTULO R$",
                5: "JUROS APROX.",
                6: "TOTAL R$",
                7: "COBRANÇA",
                8: "DIAS EM VENCI.",
                9: "EMISSAO",
                10: "DT VENCI."
            })
            formatarMoeda = ["TÍTULO R$", "JUROS APROX.", "TOTAL R$"]
            for coluna in formatarMoeda:
                inad_result[coluna] = inad_result[coluna].apply(format_number)

            formatarData = ["EMISSAO", "DT VENCI."]
            for coluna in formatarData:
                inad_result[coluna] = pd.to_datetime(inad_result[coluna]).dt.strftime('%d/%m/%Y')

            inad_result = inad_result.drop(columns=["RCA"])

            with c1:
                st.write("Legenda:")
                container1 = st.container(border=True)
                container1.caption("Selecione o vendedor acima para visualizar os clientes com débitos na empresa.")

            with c2:
                st.write("Tabela de Inadimplentes:")
                if inad_result.empty:
                    st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                else:
                    st.dataframe(inad_result)

    # ---------- Estoque ---------- #
    with aba6_5:
        st.header(":package: Estoque Gerencial")
        st.markdown("    ")
        with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:"):
            st.divider()
            diasUteis = diasUteis().values[0][0]
            # Data atual
            now = datetime.now()
            # Mês 0 - Mês Atual
            dtIniMesAtual = now.replace(day=1)
            dtFimMesAtual = now
            # Mês 1 - 1 Mês Antes
            dtIniMes1 = dtIniMesAtual - relativedelta(months=1)
            dtFimMes1 = dtIniMesAtual - relativedelta(days=1)
            # Mês 2 - 2 Meses Antes
            dtIniMes2 = dtIniMes1 - relativedelta(months=1)
            dtFimMes2 = dtIniMes1 - relativedelta(days=1)
            # Mês 3 - 3 Meses Antes
            dtIniMes3 = dtIniMes2 - relativedelta(months=1)
            dtFimMes3 = dtIniMes2 - relativedelta(days=1)
            c1,c2,c3 = st.columns([0.6,1.5,1])
            with c3:
                qtdVendaMes0_result = qtdVendaProd(dtIniMesAtual, dtFimMesAtual)
                qtdVendaMes0_result = qtdVendaMes0_result.iloc[:, [0, 1,]].rename(columns={
                    0: "CODPROD",
                    1: "QTD MÊS ATUAL",
                })

                qtdVendaMes1_result = qtdVendaProd(dtIniMes1, dtFimMes1)
                qtdVendaMes1_result = qtdVendaMes1_result.iloc[:, [0, 1,]].rename(columns={
                    0: "CODPROD",
                    1: "QTD MÊS 1",
                })

                qtdVendaMes2_result = qtdVendaProd(dtIniMes2, dtFimMes2)
                qtdVendaMes2_result = qtdVendaMes2_result.iloc[:, [0, 1,]].rename(columns={
                    0: "CODPROD",
                    1: "QTD MÊS 2",
                })

                qtdVendaMes3_result = qtdVendaProd(dtIniMes3, dtFimMes3)
                qtdVendaMes3_result = qtdVendaMes3_result.iloc[:, [0, 1,]].rename(columns={
                    0: "CODPROD",
                    1: "QTD MÊS 3",
                })

                estoque266_result = estoque266()
                estoque266_result = estoque266_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]].rename(columns={
                    0: "CODPROD",
                    1: "DTULTENT",
                    2: "DESCRICAO",
                    3: "CODFORNEC",
                    4: "FORNECEDOR",
                    5: "EMBALAGEM",
                    6: "QTDULTENT",
                    7: "UN MASTER",
                    8: "QTEST",
                    9: "QTD ESTOQUE",
                    10: "QTBLOQMENOSAVARIA",
                    11: "QTD EST CX", # QTD ESTOQUE / UN. MASTER = QTD CAIXA
                })


                formatarData = ["DTULTENT"]
                for coluna in formatarData:
                    estoque266_result[coluna] = pd.to_datetime(estoque266_result[coluna]).dt.strftime('%d/%m/%Y')
                
                estoque266_result = estoque266_result.drop(columns=["QTBLOQMENOSAVARIA", "QTEST", "UN MASTER"])

                estoque266_result = estoque266_result.merge(qtdVendaMes3_result, on='CODPROD', how='left').fillna('0')
                estoque266_result = estoque266_result.merge(qtdVendaMes2_result, on='CODPROD', how='left').fillna('0')
                estoque266_result = estoque266_result.merge(qtdVendaMes1_result, on='CODPROD', how='left').fillna('0')
                estoque266_result = estoque266_result.merge(qtdVendaMes0_result, on='CODPROD', how='left').fillna('0')

                estoque266_result = estoque266_result.assign(QTDVENDDIA = lambda x: (((x['QTD MÊS ATUAL'].astype(float)) + 
                                                                                    (x['QTD MÊS 1'].astype(float)) + 
                                                                                    (x['QTD MÊS 2'].astype(float)) + 
                                                                                    (x['QTD MÊS 3'].astype(float))) / 4) / diasUteis)
                
                estoque266_result = estoque266_result.assign(QTDESTDIA = lambda x: ((x["QTD ESTOQUE"].astype(float) / x["QTDVENDDIA"].astype(float))))

                st.markdown("    ")
                selected_fornec = st.selectbox(label="Filtro de :red[Fornecedor]", options=estoque266_result['FORNECEDOR'].unique().tolist(), index=0, placeholder="Filtro de Fornecedor", help="Selecione para filtrar na tabela")
            # ------ Fora da Coluna
            filtered_estoque266_result = estoque266_result[estoque266_result['FORNECEDOR'].isin([selected_fornec])]
            codFornec = filtered_estoque266_result["CODFORNEC"].iloc[0]
            nomeFornec = filtered_estoque266_result["CODFORNEC"].iloc[0]
            filtered_estoque266_result = filtered_estoque266_result.drop(columns=["FORNECEDOR", "CODFORNEC"])
            filtered_estoque266_result = filtered_estoque266_result.sort_values('QTDVENDDIA', ascending=False)
            filtered_estoque266_result[['QTDVENDDIA','QTDESTDIA','QTDULTENT']] = filtered_estoque266_result[['QTDVENDDIA','QTDESTDIA','QTDULTENT']].fillna(0).replace([np.inf, -np.inf], 0)
            filtered_estoque266_result[['QTDVENDDIA','QTDESTDIA','QTDULTENT']] = filtered_estoque266_result[['QTDVENDDIA','QTDESTDIA','QTDULTENT']].astype(float).round(0).astype(int).astype(str)
            with c3:
            # ------ Retorna para Coluna
                st.divider()
                if st.button('GERAR EXCEL', key="excel_estoque"): # ---- Convertendo para Excel
                    st.markdown(getTableXls(filtered_estoque266_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
            
            with c1:
                st.write("Legenda:")
                container1 = st.container(border=True)
                container1.caption(':orange["DTULTENT"] É a data da última entrada do produto. :orange["QTDULTENT"] É a quantidade da última entrada do produto.')
                container2 = st.container(border=True)
                container2.caption(':blue["QTD EST CX"] É a quantidade disponível de produtos em Caixas Master.')
                container3 = st.container(border=True)
                container3.caption(':green["QTD MÊS 1"] Se refere ao :green[mês anterior] ao mês atual. Mês 2 e 3 antecedem em sequência.')
                container4 = st.container(border=True)
                container4.caption(f':blue["QTESTDIA"] É quantidade de estoque para {diasUteis} dias úteis do mês. :green["QTVENDDIA"] É quantidade vendida em {diasUteis} dias.')

            with c2:
                st.write("Tabela de Estoque Gerencial:")
                if filtered_estoque266_result.empty:
                    st.warning("Sem dados para exibir. Verifique os filtros selecionados ao lado :point_right:")
                else:
                    st.dataframe(filtered_estoque266_result)

            st.divider()
            c1_2, c2_2, c3_2 = st.columns([0.6,1.5,1])
            with c3_2:
                prodSemVenda_result = prodSemVenda(codFornec)
                prodSemVenda_result = prodSemVenda_result.iloc[:, [0, 1, 2, 3, 4, 5]].rename(columns={
                    0: "CODPROD",
                    1: "DESCRICAO",
                    2: "DTULTENT",
                    3: "QTDULTENT",
                    4: "ESTOQUE",
                    5: "DIAS SEM VENDA"
                })
                st.divider()
                if st.button('GERAR EXCEL', key="excel_prodSemVenda"): # ---- Convertendo para Excel
                    st.markdown(getTableXls(prodSemVenda_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
            
            with c2_2:
                st.write("Tabela de Produtos Sem Venda:")
                if prodSemVenda_result.empty:
                    st.warning("Sem dados para exibir. Verifique os filtros selecionados ao lado :point_right:")
                else:
                    st.dataframe(prodSemVenda_result)

            with c1_2:
                st.write("Legenda:")
                container1 = st.container(border=True)
                container1.caption(f'Produtos sem venda a mais de 7 dias do fornecedor {nomeFornec}')


# --------------------------- Outros ----------------------------------- #
with aba7:
    with st.spinner('Carregando dados...'): 
        result = campanhaDanone()
        st.table(result)
        c1, c2, c3 = st.columns([2,0.75,2])
        with c2:
            if st.button('GERAR EXCEL'): # ---- Convertendo para Excel
                st.markdown(getTableXls(result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download


st.divider()
col1, col2, col3 = st.columns([2.5,1,2.5])
with col2:
    st.image(path + 'Imagens/DataAdvisor.png', width=200, caption="Plataforma BI - Versão 1.8.8.8") # "X." Versão Total | ".X." Versão do SQL | ".X." Versão Navigator e Opções de Paineis | ".X" Versão Layout (disposição dos itens. HTML, CSS, Streamlit)
    c1, c2 = st.columns([0.4, 1.6])
    with c2:
        st.caption("By SammMartins", help="Desenvolvido por Sammuel G Martins")
        with st.spinner('Carregando...'):
            tm.sleep(3)