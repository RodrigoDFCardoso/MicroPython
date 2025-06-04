import network
import socket
import json
from time import sleep
from machine import Pin

# Configurar Wi-Fi
ssid = "AP21_23"
password = "familiacardoso23"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Aguarde a conexão
while not wlan.isconnected():
    print("Conectando ao Wi-Fi...")
    sleep(1)

print("Conectado!", wlan.ifconfig())

# Dados simulados
def gerar_dados():
    return {
        "chart1": [10, 20, 30, 40],
        "chart2": [15, 25, 35, 45],
        "chart3": [20, 30, 40, 50],
        "chart4": [25, 35, 45, 55]
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
        # Responder com dados JSON
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(json.dumps(gerar_dados()))
    else:
        # Página HTML (ou mensagem simples)
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n")
        cl.send("Servidor funcionando.")

    cl.close()
