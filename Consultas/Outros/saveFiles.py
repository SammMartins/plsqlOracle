import os
import time
import datetime

while True:
    print("Difina o diretório onde o arquivo será salvo:")
    time.sleep(1) # Espera 1 segundo
    print(">>> C:/caminho/para/diretorio # Exemplo")
    time.sleep(2) 
    diretorioAlvo = input(">>> ") # Diretório onde o arquivo será salvo
    time.sleep(1)

    if not os.path.exists(diretorioAlvo): # Verifica se o diretório existe
        print("Diretório não existe! Pressione Ctrl + C para sair ou aguarde para nova tentativa.\n ")
        time.sleep(3)
    else:
        break

nA1 = "COMODATO"
sysdate = datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
extensao = ".txt"

nomeArquivo = nA1 + sysdate + extensao # Nome do arquivo a ser salvo

caminhoCompleto = os.path.join(diretorioAlvo, nomeArquivo) # Junta o diretório com o nome do arquivo

with open(caminhoCompleto, "w") as arquivo: # Abre o arquivo para escrita
    arquivo.write("Olá mundo!") # Escreve no arquivo

if os.path.exists(caminhoCompleto): # Verifica se o arquivo existe 
    time.sleep(1)
    print("\nArquivo salvo com sucesso!") # Imprime uma mensagem de sucesso