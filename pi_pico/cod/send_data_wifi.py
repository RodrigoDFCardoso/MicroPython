import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import os

ssid = 'AP21_23'
password = 'familiacardoso23'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

try:
    connect()
except KeyboardInterrupt:
    machine.reset()

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data.append(line.strip().split(','))
    return data

def web_page():
    data = read_csv('dados.csv')
    print(data)
    html = """<!DOCTYPE html>
    <html>
    <head><title>Dashboard</title></head>
    <body><h1>Dashboard</h1><table border="1">"""
    for row in data:
        html += "<tr>"
        for col in row:
            html += f"<td>{col}</td>"
        html += "</tr>"
    html += "</table><script>setTimeout(()=>{location.reload();}, 5000);</script></body></html>"
    return html

addr = socket.getaddrinfo('192.168.15.100', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)

print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    response = web_page()
    cl.send('HTTP/1.1 200 OK\n')
    cl.send('Content-Type: text/html\n')
    cl.send('Connection: close\n\n')
    cl.sendall(response)
    cl.close()
