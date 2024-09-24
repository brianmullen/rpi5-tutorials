from time import sleep
from DHT11 import DHT11Device

# Doesn't work on Pi5
fps = 1/30.0
sensor = DHT11Device(pin=17)

try:
    while True:
        result = sensor.read()
        if result.is_valid():
            print("Temperature: ", result.temperature, "Humidity: ", result.humidity)
        else:
            print("Error: ", result.error_code)
        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

sensor.close()
print('Done!')
