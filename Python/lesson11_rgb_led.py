from gpiozero import RGBLED
from gpiozero import Button
from time import sleep
from enum import Enum

fps=1.0/60.0
led = RGBLED(red="BOARD37", green="BOARD35", blue="BOARD33")
red = Button("BOARD40", pull_up=True, bounce_time=0.1)
green = Button("BOARD38", pull_up=True, bounce_time=0.1)
blue = Button("BOARD36", pull_up=True, bounce_time=0.1)

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def toggle(colors):
    global led

    print(colors)
    if Color.RED in colors:
        led.red = not led.red
    if Color.GREEN in colors:
        led.green = not led.green
    if Color.BLUE in colors:
        led.blue = not led.blue

try:
    led.red = 0.0
    led.green = 0.0
    led.blue = 0.0
    red.when_released = lambda: toggle({Color.RED})
    green.when_released = lambda: toggle({Color.GREEN})
    blue.when_released = lambda: toggle({Color.BLUE})

    while True:
        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

led.close()
red.close()
green.close()
blue.close()
