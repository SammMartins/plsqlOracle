import pandas as pd
import cx_Oracle as cx
from configparser import ConfigParser

def df1(dataIni, dataFim):
    config = ConfigParser()
    config.read('/home/premium/db_config.ini')

    username = config.get('oracle_db', 'username')
    password = config.get('oracle_db', 'password')
    host = config.get('oracle_db', 'host')
    port = config.get('oracle_db', 'port')
    sid = config.get('oracle_db', 'sid')

    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Comerciais/4Dashboards/vendasRealTime_dashboard/vendasPorSupervisor.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    cursor.execute(consulta)

    # Obtenha os resultados da consulta
    resultados = cursor.fetchall()

    df = pd.DataFrame.from_dict(resultados)

    return df

def df2(dataIni, dataFim):
    config = ConfigParser()
    config.read('/home/premium/db_config.ini')

    username = config.get('oracle_db', 'username')
    password = config.get('oracle_db', 'password')
    host = config.get('oracle_db', 'host')
    port = config.get('oracle_db', 'port')
    sid = config.get('oracle_db', 'sid')

    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Comerciais/4Dashboards/vendasRealTime_dashboard/vendasPorRCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    cursor.execute(consulta)

    # Obtenha os resultados da consulta
    resultados = cursor.fetchall()

    df = pd.DataFrame.from_dict(resultados)

    return df

def df3(dataIni, dataFim):
    config = ConfigParser()
    config.read('/home/premium/db_config.ini')

    username = config.get('oracle_db', 'username')
    password = config.get('oracle_db', 'password')
    host = config.get('oracle_db', 'host')
    port = config.get('oracle_db', 'port')
    sid = config.get('oracle_db', 'sid')

    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    con = cx.connect(user=username, password=password, dsn=dsn_tns)

    cursor = con.cursor()

    with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Comerciais/4Dashboards/vendasRealTime_dashboard/vendasPorCliente.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    cursor.execute(consulta)

    # Obtenha os resultados da consulta
    resultados = cursor.fetchall()

    df = pd.DataFrame.from_dict(resultados)

    return df