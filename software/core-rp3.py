import sys
import time
import RPi.GPIO as GPIO
from loadcell import LoadCell


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

        # TODO do all weight and percentage calculations here

        print('FL: ' + str(self.load_cells['FL']),
              'FR: ' + str(self.load_cells['FL']),
              'RL: ' + str(self.load_cells['FL']),
              'RR: ' + str(self.load_cells['FL']))

    def _get_weights(self):
        for k, v in self.load_cells.items():
            v.get_measure()


if __name__ == '__main__':
    sc = ScaleControl()

    while True:

        try:
            sc.update()
            time.sleep(.2)

        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            sys.exit()



