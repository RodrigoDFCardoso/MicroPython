from machine import I2C, Pin
import struct

# Endereço do INA226 (padrão 0x40)
INA226_ADDR = 0x40
SHUNT_VOLTAGE_REG = 0x01  # Registrador de tensão no shunt
CURRENT_REG = 0x04        # Registrador de corrente (se calibrado)

# Configurar I2C no Raspberry Pi Pico (GPIO 16 e 17, por exemplo)
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

# Função para ler valores do registrador
def read_register(reg):
    data = i2c.readfrom_mem(INA226_ADDR, reg, 2)
    value = struct.unpack('>h', data)[0]  # Converte para inteiro com sinal
    return value

# Ler a tensão no shunt
v_shunt = read_register(SHUNT_VOLTAGE_REG) * 2.5e-6  # Conversão para volts (2.5µV por LSB)
print(v_shunt)
# Definir resistência do shunt (exemplo: 0.01 ohm)
r_shunt = 0.1  

# Calcular corrente
corrente = v_shunt / r_shunt *1000 # Pode ser negativa!

print(f"Corrente: {corrente:.3f} mA")
