import time
from machine import Pin, SoftI2C, ADC, I2C
from ssd1306 import SSD1306_I2C
import machine
import neopixel
import ina226
import uasyncio as asyncio
import network
import socket
import json
import random


ssid = "Wifi BMS"
password = "testebms2024"
#ssid = "ehookconfig"
#password = "ehook123123123"
#ssid = "AP21_23"
#password = "familiacardoso23"
#conection = 0
#server = ''
#addr = ''
async def conection_wifi():
    global conection
    global ip
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Conectando à rede Wi-Fi...")
    max_wait = 10
    while not wlan.isconnected() and max_wait > 0:
        print("Aguardando conexão...")
        await asyncio.sleep(1)
        max_wait -= 1

    if wlan.isconnected():
        conection = 1
        ip = wlan.ifconfig()[0]
        print(ip)
        print("Conectado com IP:", wlan.ifconfig())
    else:
        print("Falha na conexão.")
        raise SystemExit
to_send = {
        'temp1': [],
        'temp2': [],
        'temp3': [],
        'temp4': [],
        'voltage1': [],
        'voltage2': [],
        'voltage3': [],
        'voltage4': [],
        'current1': [],
        'current2': [],
        'current3': [],
        'current4': []
    }

# Abra e leia o arquivo HTML
def load_html(filename):
    with open(filename, 'r') as file:
        return file.read()

# Função assíncrona para lidar com conexões
async def handle_client(reader, writer):
    # Receber a solicitação do cliente
    request = await reader.read(1024)
    request = request.decode('utf-8')
    print("Requisição recebida:\n", request)
    graf_get_data = load_html("graf_get_data.html")
    # Responder com JSON se a rota for "/data"
    if "GET /data" in request:
        #arrays = [[random.randint(1, 100) for _ in range(5)] for _ in range(4)]
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "\r\n"
        )
        writer.write(response.encode('utf-8'))
        writer.write(json.dumps(to_send))

    # Responder com a página HTML para outras rotas
    else:
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
        )
        writer.write(response.encode('utf-8'))
        writer.write(graf_get_data.encode('utf-8'))

    await writer.drain()  # Garante que os dados foram enviados
    await asyncio.sleep(0.1)  # Pausa breve para estabilidade
    writer.close()
    await writer.wait_closed()
    print("Conexão encerrada.")

# Função principal do servidor web
async def servidor_web():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("Servidor rodando...")
    while True:
        await asyncio.sleep(1)  # Mantém o loop ativo

##################################################################

# ads1115
dev = I2C(0, scl=Pin(9), sda=Pin(8))
address = 72

#oled
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Inicializar ADC para os pinos VRx (GPIO26) e VRy (GPIO27)
adc_vrx = ADC(Pin(26))
adc_vry = ADC(Pin(27))

# Número de LEDs na sua matriz 5x5
NUM_LEDS = 25

# Inicializar a matriz de NeoPixels no GPIO7
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Definindo a matriz de LEDs
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]

# definir cores para os LEDs
RED = (50, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 50, 0)
BLUE = (0, 0, 50)
YELLOW = (30, 30, 0)
#MAGENTA = (30, 0, 30)
#CYAN = (0, 30, 30)
#WHITE = (25, 25, 25)
BLACK = (0, 0, 0)    


def readConfig():
    dev.writeto(address, bytearray([1])) 
    result = dev.readfrom(address, 2)
    
    return result[0]<<8 | result[0]

# print(bin(readConfig()))

# read value from channel
def readValueFrom(channel):
    config = readConfig()
    
    config &= ~(7<<12)# clear MUX bits
    config &= ~(7<<9) # clear PGA
    
    config |= (7 & (4 + channel))<<12
    config |= (1<<15) # trigger next conversion
    config |= (1<<9) # gain 4.096 v
    
    config = [int(config>>i & 0xff) for i in [8,0]]
    
    dev.writeto(address, bytearray([1] + config))
    
    config = readConfig()
    while (config & 0x8000) == 0:
        config = readConfig()
        
    dev.writeto(address, bytearray([0]))
    result = dev.readfrom(address, 2)
    
    return result[0]<<8 | result[0]

# value to temperature 
def voltage_temp(val, max_val=26214, voltage_ref=3.3):
    voltage = val / max_val * voltage_ref
    temp = voltage * (17.9) - 10
    return voltage, temp


def LED_all(COLOR):
    for i in range(len(np)):
        np[i] = COLOR
    np.write()

def color_temp(temp):
    if temp < 20:
        color = BLUE
    if 20 < temp < 35:
        color = GREEN
    if 35 < temp < 50:
        color = YELLOW
    if 50 < temp < 65:
        color = ORANGE
    if temp > 65:
        color = RED

    #LED_all(color)
    LED_all(BLACK) #alterado para não acender
    
def select_chan(channel):
    options = {}

def white_oled(channel, y = 8):
    oled.fill(0)
    oled.text("ROTA 2030",0,0)
    oled.text("BMS Board v1",0,8)
    #oled.text("Board v1",64,16)
    oled.text("Reading...",0,24)
    voltage = voltage_temp(readValueFrom(channel))[0]
    temp = voltage_temp(readValueFrom(channel))[1]
    i_v = get_i_v(options[channel][1])
    color_temp(temp)
    # print(f'value channel {channel}: {readValueFrom(channel)}')
    # Add some text
    
    # map the inputs to the board
    #options = {0 : 'D', 1 : 'C', 2 : 'B', 3 : 'A'}
    
    chan = options[channel][0]
    oled.text(f"Channel: {chan}",0,y)
    
    oled.text("Temp: ",0,(y+8))
    oled.text(str("{:.2f} C".format(temp)),72,(y+8))
    
    oled.text("VxI: ",0,(y+16))
    oled.text(str("{:.1f}V".format(i_v[0])),36,(y+16))
    oled.text(str("{:.0f}mA".format(i_v[2])),72,(y+16))

    # Finally update the oled display so the image & text is displayed
    oled.show()

#LED_all(CYAN)

# oled.text("ADC: ",1,8)
def select_channel(channel):
    vry_value = adc_vry.read_u16()
    time.sleep(0.3)
    # print(vry_value)
    if vry_value > 60000:
        if channel == 3:
            channel = 0
        else:
            channel += 1
    if vry_value < 1000:
        if channel == 0:
            channel = 3
        else:
            channel -= 1
    
    return channel

# current and voltage
def get_i_v(address):

    i2c_ina226 = SoftI2C(scl=Pin(19), sda=Pin(18)) #definir qual pin i2c está
    ina = ina226.INA226(i2c_ina226, address)
    
    data_ina226_ = f'{ina.bus_voltage} {ina.shunt_voltage} {ina.current*1000} {ina.power}'
    data_ina226 = [ina.bus_voltage, ina.shunt_voltage, ina.current*1000, ina.power]
    voltage = ina.bus_voltage
    s_voltage = ina.shunt_voltage
    current = ina.current*1000
    power = ina.power

    return data_ina226


#define condicoes iniciais
options = {0 : ['D', 76], 1 : ['C', 72], 2 : ['B', 68], 3 : ['A', 64]}
timestamp = time.localtime()
file_name = 'data_%04d%02d%02d.csv'%(timestamp[0:3])
file=open(file_name,"a+b")  # file is created and opened in write mode
#channel = 3
#color = BLACK
#LED_all(color)
global timer
def gerar_dados(dados, timer):
    if timer > 20:
        if len(to_send['temp1']) >= 15:
            for i in to_send:
                to_send[i].pop(0)
                # print('OK....')


        to_send['temp1'].append([dados[3][0], dados[3][2]])
        to_send['temp2'].append([dados[2][0], dados[2][2]])
        to_send['temp3'].append([dados[1][0], dados[1][2]])
        to_send['temp4'].append([dados[0][0], dados[0][2]])

        to_send['voltage1'].append([dados[3][0], dados[3][3]])
        to_send['voltage2'].append([dados[2][0], dados[2][3]])
        to_send['voltage3'].append([dados[1][0], dados[1][3]])
        to_send['voltage4'].append([dados[0][0], dados[0][3]])

        to_send['current1'].append([dados[3][0], dados[3][4]])
        to_send['current2'].append([dados[2][0], dados[2][4]])
        to_send['current3'].append([dados[1][0], dados[1][4]])
        to_send['current4'].append([dados[0][0], dados[0][4]])
    
    # print(dados)
    #print(to_send)


async def save_data():
    # timestamp = time.localtime()
    # file_name = 'data_%04d%02d%02d.csv' % (timestamp[0:3])
    timer = 0
    # with open(file_name, "a") as file:  # Use um gerenciador de contexto para manipular o arquivo
    while True:
        dados = []
        for i in range(4):
            voltage = voltage_temp(readValueFrom(i))[0]
            temp = voltage_temp(readValueFrom(i))[1]
            i_v = get_i_v(options[i][1])
            data = f'{time.time()} {options[i][0]} {temp:.2f} {i_v[0]:.2f} {i_v[2]}'
            file.write(str(data) + "\n")
            file.flush()
            dados.append(data.split())
            print(data)
        gerar_dados(dados, timer)
        print(timer)
        timer += 1
        if timer > 21:
            timer = 0
        await asyncio.sleep(10)  # Salva os dados a cada 10 segundos

async def main_loop():
    channel = 3
    color = BLACK
    #LED_all(color)
    while True:
        
        channel = select_channel(channel)
        white_oled(channel, 32)
        await asyncio.sleep(0)  # Permite que o asyncio alterne entre as tarefas

async def main():
    # Inicializar todas as tarefas
    await asyncio.gather(
        conection_wifi(),
        save_data(),
        servidor_web(),
        main_loop()
    )

# Inicia o loop principal
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Encerrando...")
