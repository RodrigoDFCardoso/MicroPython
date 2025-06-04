import network
import time
import socket

ssid = "teste_web"
password = "teste@7890"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print("Conectado com IP:", wlan.ifconfig()[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Servidor ativo em:", addr)

while True:
    cl, addr = s.accept()
    print('Cliente conectado de', addr)
    request = cl.recv(1024)
    print("Requisição:", request)

    # Exemplo de resposta HTTP
    response = """\
    HTTP/1.1 200 OK
    Content-Type: text/html

    <html><body><h1>Dados da Pico W</h1><p>Olá, mundo! eaiii</p></body></html>
    """
    cl.send(response)
    cl.close()
