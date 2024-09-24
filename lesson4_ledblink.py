# terminal: jobs
#           - list suspended tasks
#           fg
#           - returns suspended task back to foreground

from gpiozero import LED
from time import sleep

red = LED("BOARD40")

try:    
    while True:
        blinkTimes=int(input('How many times do you want the LED to blink? '))
        for i in range(0, blinkTimes, 1):
            red.on()
            sleep(1)
            red.off()
            sleep(1)
except KeyboardInterrupt:
    print(' Interrupted')

red.close()
