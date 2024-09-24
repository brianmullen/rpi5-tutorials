from time import sleep
from gpiozero import MotionSensor

fps = 1/30.0
sensor = MotionSensor(18)

try:
    while True:
       print("detected: ", sensor.motion_detected)
       sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

sensor.close()
print('Done!')
