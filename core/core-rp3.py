from core.hx711 import HX711
import time


class LoadCell:
    def __init__(self, dout_pin, pd_sck_pin):
        self.driver = HX711(dout_pin, pd_sck_pin)

        self.ref_weight = 0
        self.units = None
        self.weight = 0

        # I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
        # Still need to figure out why does it change.
        # If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
        # There is some code below to debug and log the order of the bits and the bytes.
        # The first parameter is the order in which the bytes are used to build the "long" value.
        # The second paramter is the order of the bits inside each byte.
        # According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
        self.driver.set_reading_format("LSB", "MSB")

        # HOW TO CALCULATE THE REFFERENCE UNIT
        # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
        # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
        # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
        # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
        self.driver.set_reference_unit(92)

        self.driver.reset()
        self.driver.tare()

    def get_weight(self, no_of_reads=3):
        self.weight = self.driver.get_weight(no_of_reads)

    def power_down(self):
        self.driver.power_down()

    def power_up(self):
        self.driver.power_up()


class ScaleControl:
    def __init__(self):
        self.load_cells = {'FL': LoadCell(4, 5), 'FR': LoadCell(4, 5), 'RL': LoadCell(4, 5), 'RR': LoadCell(4, 5)}

        self.total_weight = 0

        # front data
        self.F_weight = 0
        self.F_percent = 0

        # rear data
        self.R_weight = 0
        self.R_percent = 0

        # left data
        self.L_weight = 0
        self.L_percent = 0

        # right data
        self.R_weight = 0
        self.R_percent = 0

        # front left to rear right cross data
        self.FL_RR_weight = 0
        self.FL_RR_percent = 0

        # front right to rear left cross data
        self.FR_RL_weight = 0
        self.FR_RL_percent = 0

    def update(self):
        self._get_weights()
        print(self.load_cells['FL'].weight)

    def _get_weights(self):
        for k, v in self.load_cells.items():
            v.get_weight()

if __name__ == '__main__':
    sc = ScaleControl()

    while True:
        sc.update()
        time.sleep(1)



