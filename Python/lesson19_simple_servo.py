from gpiozero import Servo, PWMLED
from time import sleep
from Pi5Servo import PWMPin

fps = 1/60.0
period = 0.02 # 20ms; 
frequency = 1 / period # 50Hz
# servo = PWMOutputDevice(21, frequency=int(frequency), initial_value=0)
# pwm0 = PWMPin(18)
# pwm0.set(1500)
# servo = Servo(12)
led = PWMLED(18, frequency=frequency)

try:
    led.value = 8.0/100.0
    # pwm0.set(1500)
    # pwm0.enable(True)
    # sleep(2)

    # for i in range(0, 10, 1):
    #     for v in range(-1000, 1000, 50):
    #         pwm0.set(1500+v)
    #         sleep(0.2)
    #     for v in range(1000, -1000, -50):
    #         pwm0.set(1500+v)
    #         sleep(0.2)
    
    # pwm0.set(1500)
    # sleep(2)

    # servo.value = 1
    # servo.min()
    # sleep(5)
    # print('min: ', servo.value)
    # servo.mid()
    # sleep(5)
    # print('mid: ', servo.value)
    # servo.max()
    # sleep(5)
    # print('max: ', servo.value)
    # servo.value = 0.13
    # sleep(5)
    # print('value: ', servo.value)
    while True:
        # print(servo.value)
        sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

# servo.close()
# servo = None
# pwm0 = None
led.close()
print('Done!')
