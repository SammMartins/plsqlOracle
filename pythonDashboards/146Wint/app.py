import numpy as np
import pandas as pd
import streamlit as st
import time as tm
import math
from dataset import df1, df2, df3, df4, diasUteis, diasDecorridos, flash322RCA, flashDN322RCA, flash1464RCA, flash322RCA_semDev, flashDN1464RCA, flash1464SUP, flashDN1464SUP, flash322SUP, flashDN322SUP, top100Cli, top100Cli_comparativo, metaCalc, metaSupCalc, verbas, trocaRCA
from utils import format_number, data_semana_ini, data_semana_fim
from grafic import grafico_vend_sup, grafico_top_rca2, grafico_top_rca8
from datetime import datetime

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

# ----------------------- Dashboard Layout ----------------------- #
aba1, aba2, aba3, aba4, aba5 = st.tabs([":dollar: VENDA", ":bar_chart: FLASH", ":dart: META", ":department_store: CLIENTES", ":bank: VERBAS"])

with aba1:
    c1, c2 = st.columns([0.2, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/1358/1358684.png', width=180)
    with c2:
        st.title("PAINEL DE VENDAS")
        st.markdown(":page_with_curl: Faturado e não faturado semelhante a rotina 322 Winthor")
        st.markdown(":iphone:   Apenas pedidos digitados pelo vendedor são exibidos")
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
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
                if df2_result.empty:
                    st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos.")
                else:
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
            with st.spinner('Caregando dados...'):
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
                    with st.spinner('Caregando dados...'):
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
    c1, c2 = st.columns([0.2, 1])
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

    with st.spinner('Caregando dados...'):
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
            supName = st.selectbox("SUPERVISOR", ("ADAILTON", "VILMAR JR"), index=0, key='sup', help="Selecione o Supervisor", placeholder="Escolha o Supervisor", label_visibility="visible")
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
                    with st.spinner('Caregando dados...'):
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
                    with st.spinner('Caregando dados...'):
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
            vendedorName = st.selectbox("VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca', help="Selecione o vendedor", placeholder="Escolha um Vendedor", label_visibility="visible")
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
                    with st.spinner('Caregando dados...'):
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
                                    st.markdown(f"<p class='dn'>TROCA {vendedorName}</p>", unsafe_allow_html=True)
                                    st.markdown(troca_result, unsafe_allow_html=True)





        # -------------------------------- Não Faturado incluso ABATENDO DEVOLUÇÃO ----------------------------------
        elif notFatOn == True and devOn == True:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Todos", help="Todos os pedidos digitados abatendo devolução (se houver). Essa opção apresenta um resultados mais completo das vendas, mas com sofrerá alterações caso algum pedido não seja faturado, cancelado, ou sofra algum corte.")
            with col1:
                if st.button("CARREGAR"):
                    with st.spinner('Caregando dados...'):
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
                                    st.markdown(f"<p class='dn'>TROCA {vendedorName}</p>", unsafe_allow_html=True)
                                    st.markdown(troca_result, unsafe_allow_html=True)                                    


        # -------------------------------- Não Faturado incluso COM DEVOLUÇÃO ----------------------------------
        else:
            col1, col2 = st.columns([1, 0.12])
            with col2:
                st.caption("Irreal", help="Todos os pedidos digitados sem abater devolução. Essa opção apresenta um resultados mais completo das vendas, mas com sofrerá alterações caso algum pedido não seja faturado, cancelado, ou sofra algum corte.")
            with col1:
                if st.button("CARREGAR"):
                    with st.spinner('Caregando dados...'):
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
    c1, c2 = st.columns([0.2, 1])
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
                vendedorName = st.selectbox("VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_2', help="Selecione o vendedor", placeholder="Escolha um Vendedor", label_visibility="visible")
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
            with st.spinner('Caregando dados...'):
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
            supName = st.selectbox("SUPERVISOR", ("ADAILTON", "VILMAR JR"), index=0, key='sup_2', help="Selecione o Supervisor", placeholder="Escolha o Supervisor", label_visibility="visible")
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
            with st.spinner('Caregando dados...'):
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
    c1, c2 = st.columns([0.2, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/5434/5434400.png', width=180)
    with c2:
        st.title("RELATÓRIO CLIENTES")
        st.markdown("Painel destinado a :blue[análise detalhada] dos principais clientes")
        st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("CARREGAR DADOS", key=1):
        with st.spinner('Caregando dados...'):
            # --------------------------- RANK TOP 100 --------------------------- #
            with st.expander("RANK TOP 100"):
                # --------------- Dados Top CLI -----------------------
                topCli_result = top100Cli()

                # ----------------- Formatação da tabela -----------------
                topCli_result = topCli_result.iloc[:, [0, 1, 2, 3, 4, 5, 6,]].rename(columns={
                    0: "RANK",
                    1: "CODCLI",
                    2: "CLIENTE",
                    3: "VENDEDOR",
                    4: "FATURADO",
                    5: "INVESTIDO",
                    6: "% INVESTIDA"
                })

                formatarMoeda = ["FATURADO", "INVESTIDO"]
                for coluna in formatarMoeda:
                    topCli_result[coluna] = topCli_result[coluna].apply(format_number)

                formatarPorcent = ["% INVESTIDA"]
                for coluna in formatarPorcent:
                    topCli_result[coluna] = topCli_result[coluna].apply(lambda x: '{:.1f}%'.format(x))
                
                # ------ DataFrame para HTML 
                table_html = topCli_result.to_html(classes='table-style', index=False)

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



            # --------------------------- COMPARATIVO --------------------------- #
            with st.expander("RANK TOP 100 - COMPARATIVO"):
                topCli_result = top100Cli()
                topCliOld_result = top100Cli_comparativo()

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

                # Adiciona uma nova coluna 'TENDENCIA' que compara as colunas 'ANO ATUAL' e 'ANO ANTERIOR'
                merge_result['TENDENCIA'] = np.where(merge_result['ANO ATUAL'] > merge_result['ANO ANTERIOR'], '↑↑↑', '↓↓↓')

                # ------ Formatar Linha
                formatarMoeda = ["ANO ATUAL", "ANO ANTERIOR"]
                for coluna in formatarMoeda:
                    merge_result[coluna] = merge_result[coluna].apply(format_number)
                
                # ------ DataFrame para HTML 
                table_html = merge_result.to_html(classes='table-style', index=False)

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
                st.markdown("<h3 class='dnH3'>RANK TOP 100 CLIENTES - COMPARATIVO</h3>", unsafe_allow_html=True) # Título da seção

                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

            tm.sleep(1)

with aba5:
    c1, c2 = st.columns([0.2, 1])
    with c1:
        st.image('https://cdn-icons-png.flaticon.com/512/1649/1649628.png', width=180)
    with c2:
        st.title("CONSULTAR VERBA")
        st.markdown("Painel destinado a :green[CONSULTAR VERBAS]")
        st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 1, 3.75])
    with col1:
        btn1 = st.button("CARREGAR", key=4, type="primary")
    with col2:
        senha = st.text_input("Senha", "", max_chars = 6, type = "password", label_visibility="collapsed", help="Digite a senha numérica para acessar as informações")
    with col3:
        if senha == "" or len(senha) < 6:
            st.caption("Sem dados para exibir. Verifique a senha inserida.", help="Não há dados para exibir, verifique a senha inserida ou contate o suporte.")
        else:
            pass
    if btn1:
        with st.spinner('Caregando dados...'):
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
                    st.caption("Sem dados para exibir. Verifique a senha inserida.", help="Não há dados para exibir, verifique a senha inserida ou contate o suporte.")
            else:
                col1, col2, col3 = st.columns([0.35, 1.5, 2.05])
                with col2:
                    st.table(verbas_result)
            tm.sleep(1.75)



st.divider()
col1, col2, col3 = st.columns([2.5,1,2.5])
with col2:
    st.image(path + 'Imagens/DataAdvisor.png', width=200, caption="Plataforma de BI - Versão 1.3.2.5") # "X." Versão Total | ".X." Versão do SQL | ".X." Versão Navigator | ".X" Versão Layout