import network
import time
import socket

# Configurações da rede Wi-Fi
ssid = "teste_web"
password = "teste@7890"

ssid = "AP21_23"
password = "familiacardoso23"
# Configurações do IP estático
ip = "192.168.1.100"        # IP desejado
subnet = "255.255.255.0"    # Máscara de sub-rede
gateway = "192.168.1.1"     # Gateway (normalmente o IP do roteador)
dns = "8.8.8.8"             # Servidor DNS

# Conectar ao Wi-Fi com IP estático
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#wlan.ifconfig((ip, subnet, gateway, dns))

# Conectar à rede Wi-Fi
print("Conectando à rede Wi-Fi...")
wlan.connect(ssid, password)

# Aguarda a conexão
max_wait = 10
while not wlan.isconnected() and max_wait > 0:
    print("Aguardando conexão...")
    time.sleep(1)
    max_wait -= 1

if wlan.isconnected():
    print("Conectado com IP fixo:", wlan.ifconfig())
else:
    print("Falha na conexão. Verifique as credenciais ou o alcance da rede.")
    raise SystemExit

# Configurar o servidor
try:
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Servidor ativo em:", wlan.ifconfig()[0])

    while True:
        cl, addr = s.accept()
        print('Cliente conectado de', addr)
        request = cl.recv(1024)
        print("Requisição:", request)

        # Exemplo de resposta HTTP
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>Dados da Pico W</h1><p>Olá, mundo! eai</p></body></html>
"""
        cl.send(response)
        cl.close()

except Exception as e:
    print("Erro no servidor:", e)
    s.close()
