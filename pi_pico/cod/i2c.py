import machine


# Configurar os números dos pinos SDA e SCL
sda_pin = machine.Pin(8)  # Substitua pelo número do pino SDA desejado
scl_pin = machine.Pin(9)  # Substitua pelo número do pino SCL desejado

# Inicializar o barramento I2C
#i2c = machine.I2C(1, sda=sda_pin, scl=scl_pin)
i2c2 = machine.SoftI2C(sda=sda_pin, scl=scl_pin)
# SoftI2C
#print(i2c)
print(i2c2)
# Realizar uma varredura (scan) dos endereços I2C
#dispositivos_conectados = i2c.scan()
dispositivos_conectados2 = i2c2.scan()

# Exibir os endereços encontrados
#print("Endereços I2C encontrados:", dispositivos_conectados)
print("Endereços i2c2 encontrados:", dispositivos_conectados2)
