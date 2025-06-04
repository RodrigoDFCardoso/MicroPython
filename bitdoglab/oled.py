import machine
import ssd1306

i2c = machine.I2C(1, scl=machine.Pin(15), sda=machine.Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Ativar pixel na posição (0, 0)
#oled.pixel(0, 0, 1)

# Atualizar o display
#oled.show()
