import utime
from machine import Pin, SoftI2C, ADC, I2C
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
 
#i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14), freq=200000)
oled = SSD1306_I2C(128, 64, i2c)

print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
 
 
#oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# Inicializar ADC para os pinos VRx (GPIO26) e VRy (GPIO27)
adc_vrx = ADC(Pin(26))
adc_vry = ADC(Pin(27))

oled.text("ADC: ",1,8)


x = 0

while True:
    for i in range(4):
        voltage = voltage_temp(readValueFrom(i))[0]
        temp = voltage_temp(readValueFrom(i))[1]
        
        utime.sleep(2)
        #print(f"{i}, {voltage}, {temp}, {readValueFrom(i)}")
        #vrx_value = adc_vrx.read_u16()
        vry_value = adc_vry.read_u16()
        #print(f"{vrx_value}, {vry_value}")
        
        if vry_value > 40000:
            if x == 0:
                x = 4
            else:
                x -= 1
        if vry_value < 20000:
            if x == 4:
                x = 0
            else:
                x += 1
        
        # Clear the oled display in case it has junk on it.
        oled.fill(0)
        
        # Add some text
        
        oled.text(f"Channel {i}",0,8)
        
        oled.text("Voltage: ",0,16)
        oled.text(str("{:.2f} V".format(voltage)),72,16)
    
        oled.text("Temp: ",0,24)
        oled.text(str("{:.2f} C".format(temp)),72,24)
        
        # controle joystick
        oled.text(f"Channel {x}",0,32)
        oled.text("Voltage: ",0,40)
        oled.text(str("{:.2f} V".format(voltage_temp(readValueFrom(x))[0])),72,40)
    
        oled.text("Temp: ",0,48)
        oled.text(str("{:.2f} C".format(voltage_temp(readValueFrom(x))[1])),72,48)
        
        # Finally update the oled display so the image & text is displayed
        oled.show()
    
        
        
        