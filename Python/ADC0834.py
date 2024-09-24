from threading import RLock
from gpiozero import GPIOZeroError, Device, InputDevice, OutputDevice
from time import sleep

class ADC0834BadChannel(GPIOZeroError, ValueError):
    "Error rased when an invalid channel is given to an :class:`ADC0834Device`"

class ADC0834BadFrequency(GPIOZeroError, ValueError):
    "Error rased when an invalid frequency is given to an :class:`ADC0834Device`"

class ADC0834Device(Device):
    """
    Extends :class:`Device`. Represents an ADC0834

    :type select_pin: int or str
    :param select_pin:
        The GPIO pin that is used for the chip select. See :ref:`pin-numbering` for valid pin numbers.
    
    :type clock_pin: int or str
    :param clock_pin:
        The GPIO pin that is used as the clock. See :ref:`pin-numbering` for valid pin numbers.

    :type data_io_pin: int or str
    :param data_io_pin:
        The GPIO pin that is used as the data and output. See :ref:`pin-numbering` for valid pin numbers.
    
    :type channel: int
    :param channel:
        The default channel to read data from when using the :ref:`value` property. Valid values are between 0 and 3. Default is 0.
    
    :type frequency: int
    :param frequency:
        The frequency of the clock signal in Hz. Valid values are between 10-400kHz (10,0000 - 400,000). Default is 250,0000.
    """
    def __init__(self, select_pin, clock_pin, data_io_pin, channel: int = 0, frequency: int = 250_000, *, pin_factory=None):
        if not 0 <= channel < 4:
            raise ADC0834BadChannel('channel must be between 0 and 3')
        self._channel = channel
        if not 10_000 <= frequency < 400_000:
            raise ADC0834BadFrequency('frequency must be between 10,000 and 400,000')
        self._frequency = frequency
        self._data_io_pin = data_io_pin
        self.lock = None
        self.chip_select = None
        self.clock = None
        self.data_io = None
        super().__init__(pin_factory=pin_factory)
        try:
            self.lock = RLock()
            self.chip_select = OutputDevice(select_pin, pin_factory=pin_factory)
            self.clock = OutputDevice(clock_pin, pin_factory=pin_factory)
            self.data_io = OutputDevice(data_io_pin, pin_factory=pin_factory)
        except:
            self.close()
            raise

    def close(self):
        super().close()
        if getattr(self, 'lock', None):
            with self.lock:
                self.data_io.close()
                self.data_io = None
                self.chip_select.close()
                self.chip_select = None
                self.clock.close()
                self.clock = None
        self.lock = None

    @property
    def channel(self):
        return self._channel

    @property
    def frequency(self):
        return self._frequency

    @property
    def value(self):
        with self.lock:
            return self._readValue(channel=self.channel)

    def valueAt(self, channel: int = 0):
        if not 0 <= channel < 4:
            raise ADC0834BadChannel('channel must be between 0 and 3')
        with self.lock:
            return self._readValue(channel=channel)

    @property
    def closed(self):
        return self.lock is None
    
    def _readValue(self, channel: int):
        self.chip_select.value = 0
        self.data_io.value = 0

        # Start bit
        self._set_clock_low()
        self.data_io.value = 1
        self._set_clock_high()

        # SGL/DIF
        self._set_clock_low()
        self.data_io.value = 1
        self._set_clock_high()

        # ODD/SIGN
        self._set_clock_low()
        self.data_io.value = channel % 2
        self._set_clock_high()

        # SELECT1
        self._set_clock_low()
        self.data_io.value = int(channel > 1)
        self._set_clock_high()

        # Allow the MUX to settle for 1/2 clock cycle
        self._set_clock_low()

        # Switch to data in
        self._set_data_in()

        # Read the data from MSB to LSB
        value1 = 0
        for i in range(0, 8):
            self._set_clock_high()
            self._set_clock_low()
            value1 = value1 << 1
            value1 = value1 | self.data_io.value

        value2 = 0
        for i in range(0, 8):
            bit = self.data_io.value << i
            value2 = value2 | bit
            self._set_clock_high()
            self._set_clock_low()

        # Set chipSelect to high to clear all internal registers
        self.chip_select.value = 1

        # Done reading, switch back to data out
        self._set_data_out()

        return value1 if value1 == value2 else 0

    def _set_clock_high(self):
        self.clock.value = 1
        self._tick()
    
    def _set_clock_low(self):
        self.clock.value = 0
        self._tick()

    def _tick(self):
        sleep(1 / self.frequency / 2)

    def _set_data_in(self):
        if self.data_io is not None:
            self.data_io.close()
            self.data_io = None
        self.data_io = InputDevice(pin=self._data_io_pin, pin_factory=self.pin_factory)

    def _set_data_out(self):
        if self.data_io is not None:
            self.data_io.close()
            self.data_io = None
        self.data_io = OutputDevice(pin=self._data_io_pin, pin_factory=self.pin_factory)
