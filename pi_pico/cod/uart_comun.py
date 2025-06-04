import machine
from picozero import pico_led
from time import sleep

# Configurar UART0 com GP0 (TX) e GP1 (RX)
tx_pin = machine.Pin(0)  # Substitua 0 pelo número do pino desejado para TX
rx_pin = machine.Pin(1)  # Substitua 1 pelo número do pino desejado para RX
uart0 = machine.UART(0, tx=tx_pin, rx=rx_pin, baudrate=9600)

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
    if uart0.any():  # Verifica se há dados disponíveis para leitura
        mensagem_recebida = uart0.readline()
        print("Mensagem Recebida:", mensagem_recebida.decode("utf-8").strip())
