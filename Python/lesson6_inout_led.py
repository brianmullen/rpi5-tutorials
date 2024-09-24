from gpiozero import LED
from gpiozero import Button
from time import sleep

useHardwarePullup = False

if useHardwarePullup:
    btn = Button("BOARD40", pull_up=None, active_state=False)
else:
    btn = Button("BOARD40", pull_up=True)
led = LED("BOARD38")

try:
    print(btn.pull_up)
    btn.when_pressed = lambda: led.on()
    btn.when_released = lambda: led.off()
    while True:
        sleep(1)
except KeyboardInterrupt:
    print(' Interrupted')

btn.close()
led.close()
