import machine
import time

# Configurar o pino ADC (por exemplo, GP26)
adc = machine.ADC(26)

while True:
    # Ler o valor do ADC
    adc_value = adc.read_u16()
    
    # Converter o valor do ADC em temperatura
    voltage = (adc_value / 65535) * 3.3  # 3.3V é a tensão de referência
    temperature_celsius = ((voltage - 0.6) / 0.01)
    
    # Exibir a temperatura em graus Celsius
    print("Temperatura (°C):", temperature_celsius)
    
    # Esperar um segundo antes de ler novamente
    time.sleep(1)
