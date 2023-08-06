
from pyxperiment.controller import VisaInstrument

class AgilentN9000A(VisaInstrument):
    """Анализатор спектра Agilent N9000A
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('CONF:SAN:NDEF')

    @staticmethod
    def driver_name():
        return 'Agilent/Keysight N9000A'

    @property
    def channels_num(self):
        return self.query('SWE:POIN?')

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r','\n']}).split(',')
        return value[0] + ' ' + value[1] + ' SA'

    def get_value(self):
        return self.query('READ:SAN?')