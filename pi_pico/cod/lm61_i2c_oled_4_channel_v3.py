import utime
from machine import I2C, Pin

dev = I2C(0, scl=Pin(9), sda=Pin(8))
address = 72

print("Devices found:", dev.scan())

def readConfig():
    dev.writeto(address, bytearray([1]))
    result = dev.readfrom(address, 2)
    return result[0] << 8 | result[1]

print("Initial Config (bin):", bin(readConfig()))

def readValueFrom(channel):
    config = readConfig()
    
    # Clear MUX and PGA bits
    config &= ~(7 << 12) # clear MUX bits
    config &= ~(7 << 9)  # clear PGA bits
    
    # Set MUX for the channel and gain configuration
    config |= ((7 & (4 + channel)) << 12)
    config |= (1 << 15)  # Trigger next conversion
    config |= (1 << 9)   # Gain set for 4.096 V

    # Send updated config to ADC
    config_bytes = [config >> 8 & 0xFF, config & 0xFF]
    dev.writeto(address, bytearray([1] + config_bytes))
    
    # Wait for conversion to complete
    while (readConfig() & 0x8000) == 0:
        pass
        
    # Read the conversion result
    dev.writeto(address, bytearray([0]))
    result = dev.readfrom(address, 2)
    return result[0] << 8 | result[1]

def voltage_temp(val, max_val=26100, voltage_ref=3.3):
    voltage = val / max_val * voltage_ref
    temp = (voltage - 0.6) / 0.01
    return voltage, temp

val = [0, 0, 0, 0]

while True:
    # Read values from each channel and convert to temperature
    val[0] = readValueFrom(0)
    val[1] = readValueFrom(1)
    val[2] = readValueFrom(2)
    val[3] = readValueFrom(3)
    
    temperatures = [voltage_temp(i)[1] for i in val]
    print("Temperatures:", temperatures)
    
    utime.sleep(0.1)
