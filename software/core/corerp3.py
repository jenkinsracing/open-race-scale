import sys
import time
from core.loadcell import LoadCell
from core.scaledata import ScaleData


class ScaleControl:
    def __init__(self, interface=None, simulate=False):
        self.interface = interface
        self.load_cells = {'FL': LoadCell(4, 5, simulate=simulate), 'FR': LoadCell(4, 5, simulate=simulate), 'RL': LoadCell(4, 5, simulate=simulate), 'RR': LoadCell(4, 5, simulate=simulate)}
        self.scale_data = {'FL': ScaleData('FL'), 'FR': ScaleData('FR'), 'RL': ScaleData('RL'), 'RR': ScaleData('RR'), 'TOTAL': ScaleData('TOTAL', calculated=True)}

    def update(self):
        self._get_weights()

        # TODO copy the load cell weight the scale data object
        self.scale_data['FL'].weight = self.load_cells['FL'].weight
        self.scale_data['FR'].weight = self.load_cells['FR'].weight
        self.scale_data['RL'].weight = self.load_cells['RL'].weight
        self.scale_data['RR'].weight = self.load_cells['RR'].weight

        # TODO do all weight and percentage calculations here

        self.scale_data['TOTAL'].weight = self.load_cells['FL'].weight + self.load_cells['FR'].weight + self.load_cells['RL'].weight + self.load_cells['RR'].weight

        print('FL: ' + str(self.load_cells['FL']),
              'FR: ' + str(self.load_cells['FR']),
              'RL: ' + str(self.load_cells['RL']),
              'RR: ' + str(self.load_cells['RR']))

    def _get_weights(self):
        for k, v in self.load_cells.items():
            v.get_measure()

    def _send_data(self):
        # TODO finish bluetooth implementation so that scale data can be sent to clients
        if self.interface is not None:
            self.interface.send(str(self.scale_data))


if __name__ == '__main__':
    """
    If the core is run by itself then it is headless and needs to set up a BT server for clients to read, conversely if
    the core is run by the local GUI, then the GUI will access the scale controller directly and BT is not started
    """
    # TODO in future the bluetooth server should always be started, then data can be accessed by a client even if local
    # TODO GUI is running

    import RPi.GPIO as GPIO
    from core.btserver import Bluetooth
    sc = ScaleControl(Bluetooth())

    while True:

        try:
            sc.update()
            time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            sys.exit()
