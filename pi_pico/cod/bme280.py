

import time
import machine
import bme280_float as bme280

def bme280_values():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
    bme = bme280.BME280(i2c=i2c)
    
    return bme.values

while True:
    print(bme280_values())
    time.sleep(2)

print(bme.values)