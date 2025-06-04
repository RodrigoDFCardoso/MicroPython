import time
from machine import Pin, SoftI2C, ADC, I2C
from ssd1306 import SSD1306_I2C
import machine
import neopixel
import ina226
import uasyncio as asyncio

#define pin comunication for ina226 i2c

i2c_ina226 = SoftI2C(scl=Pin(19), sda=Pin(18)) #definir qual pin i2c está
ina = ina226.INA226(i2c_ina226, 68)

def get_i_v(address):
    
    data_ina226_ = f'{ina.bus_voltage} {ina.shunt_voltage} {ina.current*1000} {ina.power}'
    data_ina226 = [ina.bus_voltage, ina.shunt_voltage, ina.current*1000, ina.power]
    voltage = ina.bus_voltage
    s_voltage = ina.shunt_voltage
    current = ina.current*1000
    power = ina.power
    #print(data_ina226_)
    #time.sleep(5)
    return data_ina226

#for bme280
#	https://github.com/robert-hh/BME280


from machine import Pin, I2C
import bme280

i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Exemplo para ESP32
sensor = bme280.BME280(i2c=i2c)

# Lê os dados compensados (temperatura °C, pressão hPa, umidade %)
temp, pres, hum = sensor.read_compensated_data()

print("Temperatura: {:.2f} °C".format(temp / 100))
print("Pressão: {:.2f} hPa".format(pres / 25600))
print("Umidade: {:.2f} %".format(hum / 1024))
