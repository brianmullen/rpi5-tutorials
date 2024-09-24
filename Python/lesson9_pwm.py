from gpiozero import PWMLED
from gpiozero import Button
from time import sleep

led = PWMLED("BOARD37", frequency=100)
incButton = Button("BOARD32")
decButton = Button("BOARD36")
increment = 1.5849
steps = 0
brightness = 0
fps=1.0/60.0

def incBrightness():
    global increment, steps, brightness

    steps = min(steps + 1, 10)
    if steps == 10:
        brightness = 1
    else:
        brightness = min(increment**steps, 100) / 100
        brightness = min(max(brightness, 0.0), 1.0)

def decBrightness():
    global increment, steps, brightness

    steps = max(steps - 1, 0)
    if steps == 0:
        brightness = 0
    else:
        brightness = max(increment**steps, 0) / 100
        brightness = min(max(brightness, 0.0), 1.0)

try:
    led.value = brightness
    incButton.when_released = lambda: incBrightness()
    decButton.when_released = lambda: decBrightness()

    while True:
        led.value = brightness
        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

led.value = 0
led.close()
incButton.close()
decButton.close()
