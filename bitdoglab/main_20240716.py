import time
from machine import Pin, SoftI2C, ADC, I2C
from ssd1306 import SSD1306_I2C
import machine
import neopixel
import ina226
import uasyncio as asyncio

# ads1115
dev = I2C(1, scl=Pin(3), sda=Pin(2))
address = 72

#oled
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
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
    temp = voltage * (17.9) - 10
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
    oled.text("BMS Board v1",0,8)
    #oled.text("Board v1",64,16)
    oled.text("Reading...",0,24)
    voltage = voltage_temp(readValueFrom(channel))[0]
    temp = voltage_temp(readValueFrom(channel))[1]
    i_v = get_i_v(options[channel][1])
    color_temp(temp)
    # print(f'value channel {channel}: {readValueFrom(channel)}')
    # Add some text
    
    # map the inputs to the board
    #options = {0 : 'D', 1 : 'C', 2 : 'B', 3 : 'A'}
    
    chan = options[channel][0]
    oled.text(f"Channel: {chan}",0,y)
    
    oled.text("Temp: ",0,(y+8))
    oled.text(str("{:.2f} C".format(temp)),72,(y+8))
    
    oled.text("VxI: ",0,(y+16))
    oled.text(str("{:.1f}V".format(i_v[0])),36,(y+16))
    oled.text(str("{:.0f}mA".format(i_v[2])),72,(y+16))

    # Finally update the oled display so the image & text is displayed
    oled.show()

#LED_all(CYAN)

# oled.text("ADC: ",1,8)
def select_channel(channel):
    vry_value = adc_vry.read_u16()
    time.sleep(0.3)
    # print(vry_value)
    if vry_value > 60000:
        if channel == 3:
            channel = 0
        else:
            channel += 1
    if vry_value < 1000:
        if channel == 0:
            channel = 3
        else:
            channel -= 1
    
    return channel

# current and voltage
def get_i_v(address):
    #ina226 i2c
    if address != 68:
        data_ina226 = [0, 0, 0, 0]
        #print(data_ina226)

    else:
        address = 68
        i2c_ina226 = SoftI2C(scl=Pin(9), sda=Pin(8)) #definir qual pin i2c está
        ina = ina226.INA226(i2c_ina226, address)
        
        data_ina226_ = f'{ina.bus_voltage} {ina.shunt_voltage} {ina.current*1000} {ina.power}'
        data_ina226 = [ina.bus_voltage, ina.shunt_voltage, ina.current*1000, ina.power]
        voltage = ina.bus_voltage
        s_voltage = ina.shunt_voltage
        current = ina.current*1000
        power = ina.power
        #print(data_ina226_)
        #time.sleep(5)
    return data_ina226
'''
async def save_data():
    #options = {0 : ['D', 68], 1 : ['C', 0], 2 : ['B', 0], 3 : ['A', 0]}
    for i in range(4):
        data = ''
        voltage = voltage_temp(readValueFrom(i))[0]
        temp = voltage_temp(readValueFrom(i))[1]
        i_v = get_i_v(options[i][1])
        data = f'{time.time()} {options[i][0]} {temp} {i_v[0]} {i_v[1]} {i_v[2]} {i_v[3]}'
        file.write(str(data)+"\n")	# data is written as a string in the CSV file
        file.flush()		# internal buffer is flushed
        #file.close()
        print(data)
    time.sleep(5)
''' 

#define condicoes iniciais
options = {0 : ['D', 0], 1 : ['C', 0], 2 : ['B', 0], 3 : ['A', 68]}
timestamp = time.localtime()
file_name = 'data_%04d%02d%02d.csv'%(timestamp[0:3])
file=open(file_name,"a+b")	# file is created and opened in write mode
#channel = 3
#color = BLACK
#LED_all(color)
'''
while True:
    
    channel = select_channel(channel)
    
    white_oled(channel, 32)
    
    #get_i_v(68)
    
    save_data()
    
        
        
'''


async def save_data():
    while True:
        for i in range(4):
            data = ''
            voltage = voltage_temp(readValueFrom(i))[0]
            temp = voltage_temp(readValueFrom(i))[1]
            i_v = get_i_v(options[i][1])
            # data = 'timestamp channel temperature Voltage Shunt_Voltage current(mA) power'
            data = f'{time.time()} {options[i][0]} {temp} {i_v[0]} {i_v[1]} {i_v[2]} {i_v[3]}'
            file.write(str(data) + "\n")  # Os dados são escritos como string no arquivo CSV
            file.flush()  # O buffer interno é liberado
            print(data)
        await asyncio.sleep(10)

async def main_loop():
    channel = 3
    color = BLACK
    LED_all(color)
    while True:
        channel = select_channel(channel)
        white_oled(channel, 32)
        await asyncio.sleep(0)  # Permite que o asyncio alterne entre as tarefas

async def main():
    await asyncio.gather(
        save_data(),
        main_loop(),
    )

# Inicia o event loop
asyncio.run(main())

# Certifique-se de fechar o arquivo quando o programa terminar
file.close()


