import statistics
import random


class LoadCell:
    def __init__(self, dout_pin, pd_sck_pin, driver=None, samples=20, spikes=4, sleep=0.1, simulate=False):


        self.simulate = simulate

        self.ref_weight = 0
        self.units = None
        self.weight = 0
        self.samples = samples
        self.spikes = spikes
        self.sleep = sleep
        self.history = []

        # HOW TO CALCULATE THE REFFERENCE UNIT
        # To set the reference unit. Put 1kg on your sensor or anything you have and know exactly how much it weighs.
        # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
        # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
        # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.

        if not self.simulate:
            from core.hx711 import HX711
            self.driver = driver or HX711(dout_pin, pd_sck_pin)
            self.driver.set_reference_unit(92)

            self.driver.reset()
            self.driver.tare()

    # def get_weight(self, no_of_reads=3):
    #     self.weight = self.driver.get_weight(no_of_reads)

    def __str__(self):
        return str(self.weight) + ' Lbs'

    def new_measure(self):
        if not self.simulate:
            value = self.driver.get_weight()
        else:
            value = random.uniform(455, 450)
        self.history.append(value)

    def get_measure(self):
        """Useful for continuous measurements."""
        self.new_measure()
        # cut to old values
        self.history = self.history[-self.samples:]

        avg = statistics.mean(self.history)
        deltas = sorted([abs(i - avg) for i in self.history])

        if len(deltas) < self.spikes:
            max_permitted_delta = deltas[-1]
        else:
            max_permitted_delta = deltas[-self.spikes]

        valid_values = list(filter(
            lambda val: abs(val - avg) <= max_permitted_delta, self.history
        ))

        avg = statistics.mean(valid_values)

        self.weight = avg  # FIXME organize this class to better manage it's own data, probably doesn't need to return
        return avg

    def get_weight(self, samples=None):
        """Get weight for once in a while. It clears history first."""
        self.history = []

        [self.new_measure() for i in range(samples or self.samples)]

        return self.get_measure()

    def tare(self, times=25):
        self.driver.tare(times)

    def set_offset(self, offset):
        self.driver.set_offset(offset)

    def set_reference_unit(self, reference_unit):
        self.driver.set_reference_unit(reference_unit)

    def power_down(self):
        self.driver.power_down()

    def power_up(self):
        self.driver.power_up()

