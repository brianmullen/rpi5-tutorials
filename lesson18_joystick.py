from gpiozero import Button
from ADC0834 import ADC0834Device
from time import sleep

fps=1.0/60.0
adc0834 = ADC0834Device(select_pin=17, clock_pin=18, data_io_pin=23)
button = Button(pin=21)

try:
    button.when_released = lambda: print('button pressed')

    while True:
        xValue = adc0834.valueAt(0)
        yValue = adc0834.valueAt(1)

        print('X=', xValue, ' Y=', yValue)

        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

adc0834.close()
