import network
import time
import socket
import os

# Configurações da rede Wi-Fi
ssid = "teste_web"
password = "teste@7890"

# Configurações do IP estático
ip = "192.168.1.100"
subnet = "255.255.255.0"
gateway = "192.168.1.1"
dns = "8.8.8.8"

# Conectar ao Wi-Fi com IP estático
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#wlan.ifconfig((ip, subnet, gateway, dns))

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
    print("Falha na conexão.")
    raise SystemExit

# Função para listar arquivos CSV
def listar_csv():
    arquivos = os.listdir()
    csv_files = [f for f in arquivos if f.endswith('.csv')]
    return csv_files

# Função para enviar o conteúdo do arquivo CSV
def enviar_arquivo(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"

def gerar_lista_arquivos():
    arquivos = listar_csv()
    if not arquivos:
        return "<p>Nenhum arquivo CSV encontrado.</p>"
    
    lista_html = ""
    for arquivo in arquivos:
        lista_html += f'<div class="file-item"><button class="button" onclick="downloadFile(\'{arquivo}\')">Baixar {arquivo}</button></div>'
    return lista_html

# Função para enviar a página HTML corretamente
# Função para enviar a página HTML corretamente
def enviar_pagina_html(cl):
    file_list_html = gerar_lista_arquivos()
    response = f"""\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
Connection: close\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>Servidor Pico W</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
        h1 {{ color: #333; }}
        .file-list {{ margin-top: 20px; }}
        .file-item {{ margin: 10px; }}
        .button {{
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border-radius: 8px;
        }}
        .button:hover {{ background-color: #45a049; }}
    </style>
</head>
<body>
    <h1>Arquivos CSV na Pico W</h1>
    <div class="file-list">
        {file_list_html}
    </div>
    <script>
        function downloadFile(filename) {{
            fetch('/download?file=' + filename)
            .then(response => response.text())
            .then(data => {{
                const blob = new Blob([data], {{ type: 'text/csv' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                a.click();
                URL.revokeObjectURL(url);
            }})
            .catch(error => console.error('Erro:', error));
        }}
    </script>
</body>
</html>
"""
    # Enviar a resposta
    cl.send(response.encode('utf-8'))
    cl.close()



# Iniciar o servidor
try:
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Servidor ativo em:", wlan.ifconfig()[0])

    while True:
        cl, addr = s.accept()
        print('Cliente conectado de', addr)
        request = cl.recv(1024).decode('utf-8')
        print("Requisição:", request)
        
        # Verificar a solicitação para download
        if 'GET /download?file=' in request:
            filename = request.split('file=')[-1].split(' ')[0]
            content = enviar_arquivo(filename)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/csv\r\nConnection: close\r\n\r\n{content}"
            cl.send(response.encode('utf-8'))
        else:
            enviar_pagina_html(cl)

except Exception as e:
    print("Erro no servidor:", e)
    s.close()
