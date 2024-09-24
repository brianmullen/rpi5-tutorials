from gpiozero import PWMLED
from ADC0834 import ADC0834Device
from time import sleep

fps=1.0/60.0
adc0834 = ADC0834Device(select_pin=17, clock_pin=18, data_io_pin=23)
led = PWMLED(pin=26, frequency=1000)

try:
    while True:
        brightness = adc0834.value / 255.0
        led.value = brightness
        print(brightness)
        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

led.close()
adc0834.close()
