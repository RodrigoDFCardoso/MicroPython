from picozero import Button, pico_led
from time import sleep

button = Button(18)

# while True:
#     if button.is_pressed:
#         print("Button is pressed")
#     else:
#         print("Button is not pressed")
#     sleep(0.1)

def led_on_off():
    pico_led.on()
    sleep(1)
    pico_led.off()
    
button.when_pressed = led_on_off