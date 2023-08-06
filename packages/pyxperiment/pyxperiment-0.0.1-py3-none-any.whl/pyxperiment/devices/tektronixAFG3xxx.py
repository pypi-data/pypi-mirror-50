from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import BooleanDeviceOption, ValueDeviceOption

class TektronixAFG3xxx(VisaInstrument):
    """
    Support for Tektronix AFG3000 series waveform generator
    """

    @staticmethod
    def driver_name():
        return 'Tektronix AFG3000 Generator'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self._idn = self.query_id().split(',')
        if self.get_mode() != 'DC':
            self.set_mode('DC')
        self.set_options([
            ValueDeviceOption('Impedance', 'Ohm', self.get_impedance, self.set_impedance),
            BooleanDeviceOption('Output', self.get_output, self.set_output),
            self.offset
        ])

    def device_name(self):
        return self._idn[0] + ' ' + self._idn[1] + ' Generator'

    def get_impedance(self):
        return self.query('OUTP:IMP?')

    def set_impedance(self, value):
        self.write('OUTP:IMP ' + str(value))

    def get_output(self):
        return self._query_boolean('OUTP?')

    def set_output(self, value):
        self._write_boolean('OUTP', value)

    def set_mode(self, mode):
        self.write('FUNC ' + mode)

    def get_mode(self):
        return self.query('FUNC?')

    def get_offset(self):
        return self.query('VOLT:OFFS?')

    def set_offset(self, value):
        self.write('VOLT:OFFS ' + str(value) + 'V')

    offset = ValueDeviceOption('Offset', 'V', get_offset, set_offset)
    