# Arquivo criado para testar a conexão com o banco de dados Oracle

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"/opt/oracle/instantclient_12_2")

# Conecte ao banco de dados Oracle
con = cx_Oracle.connect('PONTUAL/PONTUAL@192.168.38.250:1521/WINT')

# Crie um cursor
cur = con.cursor()

# Sua consulta SQL com placeholders para as datas
query = """
SELECT 'HELLO WORLD!' FROM DUAL
"""

# Execute a consulta SQL
cur.execute(query)

# Fetch os resutados
results = cur.fetchall()

# Imprima cada linha do resultado
for row in results:
    print(', '.join(map(str, row)))

# Não esqueça de fechar a conexão
con.close()