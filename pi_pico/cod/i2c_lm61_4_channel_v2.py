import utime
from machine import I2C, Pin

dev = I2C(0, scl=Pin(9), sda=Pin(8))

print(dev.scan())

address = 72

def readConfig():
    dev.writeto(address, bytearray([1]))
    result = dev.readfrom(address, 2)
    
    return result[0]<<8 | result[0]

print(bin(readConfig()))

def readValueFrom(channel):
    config = readConfig()
    
    config &= ~(7<<12)#	clear MUX bits
    config &= ~(7<<9) #	clear PGA
    
    config |= (7 & (4 + channel))<<12
    config |= (1<<15) # trigger next conversion
    config |= (1<<9) # gain 4.096 v
    
    config = [int(config>>i & 0xff) for i in [8,0]]
    
    dev.writeto(address, bytearray([1] + config))
    
    config = readConfig()
    while (config & 0x8000) == 0:
        config = readConfig()
        
    dev.writeto(address, bytearray([0]))
    result = dev.readfrom(address, 2)
    
    return result[0]<<8 | result[0]

def voltage_temp(val, max_val=26100, voltage_ref=3.3):
    voltage = val / max_val * voltage_ref
    temp = (voltage - 0.6) / 0.01
    return voltage, temp

val = [0,0,0,0]

while True:
    val[0] = readValueFrom(0)
    val[1] = readValueFrom(1)
    val[2] = readValueFrom(2)
    val[3] = readValueFrom(3)
    
    print([voltage_temp(i)[1] for i in val])
    
    
    utime.sleep(0.1)
