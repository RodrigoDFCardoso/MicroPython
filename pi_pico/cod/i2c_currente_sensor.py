import machine

# Configurar os números dos pinos SDA e SCL
sda_pin = machine.Pin(18)  # Substitua pelo número do pino SDA desejado
scl_pin = machine.Pin(19)  # Substitua pelo número do pino SCL desejado

# Inicializar o barramento I2C
i2c = machine.I2C(1, sda=sda_pin, scl=scl_pin)

# Realizar uma varredura (scan) dos endereços I2C
dispositivos_conectados = i2c.scan()[0]

# Exibir os endereços encontrados
print("Endereços I2C encontrados:", dispositivos_conectados)
