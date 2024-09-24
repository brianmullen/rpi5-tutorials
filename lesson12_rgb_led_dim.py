from gpiozero import RGBLED
from gpiozero import Button
from time import sleep
from enum import Enum

fps=1.0/60.0
led = RGBLED(red="BOARD37", green="BOARD35", blue="BOARD33")
red = Button("BOARD40", pull_up=True, bounce_time=0.1)
green = Button("BOARD38", pull_up=True, bounce_time=0.1)
blue = Button("BOARD36", pull_up=True, bounce_time=0.1)
redValue=0.99
greenValue=0.99
blueValue=0.99

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def brighten(colors, increment, minValue, maxValue):
    global led, redValue, greenValue, blueValue

    if Color.RED in colors:
        redValue *= increment
        if redValue > maxValue:
            redValue = minValue
        led.red = int(redValue) / maxValue
    if Color.GREEN in colors:
        greenValue *= increment
        if greenValue > maxValue:
            greenValue = minValue
        led.green = int(greenValue) / maxValue
    if Color.BLUE in colors:
        blueValue *= increment
        if blueValue > maxValue:
            blueValue = minValue
        led.blue = int(blueValue) / maxValue
        
try:
    led.red = 0.0
    led.green = 0.0
    led.blue = 0.0
    red.when_released = lambda: brighten({Color.RED}, 1.5849, 0.99, 100.0)
    green.when_released = lambda: brighten({Color.GREEN}, 1.5849, 0.99, 100.0)
    blue.when_released = lambda: brighten({Color.BLUE}, 1.5849, 0.99, 100.0)

    while True:
        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

led.close()
red.close()
green.close()
blue.close()
