import random
import time

from pyxperiment.controller.device_options import ValueDeviceOption
from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.instrument import Instrument

class TestDevice(VisaInstrument):

    def __init__(self, rm, resource):
        Instrument.__init__(self, '')
        self.last_value = 0
        self.last_value2 = 0
        self.options = []

    @staticmethod
    def driver_name():
        return 'Test'

    def device_name(self):
        return 'Test device'

    @property
    def location(self):
        return ''

    def get_value(self):
        return str(self.last_value)

    def get_value2(self):
        self.last_value2 += 0.1
        #time.sleep(0.01)
        return str(self.last_value2)

    def set_value(self, value):
        self.last_value = value

    def get_random(self):
        #time.sleep(0.1)
        return str(random.triangular(-10, 10))

    value = ValueDeviceOption('Test', 'V', get_value, set_value)
    value2 = ValueDeviceOption('Test up', 'V', get_value2)
    rand = ValueDeviceOption('Random', 'V', get_random)
