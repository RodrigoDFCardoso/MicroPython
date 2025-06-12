from machine import UART, Pin
from micropyGPS import MicropyGPS
import time

gps = MicropyGPS()

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def update_gps():
    if uart.any():
        linha = uart.readline()
        if linha:
            try:
                for b in linha:
                    gps.update(chr(b))
            except Exception as e:
                print('Erro ao processar linha:', e)

def mostrar_gps():
    if gps.latitude[0] != 0:
        lat = gps.latitude[0] + gps.latitude[1] / 60.0
        if gps.latitude[2] == 'S':
            lat = -lat

        lon = gps.longitude[0] + gps.longitude[1] / 60.0
        if gps.longitude[2] == 'W':
            lon = -lon

        try:
            hora = '{:02}:{:02}:{:02}'.format(gps.timestamp[0], gps.timestamp[1], gps.timestamp[2])
        except:
            hora = "Hora indisponível"

        try:
            data = '{:02}/{:02}/{:02}'.format(gps.date[2], gps.date[1], gps.date[0])
        except:
            data = "Data indisponível"

        print('Latitude:', lat)
        print('Longitude:', lon)
        print('Altitude:', gps.altitude)
        print('Data:', data)
        print('Hora:', hora)
    else:
        print('Aguardando fix do GPS...')

while True:
    update_gps()
    mostrar_gps()
    time.sleep(1)
