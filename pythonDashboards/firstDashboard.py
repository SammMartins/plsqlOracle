# Dashboard em Python com o Streamlit, Pandas, Plotly e cx_Oracle (usando segurança dos dados do banco). 

import streamlit as st
import pandas as pd
import plotly.express as px
import cx_Oracle as cx
import configparser as cp

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

# Crie um cursor
cursor = con.cursor()

# Carregue o arquivo SQL
with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Gerencial/Devoluções.sql', 'r') as arquivo: 
    consulta = arquivo.read()




# Configuração do dashboard
st.set_page_config(page_title="1º Dashboard em Python", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")
st.title("Primeiro Dashboard em Python")
st.markdown("Este é o primeiro dashboard em Python que estou criando com o Streamlit, Pandas, Plotly e cx_Oracle (usando segurança dos dados do banco).")

# Solicite ao usuário que escolha uma data inicial
dataIni = st.sidebar.date_input("Escolha uma data inicial", value=pd.to_datetime('today') - pd.Timedelta(days=30), format='DD/MM/YYYY')
# Solicite ao usuário que escolha uma data final
dataFim = st.sidebar.date_input("Escolha uma data final", value=pd.to_datetime('today'), format='DD/MM/YYYY')
# Formatar data para o formato DD-MMM-YYYY
dataIni = dataIni.strftime('%d-%b-%Y')
dataFim = dataFim.strftime('%d-%b-%Y')

# Substitui '{dtIni}' e '{dtFim}' na consulta pelas datas selecionadas pelo usuário
consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

# Execute a consulta SQL
cursor.execute(consulta)

# Obtenha os resultados da consulta
resultados = cursor.fetchall()

st.header("Devoluções")
# Crie um DataFrame com os resultados
df = pd.DataFrame(resultados, columns=[desc[0] for desc in cursor.description])

# Exiba o DataFrame na interface do Streamlit
st.dataframe(df)

# streamlit run pythonDashboards/firstDashboard.py