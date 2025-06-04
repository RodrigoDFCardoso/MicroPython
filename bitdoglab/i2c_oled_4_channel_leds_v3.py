import utime
from machine import Pin, SoftI2C, ADC, I2C
from ssd1306 import SSD1306_I2C
import machine
import neopixel

# ads1115
dev = I2C(1, scl=Pin(3), sda=Pin(2))
address = 72

#oled
i2c = SoftI2C(scl=Pin(15), sda=Pin(14), freq=200000)
oled = SSD1306_I2C(128, 64, i2c)

# Inicializar ADC para os pinos VRx (GPIO26) e VRy (GPIO27)
adc_vrx = ADC(Pin(26))
adc_vry = ADC(Pin(27))

# Número de LEDs na sua matriz 5x5
NUM_LEDS = 25

# Inicializar a matriz de NeoPixels no GPIO7
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Definindo a matriz de LEDs
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]

# definir cores para os LEDs
RED = (50, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 50, 0)
BLUE = (0, 0, 50)
YELLOW = (30, 30, 0)
#MAGENTA = (30, 0, 30)
#CYAN = (0, 30, 30)
#WHITE = (25, 25, 25)
BLACK = (0, 0, 0)    


def readConfig():
    dev.writeto(address, bytearray([1])) 
    result = dev.readfrom(address, 2)
    
    return result[0]<<8 | result[0]

# print(bin(readConfig()))

# read value from channel
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

# value to temperature 
def voltage_temp(val, max_val=26214, voltage_ref=3.3):
    voltage = val / max_val * voltage_ref
    temp = voltage * (17.9) + 8.4
    return voltage, temp


def LED_all(COLOR):
    for i in range(len(np)):
        np[i] = COLOR
    np.write()

def color_temp(temp):
    if temp < 20:
        color = BLUE
    if 20 < temp < 35:
        color = GREEN
    if 35 < temp < 50:
        color = YELLOW
    if 50 < temp < 65:
        color = ORANGE
    if temp > 65:
        color = RED

    LED_all(color)
    
def select_chan(channel):
    options = {}

def white_oled(channel, y = 8):
    oled.fill(0)
    oled.text("ROTA 2030",0,0)
    oled.text("Temperature",0,8)
    oled.text("Board v1",64,16)
    oled.text("Reading...",0,24)
    voltage = voltage_temp(readValueFrom(channel))[0]
    temp = voltage_temp(readValueFrom(channel))[1]
    color_temp(temp)
    # print(f'value channel {channel}: {readValueFrom(channel)}')
    # Add some text
    
    # map the inputs to the board
    options = {0 : 'D', 1 : 'C', 2 : 'B', 3 : 'A'}
    
    chan = options[channel]
    oled.text(f"Channel: {chan}",0,y)
    
    oled.text("Voltage: ",0,(y+8))
    oled.text(str("{:.2f} V".format(voltage)),72,(y+8))

    oled.text("Temp: ",0,(y+16))
    oled.text(str("{:.2f} C".format(temp)),72,(y+16))
    
    # Finally update the oled display so the image & text is displayed
    oled.show()

#LED_all(CYAN)

# oled.text("ADC: ",1,8)
def select_channel(channel):
    vry_value = adc_vry.read_u16()
    utime.sleep(0.3)
    # print(vry_value)
    if vry_value > 60000:
        if channel == 0:
            channel = 3
        else:
            channel -= 1
    if vry_value < 1000:
        if channel == 3:
            channel = 0
        else:
            channel += 1
    
    return channel

channel = 3
color = BLACK
LED_all(color)
while True:
    #vry_value = adc_vry.read_u16()
    #print(f"{vrx_value}, {vry_value}")
    
    # if vry_value > 40000:
    #     if x == 0:
    #         x = 4
    #     else:
    #         x -= 1
    # if vry_value < 20000:
    #     if x == 4:
    #         x = 0
    #     else:
    #         x += 1
    
    # if voltage_temp(readValueFrom(channel))[1] < 20:
    #     color = BLUE
    # if 20 < voltage_temp(readValueFrom(channel))[1] < 35:
    #     color = GREEN
    # if 35 < voltage_temp(readValueFrom(channel))[1] < 50:
    #     color = YELLOW
    # if 50 < voltage_temp(readValueFrom(channel))[1] < 65:
    #     color = ORANGE
    # if voltage_temp(readValueFrom(channel))[1] > 65:
    #     color = RED
    
    # Clear the oled display in case it has junk on it.
    # oled.fill(0)
    # Add some text

    channel = select_channel(channel)
    
    white_oled(channel, 32)

    
    #LED_all(color)

    # for i in range(4):
    #     voltage = voltage_temp(readValueFrom(i))[0]
    #     temp = voltage_temp(readValueFrom(i))[1]
        

    #     utime.sleep(2)
    #     #print(f"{i}, {voltage}, {temp}, {readValueFrom(i)}")
    #     #vrx_value = adc_vrx.read_u16()
        
    #     white_oled(i, 8)
    #     # Finally update the oled display so the image & text is displayed
    # oled.show()
    
        
        
