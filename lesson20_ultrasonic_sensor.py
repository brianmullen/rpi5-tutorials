from time import sleep
from gpiozero import DistanceSensor

fps = 1/5.0
sensor = DistanceSensor(echo=24, trigger=23)
feetInMeters = 3.28084
inchesInFeet = 12

try:
    while True:
       distance = sensor.distance * feetInMeters * inchesInFeet
       rounded = int(distance * 100) / 100.0
       print("inches: ", rounded)
       sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

sensor.close()
print('Done!')
