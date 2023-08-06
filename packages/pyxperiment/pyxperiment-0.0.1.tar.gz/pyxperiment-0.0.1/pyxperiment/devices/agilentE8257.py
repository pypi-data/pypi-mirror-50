
from pyxperiment.controller import VisaInstrument

class AgilentE8257(VisaInstrument):
    """
    Support for Agilent E8257 Generator
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)

    @staticmethod
    def driver_name():
        return 'Agilent/Keysight E8257'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r','\n']}).split(',')
        return value[0] + ' ' + value[1] + ' signal generator'

    def get_value(self):
        return self.query('FREQ:CW?')

    def set_value(self, value):
        self.write('FREQ:CW ' + str(value))
        