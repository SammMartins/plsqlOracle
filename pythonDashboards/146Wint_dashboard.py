# Dashboard em Python com o Streamlit, Pandas, Plotly e cx_Oracle (usando segurança dos dados do banco). 

import streamlit as st
import pandas as pd
import plotly.express as px
import cx_Oracle as cx
import configparser as cp
from datetime import date, timedelta

# Carregue o arquivo de configuração
config = cp.ConfigParser()
config.read('/home/premium/db_config.ini')

# Conecte ao banco de dados Oracle
username = config.get('oracle_db', 'username')
password = config.get('oracle_db', 'password')
host = config.get('oracle_db', 'host')
port = config.get('oracle_db', 'port')
sid = config.get('oracle_db', 'sid')

# Verifique se todas as variáveis de ambiente estão definidas
if None in [username, password, host, port, sid]:
    raise ValueError("Uma ou mais variáveis necessárias não estão definidas")
else:
    print("Todas as variáveis estão definidas")

dsn_tns = cx.makedsn(host, port, sid)
con = cx.connect(user=username, password=password, dsn=dsn_tns)

# Esta linha de código está criando um novo objeto cursor e atribuindo-o à variável cursor. 
# Um cursor é um objeto que permite executar comandos SQL e recuperar dados de um banco de dados. 
# con é presumivelmente uma conexão de banco de dados que foi criada anteriormente no código.
cursor = con.cursor()

# Carregando o arquivo SQL com a consulta
with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Comerciais/4Dashboards/vendasRealTime_dashboard/vendasPorSupervisor', 'r') as arquivo: 
    consulta = arquivo.read()

# Configuração do dashboard
st.set_page_config(page_title="146 Wint", page_icon=":moneybag:", layout="wide", initial_sidebar_state="expanded")
st.title("Vendas em Tempo Real")
st.markdown("Aqui você encontrará as informações completas sobre vendas da Premium Distribuidora.")

# Solicite ao usuário que escolha uma data inicial
dataIni = st.sidebar.date_input("Escolha uma data inicial", value=pd.to_datetime('today'), format='DD/MM/YYYY')
# Solicite ao usuário que escolha uma data final
dataFim = st.sidebar.date_input("Escolha uma data final", value=pd.to_datetime('today'), format='DD/MM/YYYY')
# Formatar data para o formato DD-MMM-YYYY
dataIni = dataIni.strftime('%d-%b-%Y')
dataFim = dataFim.strftime('%d-%b-%Y')

# Solicite ao usuário que escolha o supervisor
#sup = st.sidebar.multiselect("Escolha o supervisor", [2, 8], default=[2, 8])

# Substitui '{dtIni}', '{dtFim}', e '{sup}' na consulta pelas datas selecionadas pelo usuário
consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

# Execute a consulta SQL
cursor.execute(consulta)

# Obtenha os resultados da consulta
resultados = cursor.fetchall()

st.header("Vendas por Equipe")
# Crie um DataFrame com os resultados
df = pd.DataFrame(resultados, columns=[desc[0] for desc in cursor.description])

# Formate a segunda coluna para a moeda Real do Brasil
df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: 'R$ {:,.2f}'.format(x))

# Oculte a primeira coluna do DataFrame
#df = df.iloc[:, 1:]

# Defina o tamanho da fonte para 150%
styles = [
    dict(selector="th", props=[("font-size", "150%")]),
    dict(selector="td", props=[("font-size", "150%")]),
]

# Aplique os estilos ao DataFrame
df_styled = df.style.set_properties(**{'background-color': 'black',
                                       'color': 'white',
                                       'border-color': 'grey',
                                       'border-style': 'solid',
                                       'text-align': 'center',
                                       'border-width': '1px'}).set_table_styles(styles)


# Definir a opção para exibir todas as colunas sem truncar
pd.set_option('display.max_columns', None)

# Exibição da tabela na interface do Streamlit
st.dataframe(df_styled)

# streamlit run pythonDashboards/146Wint_dashboard.py