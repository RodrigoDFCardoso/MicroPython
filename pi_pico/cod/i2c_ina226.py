import ina226
import time
from machine import Pin, SoftI2C

timestamp = time.localtime()
file_name = 'data_%04d%02d%02d.csv'%(timestamp[0:3])


# i2c
i2c = SoftI2C(scl=Pin(19), sda=Pin(18))
# ina226
ina = ina226.INA226(i2c, 64)

file=open(file_name,"a+b")	# file is created and opened in write mode
# default configuration and calibration value
while 1:
    data = f'{time.time()} {ina.bus_voltage} {ina.shunt_voltage} {ina.current*1000} {ina.power}'
    print(f'Bus Voltage: {ina.bus_voltage}')
    print(f'Bus Shunt Voltage: {ina.shunt_voltage}')
    print(f'Bus Current: {ina.current*1000} mA')
    print(f'Bus Power: {ina.power}')
    print(time.time())
    print(30*'_')
    file.write(str(data)+"\n")	# data is written as a string in the CSV file
    file.flush()		# internal buffer is flushed
    time.sleep(5)
    
    
    