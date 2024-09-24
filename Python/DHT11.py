from threading import RLock
from gpiozero import GPIOZeroError, Device, InputDevice, OutputDevice
from time import sleep

class DHT11Result:
    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == DHT11Result.ERR_NO_ERROR


class DHT11Device(Device):
    def __init__(self, pin, *, pin_factory=None):
        self._data_io_pin = pin
        self.data_io = None
        super().__init__(pin_factory=pin_factory)
        try:
            self.lock = RLock()
            self.data_io = OutputDevice(pin=pin, pin_factory=pin_factory)
        except:
            self.close()
            raise
    
    def close(self):
        super().close()
        if getattr(self, 'lock', None):
            with self.lock:
                if self.data_io is not None:
                    self.data_io.close()
                self.data_io = None
        self.lock = None

    def read(self):
        self.data_io.on() # send initial high
        sleep(0.05)
        self.data_io.off() # pull down to low
        sleep(0.02)
        
        self._set_data_in() # change to input using pull up
        data = self._collect_input() # collect data into an array
        pull_up_lengths = self._parse_data_pull_up_lengths(data) # parse lengths of all data pull up periods

        # if bit count mismatch, return error (4 byte data + 1 byte checksum)
        if len(pull_up_lengths) != 40:
            return self._make_result(DHT11Result.ERR_MISSING_DATA)

        # calculate bits from lengths of the pull up periods
        bits = self._calculate_bits(pull_up_lengths)

        # we have the bits, calculate bytes
        the_bytes = self._bits_to_bytes(bits)

        # calculate checksum and check
        # checksum = self._calculate_checksum(the_bytes)
        # if the_bytes[4] != checksum:
        #     return self._make_result(DHT11Result.ERR_CRC)
 
        # ok, we have valid data

        # The meaning of the return sensor values
        # the_bytes[0]: humidity int
        # the_bytes[1]: humidity decimal
        # the_bytes[2]: temperature int
        # the_bytes[3]: temperature decimal

        temperature = the_bytes[2] + float(the_bytes[3]) / 10
        humidity = the_bytes[0] + float(the_bytes[1]) / 10

        return self._make_result(temperature=temperature, humidity=humidity)

    def _make_result(self, error = 0, temperature = 0, humidity = 0):
        self._set_data_out()
        return DHT11Result(error, temperature, humidity)

    def _collect_input(self):
        # collect the data while unchanged found
        unchanged_count = 0

        # this is used to determine where is the end of the data
        max_unchanged_count = 100

        last = -1
        data = []
        while True:
            current = int(self.data_io.is_active)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break
        
        return data

    def _parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5

        state = STATE_INIT_PULL_DOWN

        lengths = [] # will contain the lengths of data pull up periods
        current_length = 0 # will contain the length of the previous period

        for i in range(len(data)):

            current = data[i]
            current_length += 1

            if state == STATE_INIT_PULL_DOWN:
                if current == 0:
                    # ok, we got the initial pull down
                    state = STATE_INIT_PULL_UP
                continue
            if state == STATE_INIT_PULL_UP:
                if current == 1:
                    # ok, we got the initial pull up
                    state = STATE_DATA_FIRST_PULL_DOWN
                continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == 0:
                    # we have the initial pull down, the next will be the data pull up
                    state = STATE_DATA_PULL_UP
                continue
            if state == STATE_DATA_PULL_UP:
                if current == 1:
                    # data pulled up, the length of this pull up will determine whether it is 0 or 1
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                continue
            if state == STATE_DATA_PULL_DOWN:
                if current == 0:
                    # pulled down, we store the length of the previous pull up period
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                continue

        return lengths

    def _calculate_bits(self, pull_up_lengths):
        # find shortest and longest period
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        # use the halfway to determine whether the period it is long or short
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []

        for i in range(0, len(pull_up_lengths)):
            bit = False
            if pull_up_lengths[i] > halfway:
                bit = True
            bits.append(bit)

        return bits

    def _bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0

        return the_bytes

    def _calculate_checksum(self, the_bytes):
        return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3] & 255

    def _set_data_in(self):
        if self.data_io is not None:
            self.data_io.close()
            self.data_io = None
        self.data_io = InputDevice(pin=self._data_io_pin, pull_up=True, pin_factory=self.pin_factory)

    def _set_data_out(self):
        if self.data_io is not None:
            self.data_io.close()
            self.data_io = None
        self.data_io = OutputDevice(pin=self._data_io_pin, pin_factory=self.pin_factory)
