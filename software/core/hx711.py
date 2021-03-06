#!/usr/bin/python3
import statistics
import time
import RPi.GPIO as GPIO


class HX711:
    def __init__(self, dout=5, pd_sck=6, gain=128, bits_to_read=24):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        # The value returned by the hx711 that corresponds to your
        # reference unit AFTER dividing by the SCALE.
        self.REFERENCE_UNIT = 1

        self.GAIN = 0
        self.OFFSET = 1
        self.lastVal = 0
        self.bits_to_read = bits_to_read
        self.twos_complement_threshold = 1 << (bits_to_read - 1)
        self.twos_complement_offset = -(1 << bits_to_read)
        self.set_gain(gain)
        self.read()

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def set_gain(self, gain):
        """
        Choose the channel and set the gain. Note that a gain of 128 or 64 will select channel A, a gain of 32 will
        select channel B. Only one channel may be read at a time.
        :param gain:
        :return:
        """
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def wait_for_ready(self):
        while not self.is_ready():
            pass

    def correct_twos_complement(self, unsigned_value):
        if unsigned_value >= self.twos_complement_threshold:
            return unsigned_value + self.twos_complement_offset
        else:
            return unsigned_value

    def read(self):
        self.wait_for_ready()

        unsigned_value = 0
        for i in range(0, self.bits_to_read):
            GPIO.output(self.PD_SCK, True)
            bit_value = GPIO.input(self.DOUT)
            GPIO.output(self.PD_SCK, False)
            unsigned_value <<= 1
            unsigned_value = unsigned_value | bit_value

        # set channel and gain factor for next reading
        for i in range(self.GAIN):
            GPIO.output(self.PD_SCK, True)
            GPIO.output(self.PD_SCK, False)

        return self.correct_twos_complement(unsigned_value)

    def get_value(self):
        return self.read() - self.OFFSET

    def get_weight(self):
        value = self.get_value()
        value /= self.REFERENCE_UNIT
        return value

    def tare(self, times=25):
        reference_unit = self.REFERENCE_UNIT
        self.set_reference_unit(1)

        # remove spikes
        cut = times//5
        values = sorted([self.read() for i in range(times)])[cut:-cut]
        offset = statistics.mean(values)

        self.set_offset(offset)

        self.set_reference_unit(reference_unit)

    def set_offset(self, offset):
        self.OFFSET = offset

    def set_reference_unit(self, reference_unit):
        self.REFERENCE_UNIT = reference_unit

    # HX711 data sheet states that setting the PDA_CLOCK pin on high
    # for a more than 60 microseconds would power off the chip.
    # I used 100 microseconds, just in case.
    # I've found it is good practice to reset the hx711 if it wasn't used
    # for more than a few seconds.
    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)
        time.sleep(0.0001)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)
        time.sleep(0.0001)

    def reset(self):
        self.power_down()
        self.power_up()
