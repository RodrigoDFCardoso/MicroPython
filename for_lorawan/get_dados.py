from machine import Pin, SoftI2C, UART
import ssd1306
import time

# Endereço I2C do INA226
INA226_ADDR = 0x40  # Endereço padrão do INA226

# Configuração I2C para o INA226
i2c = SoftI2C(scl=Pin(3), sda=Pin(2))  # SCL e SDA conforme seu setup

#UART GPS NEO06m
uart = UART(0,baudrate=9600, tx=Pin(0), rx=Pin(1))

# Configuração I2C para o OLED
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Definir registradores
CONFIG_REG = 0x00
SHUNT_VOLTAGE_REG = 0x01
BUS_VOLTAGE_REG = 0x02
POWER_REG = 0x03
CURRENT_REG = 0x04
CALIBRATION_REG = 0x05

# Configuração do INA226 (Exemplo básico)
def configurar_ina226():
    # Configurar o INA226 para uma leitura contínua de corrente e potência
    config = 0x4127  # Configuração: medir corrente, potência e tensão (exemplo)
    i2c.writeto_mem(INA226_ADDR, CONFIG_REG, bytearray([config >> 8, config & 0xFF]))

# Função para ler a tensão no barramento (VBUS)
def ler_tensao_bus():
    data = i2c.readfrom_mem(INA226_ADDR, BUS_VOLTAGE_REG, 2)
    bus_voltage = (data[0] << 8 | data[1]) * 1.25 / 1000  # Conversão para Volts (1.25mV/bit)
    return bus_voltage

# Função para ler a tensão no resistor de shunt
def ler_tensao_shunt():
    data = i2c.readfrom_mem(INA226_ADDR, SHUNT_VOLTAGE_REG, 2)
    raw = (data[0] << 8) | data[1]
    if raw > 32767:
        raw -= 65536  # Corrigir valor negativo (conversão de complemento de dois)
    shunt_voltage = raw * 2.5 / 1_000_000  # Volts (2.5 µV/bit)
    return shunt_voltage


# Função para ler a corrente (dependendo do valor do shunt)
def ler_corrente(shunt_resistor):
    shunt_voltage = ler_tensao_shunt()
    corrente = shunt_voltage / shunt_resistor  # I = V / R (resultado com sinal)
    corrente_mA = -corrente * 1000  # inverter sinal
    return corrente_mA


# Função para calcular a potência (P = V * I)
def calcular_potencia(v_bus, corrente):
    potencia_W = v_bus * corrente / 1000  # Potência em Watts
    potencia_mW = potencia_W * 1000  # Converter de W para mW
    return potencia_mW

# Configurar o INA226
configurar_ina226()

# Resistor de shunt (em ohms)
shunt_resistor = 0.1  # 0.1 ohms

# Função para exibir informações no OLED
def exibir_no_oled(v_bus, corrente, potencia, lat, lon, hora):
    oled.fill(0)  # Limpar o display
    oled.text("V:{:.2f}V {}".format(v_bus, hora), 0, 0)  # Primeira linha: Tensão
    # Corrente com sinal
    oled.text("I: {:+.2f}mA".format(corrente), 0, 16)  # Corrente (mA) com sinal
    oled.text("P: {:+.2f}mW".format(potencia), 0, 32)  # Potência (mW)
    #oled.text("Shunt: {:+.3f}mV".format(ler_tensao_shunt() * -1000), 0, 48)  # Tensão de Shunt (mV)
    oled.text("GPS:{},{}".format(lat, lon), 0, 48) 
    oled.show()  # Atualizar o display

def parse_gprmc(linha):
    try:
        partes = linha.split(',')
        if partes[0] == '$GPRMC' and partes[2] == 'A':  # A = válido
            hora = partes[1]
            # print(hora)
            lat_raw = partes[3]
            lat_dir = partes[4]
            lon_raw = partes[5]
            lon_dir = partes[6]

            # Converter latitude
            lat_graus = int(lat_raw[:2])
            lat_min = float(lat_raw[2:])
            latitude = lat_graus + lat_min / 60.0
            #if lat_dir == 'S':
               # latitude = -latitude
            latitude = f'{latitude:.1f}{lat_dir}'
            
            # Converter longitude
            lon_graus = int(lon_raw[:3])
            lon_min = float(lon_raw[3:])
            longitude = lon_graus + lon_min / 60.0
            #if lon_dir == 'W':
               # longitude = -longitude
            longitude = f'{longitude:.1f}{lon_dir}'
            # Converter hora
            horas = hora[0:2]
            minutos = hora[2:4]
            segundos = hora[4:6]
            horario = f"{horas}:{minutos}:{segundos} UTC"

            return latitude, longitude, horario
        else:
            return None, None, None
    except:
        pass
    return None, None, None

def gps_signal():
    if uart.any():
        linha = uart.readline()
        if linha:
            try:
                linha = linha.decode('utf-8').strip()
                print(linha)
                lat, lon, hora = parse_gprmc(linha)
                if lat and lon:
                    #print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}, Horário: {hora}")
                    return [lat, lon, hora]
            except UnicodeError:
                pass

loc = [0, 0, 0]
# Loop principal
while True:
    # Ler valores
    v_bus = ler_tensao_bus()
    corrente = ler_corrente(shunt_resistor)
    potencia = calcular_potencia(v_bus, corrente)
    dados_gps = gps_signal()
    if  dados_gps != None:
        loc= dados_gps
    print(loc)
    # Exibir no OLED
    exibir_no_oled(v_bus, corrente, potencia, loc[0], loc[1], loc[2])

    time.sleep(1)

