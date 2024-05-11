import pandas as pd
import cx_Oracle as cx
from configparser import ConfigParser

config = ConfigParser()
config.read('/home/premium/db_config.ini')
username = config.get('oracle_db', 'username')
password = config.get('oracle_db', 'password')
host = config.get('oracle_db', 'host')
port = config.get('oracle_db', 'port')
sid = config.get('oracle_db', 'sid')



def df1(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('./4Dashboards/vendasRealTime_dashboard/vendasPorSupervisor.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)
    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def df2(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('./4Dashboards/vendasRealTime_dashboard/vendasPorRCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def df3(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('./4Dashboards/vendasRealTime_dashboard/vendasPorCliente.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def df4(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('./4Dashboards/vendasRealTime_dashboard/vendasPorFornecedor.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df
