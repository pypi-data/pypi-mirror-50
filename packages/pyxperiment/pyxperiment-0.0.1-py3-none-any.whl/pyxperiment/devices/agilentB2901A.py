from decimal import Decimal

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ListDeviceOption, BooleanDeviceOption, ValueDeviceOption, StateDeviceOption
)

class AgilentB2901ASMU(VisaInstrument):
    """Support for Keysight B2901A SMU"""

    def __init__(self,rm,resource):
        super().__init__(rm,resource)
        self.write('*CLS')
        self.idn = self.query_id().split(',')

        self.set_options([
            BooleanDeviceOption('Output on', self.get_output, self.set_output),
            ListDeviceOption('Function', list(self.function_values.keys()), self.get_function, self.set_function),
            ValueDeviceOption('Voltage', 'V', self.get_sour_volt, self.set_sour_volt),
            ValueDeviceOption('Current', 'A', self.get_sour_curr, self.set_sour_curr),
            BooleanDeviceOption('Voltage range auto', self.get_volt_range_auto, self.set_volt_range_auto),
            ListDeviceOption('Voltage range, V', self.volt_range_values, self.get_volt_range, self.set_volt_range),
            BooleanDeviceOption('Current range auto', self.get_curr_range_auto, self.set_curr_range_auto),
            ListDeviceOption('Current range, A', self.curr_range_values, self.get_curr_range, self.set_curr_range),
            ValueDeviceOption('Voltage limit', 'V', self.get_volt_limit, self.set_volt_limit),
            ValueDeviceOption('Current limit', 'A', self.get_curr_limit, self.set_curr_limit),
            StateDeviceOption('Voltage readout, V', self.get_meas_volt),
            StateDeviceOption('Current readout, A', self.get_meas_curr),
        ])

    @staticmethod
    def driver_name():
        return 'Keysight B2901A source/measure unit'

    def query(self, cmd):
        return super().query(cmd).translate({ord(c): None for c in ['\r', '\n']})

    def device_name(self):
        return self.idn[0] + ' ' + self.idn[1] + ' SMU'

    def get_value(self):
        func = self.get_function()
        if func == self.VOLT_NAME:
            return self.get_sour_volt()
        elif func == self.CURR_NAME:
            return self.get_sour_curr()
        else:
            raise ValueError('Invalid function: ' + func)

    def set_value(self, value):
        func = self.get_function()
        if func == self.VOLT_NAME:
            self.set_sour_volt(value)
        elif func == self.CURR_NAME:
            self.set_sour_curr(value)
        else:
            raise ValueError('Invalid function: ' + func)

    #def check_values(self, values):
    #    """Check values range"""
    #    current_range = self.get_range()[1]
    #    values = [x for x in values if abs(Decimal(x)) > current_range[1] or divmod(Decimal(x),current_range[2])[1] > 0]
    #    return len(values) == 0
        
    def get_output(self):
        return self._query_boolean(':OUTP?')

    def set_output(self, value):
        self._write_boolean(':OUTP ', value, 'ON', 'OFF')

    VOLT_NAME = 'volt'
    CURR_NAME = 'curr'

    function_values = {
        VOLT_NAME:'VOLT',
        CURR_NAME:'CURR',
        }

    def get_function(self):
        func = self.query(':SOUR:FUNC:MODE?')
        for name,fn in self.function_values.items():
            if fn == func:
                return name
        raise ValueError('Invalid function: ' + func)

    def set_function(self, value):
        try:                                                                                                      
            cmd = self.function_values[value]
        except KeyError:
            raise ValueError('Invalid function: ' + value)
        self.write(':SOUR:FUNC:MODE ' + cmd)

    def get_sour_volt(self):
        return self.query(':SOUR:VOLT?')

    def set_sour_volt(self, value):
        self.write(':SOUR:VOLT ' + str(value))

    def get_sour_curr(self):
        return self.query(':SOUR:CURR?')

    def set_sour_curr(self, value):
        self.write(':SOUR:CURR ' + str(value))

    def get_volt_limit(self):
        return self.query(':SENS:VOLT:PROT?')

    def set_volt_limit(self, value):
        self.write(':SENS:VOLT:PROT ' + str(value))

    def get_curr_limit(self):
        return self.query(':SENS:CURR:PROT?')

    def set_curr_limit(self, value):
        self.write(':SENS:CURR:PROT ' + str(value))

    def get_meas_volt(self):
        return self.query(':MEAS:VOLT?')

    def get_meas_curr(self):
        return self.query(':MEAS:CURR?')

    def get_volt_range_auto(self):
        return self._query_boolean(':SOUR:VOLT:RANG:AUTO?')

    def set_volt_range_auto(self, value):
        self._write_boolean(':SOUR:VOLT:RANG:AUTO ', value, 'ON', 'OFF')

    def get_curr_range_auto(self):
        return self._query_boolean(':SOUR:CURR:RANG:AUTO?')

    def set_curr_range_auto(self, value):
        self._write_boolean(':SOUR:CURR:RANG:AUTO ', value, 'ON', 'OFF')

    volt_range_values = [
        '200',
        '20',
        '2',
        '0.2'
        ]

    curr_range_values = [
        '3',
        '1.5',
        '1',
        '1E-1',
        '1E-2',
        '1E-3',
        '1E-4',
        '1E-5',
        '1E-6',
        '1E-7'
        ]

    def set_volt_range(self, value):
        if value in self.volt_range_values:
            self.write(':SOUR:VOLT:RANG ' + value)
        else:
            raise ValueError('Invalid range.')

    def get_volt_range(self):
        value = self.query(':SOUR:VOLT:RANG?')
        for range_value in self.volt_range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    def set_curr_range(self, value):
        if value in self.curr_range_values:
            self.write(':SOUR:CURR:RANG ' + value)
        else:
            raise ValueError('Invalid range.')

    def get_curr_range(self):
        value = self.query(':SOUR:CURR:RANG?')
        for range_value in self.curr_range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    #def to_local(self):
    #    """Enable local controls after sweep is over"""
    #    self.write(':TRIG:ALL:SOUR AINT')
