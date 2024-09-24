from os import system, path
from time import sleep
from gpiozero import GPIOZeroError

class PWMBadPin(GPIOZeroError, ValueError):
    "Error rased when an invalid pin is given to an :class:`PWMPin`"

class PWMPin:
    def __init__(self, pin: int):
        valid_pins = [12, 13, 14, 15, 18, 19]
        valid_afunc = ['a0', 'a0', 'a0', 'a0', 'a3', 'a3']
        valid_pwmx = [0, 1, 2, 3, 2, 3]

        self.is_enabled = False
        self.onTime_us = 0
        if pin in valid_pins:
            idx = valid_pins.index(pin)
            self.pin = pin
            self.afunc = valid_afunc[idx]
            self.pwmx = valid_pwmx[idx]
            self._set_pinctrl(self.afunc)
            if not path.exists("/sys/class/pwm/pwmchip2/pwm{}".format(self.pwmx)):
                system("echo {} > /sys/class/pwm/pwmchip2/export".format(self.pwmx))
            sleep(0.2)
            system("echo {} > /sys/class/pwm/pwmchip2/pwm{}/period".format(20_000_000, self.pwmx))
            sleep(0.1)
            self.enable(False)
            self.file_duty_cycle = open("/sys/class/pwm/pwmchip2/pwm{}/duty_cycle".format(self.pwmx), "w")
            if self.file_duty_cycle.closed:
                raise IOError("Unable to create pwm{} file".format(self.pwmx))
        else:
            self.pin = None
            raise PWMBadPin('pin must be one of: 12, 13, 14, 15, 18 or 19')

    def enable(self, enabled: bool):
        if self.pin is not None:
            self.is_enabled = enabled
            system("echo {} > /sys/class/pwm/pwmchip2/pwm{}/enable".format(int(enabled), self.pwmx))
    
    def set(self, onTime_us: int):
        if self.pin is not None:
            if not self.is_enabled:
                self.enable(True)
            self.onTime_us = onTime_us
            self.file_duty_cycle.write("{}".format(onTime_us * 1000))
            self.file_duty_cycle.flush()

    def _set_pinctrl(self, value: str):
        system("/usr/bin/pinctrl set {} {}".format(self.pin, value))

    def __del__(self):
        if self.pin is not None:
            system("echo {} > /sys/class/pwm/pwmchip2/unexport".format(self.pwmx))
            self._set_pinctrl("no")
            if not self.file_duty_cycle.closed:
                self.file_duty_cycle.close()
