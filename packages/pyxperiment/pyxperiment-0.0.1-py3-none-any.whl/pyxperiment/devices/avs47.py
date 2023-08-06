from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import ValueDeviceOption

class AVS47ResBridge(VisaInstrument):
    """ AVS47 resistance bridge support"""

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.set_options([
            self.temperature
        ])

    @staticmethod
    def driver_name():
        return 'AVS47 resistance bridge'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    def get_temperature(self):
        self.write('ADC')
        return self.query('RES?').translate({ord(c): None for c in ['\r', '\n']})[5:]

    temperature = ValueDeviceOption('Resistance', 'Ohm', get_temperature)
