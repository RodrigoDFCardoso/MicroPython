#
# this script for the rp2040 port assumes the I2C connections at
# GPIO8 and 9. At the RPi Pico, these are the board pins 11 and 12
# Please check that pull-up resistors are in place at sda and scl.
#
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

#print(bme.values)