#out pwm in voltage 

import machine
import utime
from picozero import pico_led
from time import sleep

# Configurar o pino GP28 como entrada analógica
adc2 = machine.ADC(28)

# Ler o valor analógico
def valor_entrada():
    valor_analogico = adc2.read_u16()
    valor_tensao = valor_analogico / (65535) * 3.3
    print("Valor Analógico (GP28):", valor_analogico)
    print("Valor Tensão:", valor_tensao)

# Escolha o pino GPIO que você deseja usar para o PWM
pwm_pin = machine.Pin(0)  # Substitua 0 pelo número do pino desejado

# Crie um objeto PWM
pwm = machine.PWM(pwm_pin)

# Configura a frequência do PWM (em Hertz)
pwm.freq(1000)  # Por exemplo, 1000 Hz

# Determine o ciclo de trabalho necessário para obter 2V de saída
# O ciclo de trabalho é uma fração entre 0 (0%) e 1023 (100%)
def tensao(valor):
    tensao_desejada = valor  # Volts
    faixa_tensao = 3.3  # Faixa de tensão da Raspberry Pi Pico (0 a 3.3V)
    ciclo_de_trabalho = (valor / faixa_tensao) * 65535
    pwm.duty_u16(int(ciclo_de_trabalho))
    return ciclo_de_trabalho
#pwm.duty_u16(32768)

# Agora, você pode definir o ciclo de trabalho do PWM, variando de 0 (0%) a 1023 (100%)
#while True:
#    for duty in range(0, 3.3, 0.1):
#        pwm.duty_u16(duty * 32)
#        valor_entrada()
#        print(duty)
#        #utime.sleep_ms(1000)  # Espere um curto período de tempo
#        utime.sleep(1)  # Espere 1 segundo
#    for duty in range(1023, -1, -1):
#        pwm.duty_u16(duty * 1024)
#        valor_entrada()
#        utime.sleep_ms(1000)  # Espere um curto período de tempo
#    utime.sleep(1)  # Espere 1 segundo

inicio = 0.0  # Valor inicial (float)
fim = 3.3    # Valor final (float)
passo = 0.1  # Tamanho do passo (float)

# Use um loop for para criar a sequência de números de ponto flutuante
valores_float = []
valor_atual = inicio
while valor_atual <= fim:
    valores_float.append(valor_atual)
    valor_atual += passo
#print(valores_float)
# Imprima os valores float
for valor in valores_float:
    tensao(valor)
    valor_entrada()
    print(valor)
#while True:
 #   pico_led.on()
  #  sleep(0.5)
   # valor_entrada()
    #pico_led.off()
    #sleep(0.5)
    #pass
#    tensao(2)