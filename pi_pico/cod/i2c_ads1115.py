import machine
import time

# Configurar o barramento I2C (usando os pinos GP9 e GP8 no Raspberry Pi Pico)
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=500000)  # Configurar frequência I2C

# Endereço I2C do ADS1115 (depende da configuração dos pinos ADDR)
# O endereço padrão é 0x48.
address = 72

# Configuração do ganho (para tensão de entrada de 3.3V, use 2/3x)
# Consulte o datasheet do seu ADS1115 para entender as opções de ganho.
gain = 2/3

# Configuração do canal de entrada (A0 no exemplo)
channel = 0

while True:
    # Configuração do comando de conversão (single-shot, ganho e canal)
    config = 0x8000 | (channel << 12) | (int(gain) << 9)

    # Enviar o comando de configuração para o ADS1115
    i2c.writeto(address, bytes([(config >> 8) & 0xFF, config & 0xFF]))

    # Aguarde a conversão ser concluída (tempo depende da taxa de dados)
    time.sleep(0.1)  # Pode ser necessário ajustar o tempo de espera

    # Ler os dados convertidos (2 bytes)
    data = i2c.readfrom(address, 2)
    value = (data[0] << 8) | data[1]
    print( data)

    # Calcular a tensão com base no valor lido e no ganho
    voltage = (value / 32767) * 3.048 * gain

    # Exibir a tensão lida
    print("Tensão lida (V):", voltage)

    # Esperar antes de fazer a próxima leitura
    time.sleep(1)
