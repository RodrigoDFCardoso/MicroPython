import network
import socket
import json
from time import sleep
import random

# Configurar Wi-Fi
ssid = "AP21_23"
password = "familiacardoso23"
ssid = "teste_web"
password = "teste@7890"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
t = 0
# Aguarde a conexão
while not wlan.isconnected():
    t += 1
    print("Conectando ao Wi-Fi...")
    sleep(2)
    if t > 10:
        print("Não foi possível Conectrar")
        break
print("Conectado!", wlan.ifconfig())

# Dados simulados
def gerar_dados(dados):
    return {
        "chart1": dados[0],
        "chart2": dados[1],
        "chart3": dados[2],
        "chart4": dados[3]
    }

# Configurar servidor HTTP
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)

print("Servidor rodando em http://{}".format(addr))

while True:

    cl, addr = server.accept()
    print("Cliente conectado de", addr)

    request = cl.recv(1024).decode('utf-8')
    if "GET /data" in request:
        arrays = [[random.randint(1, 100) for _ in range(5)] for _ in range(4)]
        # Responder com dados JSON e cabeçalho CORS
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"  # Permitir requisições de qualquer origem
            "\r\n"
        )
        cl.send(response)
        cl.send(json.dumps(gerar_dados(arrays)))
    else:
        # Página HTML ou mensagem simples
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Access-Control-Allow-Origin: *\r\n"  # Permitir requisições de qualquer origem
            "\r\n"
        )
        cl.send(response)
        cl.send("Servidor funcionando.")

    cl.close()
