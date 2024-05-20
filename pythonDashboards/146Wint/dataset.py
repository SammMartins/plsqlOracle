import pandas as pd
import cx_Oracle as cx
from configparser import ConfigParser

with open('/home/ti_premium/dbpath.txt', 'r') as file:
    dbpath = file.read().strip().strip("'")
config = ConfigParser()
files = config.read(dbpath)
if not files:
    raise ValueError(f"Não foi possível ler o arquivo: {dbpath}")

path = '/home/ti_premium/PyDashboards/PremiumDashboards/4Dashboards/'

try:
    username = config.get('oracle_db', 'username')
    password = config.get('oracle_db', 'password')
    host = config.get('oracle_db', 'host')
    port = config.get('oracle_db', 'port')
    sid = config.get('oracle_db', 'sid')
except Exception as e:
    raise ValueError("Erro ao obter as informações de conexão do arquivo de configuração") from e


def df1(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorSupervisor.sql', 'r') as arquivo:
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
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorRCA.sql', 'r') as arquivo: 
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
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorCliente.sql', 'r') as arquivo: 
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
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorFornecedor.sql', 'r') as arquivo: 
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

def diasUteis():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dias_uteis.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def diasDecorridos():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dias_decorridos.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flash322RCA(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'flash322_RCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df