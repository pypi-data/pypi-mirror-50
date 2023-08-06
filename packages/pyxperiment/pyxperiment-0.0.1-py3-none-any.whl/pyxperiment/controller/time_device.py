"""Module defines special device class, used for time sweeps"""

from .instrument import Instrument
from .device_options import ValueDeviceOption

class TimeDevice(Instrument):
    """ Special device class, used for time sweeps"""

    def __init__(self):
        super().__init__('')
        self.value = 0

    @staticmethod
    def driver_name():
        return 'Time'

    def device_name(self):
        return 'Time'

    @property
    def location(self):
        return ''

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    @property
    def channels_num(self):
        return 0

    def description(self):
        ret = []
        ret.insert(0, ('Name', 'Time sweep'))
        return ret

    time = ValueDeviceOption('Time', 's', get_value, set_value)
