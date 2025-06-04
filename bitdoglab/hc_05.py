from machine import UART, Pin
import time

# Initialize UART on GPIO 16 (TX) and GPIO 17 (RX)
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

def send_data(data):
    uart.write(data + '\n')  # Send data to HC-05

def receive_data():
    if uart.any():
        return uart.read().decode('utf-8')  # Read and decode incoming data
    return None

while True:
    # Send a test message
    send_data("Hello from Pico!")
    #print("Sent: Hello from Pico!")

    # Check for incoming data
    data = receive_data()
    if data :
        print("Received:", data)
        
        if "teste" in data:
            print('ok')
            print(f'{data}.')
        else:
            print('nao ok')
    time.sleep(1)
