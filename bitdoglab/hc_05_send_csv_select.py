import os
from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

# Função para listar arquivos no diretório raiz
def listar_arquivos():
    arquivos = os.listdir()
    print("Arquivos disponíveis:")
    for idx, nome in enumerate(arquivos):
        print(f"{idx + 1}. {nome}")
    return arquivos

# Função para enviar um arquivo selecionado
def enviar_arquivo():
    arquivos = listar_arquivos()
    
    # Solicita ao usuário que escolha um arquivo
    escolha = int(input("Digite o número do arquivo que deseja enviar: ")) - 1
    
    # Verifica se a escolha é válida
    if 0 <= escolha < len(arquivos):
        arquivo_selecionado = arquivos[escolha]
        print(f"Enviando: {arquivo_selecionado}")
        try:
            with open(arquivo_selecionado, 'r') as f:
                for linha in f:
                    uart.write(linha)
                    print("Enviado:", linha.strip())
                    time.sleep(0.1)  # Pequeno delay para evitar overflow
        except OSError:
            print("Erro ao abrir o arquivo.")
    else:
        print("Escolha inválida.")

enviar_arquivo()
