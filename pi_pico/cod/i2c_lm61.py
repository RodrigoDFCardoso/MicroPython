import machine
import time

# Configurar os números dos pinos SDA e SCL
sda_pin = machine.Pin(2)  # Substitua pelo número do pino SDA desejado
scl_pin = machine.Pin(3)  # Substitua pelo número do pino SCL desejado

# Inicializar o barramento I2C
i2c = machine.I2C(1, sda=sda_pin, scl=scl_pin)

# Realizar uma varredura (scan) dos endereços I2C
dispositivos_conectados = i2c.scan()

# Endereço I2C do módulo ADS1115 (depende da configuração dos pinos ADR)
# Por padrão, o endereço é 0x48.
address = 0x48

# Configurar o ganho do ADS1115 (para tensão de entrada de 3.3V, use 2/3x)
# Consulte o datasheet do LM61 para entender a faixa de tensão do sensor e escolher o ganho apropriado.
gain = int(2 / 3)

# Configurar o canal de entrada do ADS1115 (canal 0 no exemplo)
channel = 3

# Configurar o modo de operação (single-shot)
config = 0x8000  # Bit MSB define o modo single-shot

while True:
    # Configurar a conversão no ADS1115
    config |= (channel << 12)  # Selecionar o canal de entrada
    config |= (gain << 9)      # Selecionar o ganho
    config |= 0x0100           # Taxa de dados de 128SPS (samples por segundo)

    # Iniciar uma única conversão
    i2c.writeto(address, bytearray([config >> 8, config & 0xFF]))

    # Aguardar o término da conversão (aproximadamente 8ms para 128SPS)
    time.sleep_ms(10)

    # Ler o valor da conversão
    data = i2c.readfrom(address, 2)
    value = (data[0] << 8) | data[1]

    # Calcular a tensão convertida (depende do ganho)
    voltage = (value / 65535) * 3.3
    #(adc_value / 65535) * 3.3

    # Calcular a temperatura com base na tensão (ajuste isso com base nas especificações do LM61)
    temperature_celsius = (voltage - 0.6) / 0.01

    # Exibir a temperatura em graus Celsius
    print("Temperatura (°C):", temperature_celsius)

    # Esperar um segundo antes de ler novamente
    time.sleep(1)