import utime
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import framebuf
import machine

class ADCDevice:
    def __init__(self, i2c_bus, address=72):
        self.i2c = i2c_bus
        self.address = address

    def read_config(self):
        self.i2c.writeto(self.address, bytearray([1]))
        result = self.i2c.readfrom(self.address, 2)
        return result[0] << 8 | result[1]


    def read_value(self, channel):
        config = self.read_config()
        
        config &= ~(7<<12)# clear MUX bits
        config &= ~(7<<9) # clear PGA
        
        config |= (7 & (4 + channel))<<12
        config |= (1<<15) # trigger next conversion
        config |= (1<<9) # gain 4.096 v
        
        config = [int(config>>i & 0xff) for i in [8,0]]
        
        self.i2c.writeto(self.address, bytearray([1] + config))
        
        # config = readConfig()
        # while (config & 0x8000) == 0:
        #     config = readConfig()
            
        self.i2c.writeto(self.address, bytearray([0]))
        result = self.i2c.readfrom(self.address, 2)
        
        return result[0]<<8 | result[0]

    @staticmethod
    def val_to_voltage(val, max_val=26100, voltage_ref=3.3):
        return val / max_val * voltage_ref

i2c_bus = I2C(1, scl=Pin(3), sda=Pin(2))
devices = i2c_bus.scan()

for device in devices:
    print(device)

adc = ADCDevice(i2c_bus)
print(bin(adc.read_config()))

"""
while True:
    val = adc.read_value()
    voltage = adc.val_to_voltage(val)
    # Calcular a temperatura com base na tensão (ajuste isso com base nas especificações do LM61)
    temperature_celsius = (voltage - 0.6) / 0.01
    print("ADC Value:", val, "Voltage: {:.5f} V".format(voltage), "Temperature: {:.2f} °C".format(temperature_celsius))

    utime.sleep(0.5)
""" 

#sensor_temp = machine.ADC(28)
#conversion_factor = 3.3 / (65535)
 
WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
 
i2c = I2C(0, scl=Pin(9), sda=Pin(8))       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
 
# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
oled.text("ADC: ",1,8)
while True:
    for i in range(4):
    
        val = adc.read_value(i)
        voltage = adc.val_to_voltage(val)
        # Calcular a temperatura com base na tensão (ajuste isso com base nas especificações do LM61)
        temperature_celsius = (voltage - 0.6) / 0.01
        #print("ADC Value:", val, "Voltage: {:.5f} V".format(voltage), "Temperature: {:.2f} °C".format(temperature_celsius))
        print(f"{i}, {voltage}, {temperature_celsius}")
        utime.sleep(2)
        
        #reading = sensor_temp.read_u16() * conversion_factor
        # Load the raspberry pi logo into the framebuffer (the image is 32x32)
        #fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
     
        # Clear the oled display in case it has junk on it.
        oled.fill(0)
        
         # Blit the image from the framebuffer to the oled display
        #oled.blit(fb, 96, 0)
           
        
        # Add some text
        oled.text("Voltage: ",0,8)
        oled.text(str("{:.2f} V".format(voltage)),72,8)
        
        oled.text("Temp: ",0,16)
        oled.text(str("{:.2f} C".format(temperature_celsius)),72,16)
        
        oled.text(f"CHANNEL {i}",0,24)
     
        # Finally update the oled display so the image & text is displayed
        oled.show()

