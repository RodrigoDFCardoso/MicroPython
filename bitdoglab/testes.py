from machine import PWM, Pin
import neopixel
import time
import random
from machine import Pin, SoftI2C, ADC
from ssd1306 import SSD1306_I2C
import math

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

# Configuração do OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)


# Configurando o LED RGB
led_r = PWM(Pin(12))
led_g = PWM(Pin(13))
led_b = PWM(Pin(11))

led_r.freq(1000)
led_g.freq(1000)
led_b.freq(1000)

# Configuração do NeoPixel
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# definir cores para os LEDs
RED = (50, 0, 0)
GREEN = (0, 50, 0)
BLUE = (0, 0, 50)
YELLOW = (30, 30, 0)
MAGENTA = (30, 0, 30)
CYAN = (0, 30, 30)
WHITE = (25, 25, 25)
BLACK = (0, 0, 0)

# apagar todos os LEDs
def clear_all():
    for i in range(len(np)):
        np[i] = BLACK
    np.write()



def heart():
    """Acende um coração grande na matriz de LEDs."""
    # Primeiro, desligamos todos os LEDs para garantir que começa "limpo"
    clear_all()
    
    # Lista dos LEDs que devem ser acesos para o coração
    heart_leds = [2, 6, 14, 15, 23, 17, 21, 19, 10, 8]
    
    # Acendendo os LEDs em vermelho
    for led in heart_leds:
        np[led] = (255, 0, 0)  # RED
    
    np.write()

def smile_face():
    # Definindo a sequência de cores
    colors = [
        BLACK, BLUE, BLUE, BLUE, BLACK,
        BLUE, BLACK, BLACK, BLACK, BLUE,
        BLACK, BLACK, BLACK, BLACK, BLACK,
        BLACK, CYAN, BLACK, CYAN, BLACK,
        BLACK, BLACK, BLACK, BLACK, BLACK
    ]
    
    # Atribuindo as cores à matriz np
    for i, color in enumerate(colors):
        np[i] = color
    
    np.write()

#_______________________________________________
def update_oled(lines):
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 8)
    oled.show()

#update_oled("OLA HUMANO!")
messages = [
    "           ",
    "           ",
    "teste atualizado ddddddd",
    "           "
    "           ",
    "           ",
    "           ",
    "           "
]

messages = "teste atualizado ddddddd"
update_oled(messages)
