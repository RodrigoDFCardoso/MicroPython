from picozero import pico_led, LED
from time import sleep
from picozero import pinout

pinout()
led = LED(14) # Control an LED connected to pin GP14
while True:
    pico_led.on() # Turn on the LED on the Raspberry Pi Pico
    led.off()
    sleep(0.5)
    pico_led.off()
    led.brightness = 0.1
    led.on()
    sleep(0.5)
    
    #led.toggle() # Toggle an LED to turn it from on to off or off to on
    #sleep(1)
    #led.blink()
    