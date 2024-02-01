import os
import time
import datetime
import cx_Oracle as cx
import configparser as cp
import schedule

def main():
    print("Iniciando o serviço... \n Para parar o serviço, pressione Ctrl + C.")

    # Carregue o arquivo de configuração
    config = cp.ConfigParser()
    config.read('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Mtrix/config.ini')

    # Conecte ao banco de dados Oracle
    username = config.get('oracle_db', 'username')
    password = config.get('oracle_db', 'password')
    host = config.get('oracle_db', 'host')
    port = config.get('oracle_db', 'port')
    sid = config.get('oracle_db', 'sid')
    pastaAlvo = config.get('paths', 'pastaAlvo')

    # Verifique se todas as variáveis de ambiente estão definidas
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas.")
    else:
        print("Todas as variáveis estão definidas\n")
        dsn_tns = cx.makedsn(host, port, sid)

    con = None

    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
        print("Conexão bem-sucedida!")
    except cx.Error as error:
        time.sleep(1)
        print("Erro ao conectar ao banco de dados:", error)

    # Verifique se a conexão foi bem-sucedida antes de tentar usar a variável con
    if con is None:
        print("Não foi possível estabelecer uma conexão com o banco de dados.")
        exit()

    while True:
        print("O diretório onde o arquivo será salvo é:")
        time.sleep(1) # Espera 1 segundo
        print(">>> " + pastaAlvo) # Imprime o diretório padrão
        time.sleep(3) 
        diretorioAlvo = pastaAlvo
        time.sleep(1)

        if not os.path.exists(diretorioAlvo): # Verifica se o diretório existe
            print("Diretório não existe! Pressione Ctrl + C para sair ou aguarde para nova tentativa.\n ")
            time.sleep(3)
        else:
            break

    nA1 = "ESTOQUEFRO" # Prefixo + Sigla do Fornecededor
    nA2 = "COMODATOFRO" # Prefixo + Sigla do Fornecededor
    sysdate = datetime.datetime.now().strftime("%d%m%Y%H%M%S%f") # Dia + Mês + Ano + Hora + Minuto + Segundo + Milésimo de segundo
    extensao = ".txt" # Extensão do arquivo
    nomeArquivoEstoque = nA1 + sysdate + extensao # Nome completo do arquivo a ser salvo
    nomeArquivoComodato = nA2 + sysdate + extensao # Nome completo do arquivo a ser salvo

    estoqueCompleto = os.path.join(diretorioAlvo, nomeArquivoEstoque) # Junta o diretório com o nome do arquivo
    comodatoCompleto = os.path.join(diretorioAlvo, nomeArquivoComodato) 

    cursor = con.cursor() # Cria um cursor para executar a consulta

    with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Mtrix/txtComodatoMtrix-Estoque.sql', 'r') as arquivo: 
        consultaEstoque = arquivo.read() # Carrega a consulta de estoque

    with open('/mnt/g/Documentos/Sammuel/Arquivos/Consultas/principais/PLSQL/Consultas/Mtrix/txtComodatoMtrix.sql', 'r') as arquivo: 
        consultaComodato = arquivo.read() # Carrega a consulta de comodato

    try:
        # Executa a consulta SQL
        cursor.execute(consultaEstoque)
        # Obtém os resultados da consulta
        resultadoEstoque = cursor.fetchall()
    except cx.Error as error:
        print("Erro ao executar a consulta de estoque:", error)
        exit()

    try:
        # Executa a consulta SQL
        cursor.execute(consultaComodato)
        # Obtém os resultados da consulta
        resultadoComodato = cursor.fetchall()
    except cx.Error as error:
        print("Erro ao executar a consulta de comodato:", error)
        exit()

    with open(estoqueCompleto, "w") as arquivo: # Abre o arquivo para escrita
        for row in resultadoEstoque:
            arquivo.write(row[0] + "\n") # Escreve cada linha do resultadoEstoque no arquivo
            
    with open(comodatoCompleto, "w") as arquivo: # Abre o arquivo para escrita
        for row in resultadoComodato:
            arquivo.write(row[0] + "\n") # Escreve cada linha do resultadoEstoque no arquivo
            
    if os.path.exists(estoqueCompleto): # Verifica se o arquivo existe 
        time.sleep(1)
        print("\nArquivos salvos com sucesso!") # Imprime uma mensagem de sucesso
    else:
        print("\nErro ao salvar os arquivos!")    

main()

# Agende a função para ser executada a cada 5 minutos
schedule.every(1).minutes.do(main)

# Mantenha o script em execução
while True:
    schedule.run_pending()
    time.sleep(1)