import utime
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import framebuf
import machine

dev = I2C(1, scl=Pin(3), sda=Pin(2))

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


WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
 
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
 
# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
oled.text("ADC: ",1,8)



while True:
    for i in range(4):
        voltage = voltage_temp(readValueFrom(i))[0]
        temp = voltage_temp(readValueFrom(i))[1]
        
        utime.sleep(2)
        print(f"{i}, {voltage}, {temp}")
        # Clear the oled display in case it has junk on it.
        oled.fill(0)
        
        # Add some text
        
        oled.text(f"Channel {i}",0,8)
        
        oled.text("Voltage: ",0,16)
        oled.text(str("{:.2f} V".format(voltage)),72,16)
    
        oled.text("Temp: ",0,24)
        oled.text(str("{:.2f} C".format(temp)),72,24)
        
        # Finally update the oled display so the image & text is displayed
        oled.show()
    
        
        
        