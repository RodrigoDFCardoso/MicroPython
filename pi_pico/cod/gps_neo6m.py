from machine import UART, Pin
import utime

# UART1: TX=GPIO0, RX=GPIO1
uart = UART(0,baudrate=9600, tx=Pin(0), rx=Pin(1))


def parse_gprmc(linha):
    try:
        partes = linha.split(',')
        if partes[0] == '$GPRMC' and partes[2] == 'A':  # A = válido
            hora = partes[1]
            lat_raw = partes[3]
            lat_dir = partes[4]
            lon_raw = partes[5]
            lon_dir = partes[6]

            # Converter latitude
            lat_graus = int(lat_raw[:2])
            lat_min = float(lat_raw[2:])
            latitude = lat_graus + lat_min / 60.0
            if lat_dir == 'S':
                latitude = -latitude

            # Converter longitude
            lon_graus = int(lon_raw[:3])
            lon_min = float(lon_raw[3:])
            longitude = lon_graus + lon_min / 60.0
            if lon_dir == 'W':
                longitude = -longitude

            # Converter hora
            horas = hora[0:2]
            minutos = hora[2:4]
            segundos = hora[4:6]
            horario = f"{horas}:{minutos}:{segundos} UTC"

            return latitude, longitude, horario
    except:
        pass
    return None, None, None

print("Lendo GPS...")
while True:
    if uart.any():
        linha = uart.readline()
        if linha:
            try:
                linha = linha.decode('utf-8').strip()
                #print(linha)
                lat, lon, hora = parse_gprmc(linha)
                if lat and lon:
                    print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}, Horário: {hora}")
            except UnicodeError:
                pass
    utime.sleep(0.1)
