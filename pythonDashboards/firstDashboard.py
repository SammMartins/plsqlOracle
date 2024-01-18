# Dashboard em Python com o Streamlit, Pandas, Plotly e cx_Oracle (usando segurança dos dados do banco)

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
    raise ValueError("Uma ou mais variáveis de ambiente necessárias não estão definidas")
else:
    print("Todas as variáveis de ambiente estão definidas")

dsn_tns = cx.makedsn(host, port, sid)
con = cx.connect(user=username, password=password, dsn=dsn_tns)

# Crie um cursor
cur = con.cursor()

# Carregue o arquivo SQL
with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Gerencial/Devoluções.sql', 'r') as fileSql: 
    query = fileSql.read()

# Execute a consulta SQL
cur.execute(query)

# Obtenha os resultados da consulta
results = cur.fetchall()

# Crie um DataFrame com os resultados
df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])

# Exiba o DataFrame na interface do Streamlit
st.dataframe(df)
