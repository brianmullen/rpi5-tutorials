from gpiozero import RGBLED
from ADC0834 import ADC0834Device
from time import sleep

fps=1.0/60.0
adc0834 = ADC0834Device(select_pin=17, clock_pin=18, data_io_pin=23)
led = RGBLED(red=16, green=20, blue=21)

try:
    while True:
        redValue = adc0834.valueAt(0) / 255.0
        greenValue = adc0834.valueAt(1) / 255.0
        blueValue = adc0834.valueAt(2) / 255.0

        led.red = redValue
        led.green = greenValue
        led.blue = blueValue

        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

led.close()
adc0834.close()
