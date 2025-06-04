from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

def send_csv(file_path):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                uart.write(line)
                print("Sent:", line.strip())
                time.sleep(0.1)
    except OSError:
        print("File not found. Make sure the file is uploaded correctly.")


send_csv("/username.csv")
