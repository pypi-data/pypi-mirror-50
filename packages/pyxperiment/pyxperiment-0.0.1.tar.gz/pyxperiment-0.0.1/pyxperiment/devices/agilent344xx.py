"""
    devices/agilent344xx.py: Support for Keysight344xx

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import time
from decimal import Decimal
import wx

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ValueDeviceOption, BooleanDeviceOption
)
from pyxperiment.frames.device_config import (
    DeviceConfig, option_to_control
)
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)

class Agilent34xxxDMM(VisaInstrument):
    """
    Support for Keysight344xx
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        self.model = value[1]

    @staticmethod
    def driver_name():
        return 'HP/Agilent/Keysight 34xxx DMM'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' DMM'

    @property
    def channels_num(self):
        return int(self.get_sample_count())

    def set_function(self, unit):
        if unit == 'volt':
            self.write('func:volt:dc')
        elif unit == 'curr':
            self.write('func:curr:dc')
        else:
            raise ValueError('Invalid unit')

    def get_function(self):
        return self.query('func?')

    def set_autorange(self, value):
        self.write('sens:volt:dc:rang:auto ' + ('1' if value else '0'))

    def get_autorange(self):
        value = int(self.query('volt:dc:rang:auto?'))
        if value == 1:
            return True
        elif value == 0:
            return False
        raise ValueError('Unknown autorange value  "' + value + '"')  

    range_values = [
        '1000',
        '100',
        '10',
        '1',
        '0.1'
        ]

    def set_range(self, value):
        if value in self.range_values:
            self.write('volt:rang ' + value)
        else:
            raise ValueError('Invalid range.')

    def get_range(self):
        value = self.query('volt:rang?')
        for range_value in self.range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    nplc_values = [
        '0.02',
        '0.2',
        '1',
        '10',
        '100'
        ]

    def set_nplc(self, value):
        if value in self.nplc_values:
            self.write('volt:nplc ' + value)
        else:
            raise ValueError('Invalid NPLC.')

    def get_nplc(self):
        value = self.query('volt:nplc?')
        for nplc_value in self.nplc_values:
            if Decimal(nplc_value) == Decimal(value):
                return nplc_value
        raise ValueError('Unkwown NPLC: ' + value)

    def get_resolution(self):
        return self.query('volt:dc:res?')

    def set_resolution(self, value):
        self.write('volt:dc:res ' + value)

    def get_value(self):
        self.init_get_value()
        return self.end_get_value()

    def init_get_value(self):
        self.write('read?')

    def end_get_value(self):
        value = self.read().translate({ord(c): None for c in ['\r', '\n']})
        return value.split(',') if (',' in value) else value

    def set_autozero(self, value):
        cmd = 'sens:volt:dc:zero:auto ' if self.model != '34401A' else 'zero:auto '
        self._write_boolean(cmd, value)

    def get_autozero(self):
        cmd = 'sens:volt:dc:zero:auto?' if self.model != '34401A' else 'zero:auto?'
        return self._query_boolean(cmd)

    def set_apertureon(self, value):
        self._write_boolean('volt:aper:enab ', value)

    def get_apertureon(self):
        return self._query_boolean('volt:aper:enab?')

    def set_highz(self, value):
        cmd = 'volt:dc:imp:auto ' if self.model != '34401A' else 'inp:imp:auto '
        self._write_boolean(cmd, value)

    def get_highz(self):
        return self._query_boolean('volt:dc:imp:auto?' if self.model != '34401A' else 'inp:imp:auto?')

    def get_sample_count(self):
        return self.query('SAMP:COUN?')

    def set_sample_count(self, value):
        self.write('SAMP:COUN ' + str(value))

    def get_trigger_delay(self):
        return self.query('TRIG:DEL?')

    def set_trigger_delay(self, value):
        self.write('TRIG:DEL ' + str(value))

    #trigger_delay = ValueDeviceOption(
    #    'Trigger delay', None, get_trigger_delay, set_trigger_delay
    #)

    def get_trigger_delay_auto(self):
        return self._query_boolean('TRIG:DEL:AUTO?')

    def set_trigger_delay_auto(self, value):
        self._write_boolean('TRIG:DEL:AUTO ', value)

    trigger_delay_auto = BooleanDeviceOption(
        'Auto trigger delay', get_trigger_delay_auto, set_trigger_delay_auto
    )

    def set_display_state(self, value):
        if self.model == '34461A':
            self._write_boolean('disp ', value, 'on', 'off')
            self.write('disp:text' + (' "Measurement in progress..."' if not value else ':cle'))

    def get_display_state(self):
        return self._query_boolean('disp?')

    def to_remote(self):
        self.set_display_state(False)

    def to_local(self):
        """Enable local controls after sweep is over"""
        if self.model != '34461A':
            import pyvisa
            self.inst.control_ren(pyvisa.constants.VI_GPIB_REN_ADDRESS_GTL)
        else:
            self.write('SYST:LOC')

    def get_config_class(self):
        return Agilent34xxxDMMConfig

class Agilent34xxxDMMConfig(DeviceConfig):

    def _create_controls(self):
        self.controls = []

        self.autorange = wx.CheckBox(self.panel, label='Auto Range')
        self.controls.append(self.autorange)
        self.range = CaptionDropBox(self.panel, 'Range, V', self.device.range_values)
        self.controls.append(self.range)
        self.resolution = CaptionTextPanel(self.panel, 'Resolution, V',show_mod=True)
        self.controls.append(self.resolution)
        self.nplc = CaptionDropBox(self.panel, 'Power cycles', self.device.nplc_values)
        self.controls.append(self.nplc)
        self.autozero = wx.CheckBox(self.panel, label='Auto Zero')
        self.controls.append(self.autozero)
        self.highz = wx.CheckBox(self.panel, label='Auto Impedance')
        self.controls.append(self.highz)
        self.apertureon = wx.CheckBox(self.panel, label='Aperture on')
        self.apertureon.Disable()
        self.controls.append(self.apertureon)
        self.apertureval = CaptionTextPanel(self.panel,'Aperture, ms',show_mod=True)
        self.apertureval.SetEnabled(False)
        self.controls.append(self.apertureval)
        self.display_on = ModifiedCheckBox(self.panel,'Display on')
        self.display_on.SetEnabled(self.device.model == '34461A')
        self.controls.append(self.display_on)
        self.sample_count = CaptionTextPanel(self.panel,'Sample count',show_mod=True)
        self.controls.append(self.sample_count)
        self.trigger_delay_auto = ModifiedCheckBox(self.panel,'Auto trigger delay')
        self.controls.append(self.trigger_delay_auto)
        self.trigger_delay = CaptionTextPanel(self.panel,'Trigger delay',show_mod=True)
        self.controls.append(self.trigger_delay)

        self.value = CaptionTextPanel(self.panel, 'Value, V')
        self.value.SetEnabled(False)
        self.controls.append(self.value)

        self.timeout = CaptionTextPanel(self.panel, 'Timeout, ms')
        self.timeout.SetEnabled(False)
        self.controls.append(self.timeout)

    def _read_settings(self):
        self.nplc.SetValue(self.device.get_nplc())
        self.range.SetValue(self.device.get_range())
        self.resolution.SetValue(str(Decimal(self.device.get_resolution())))
        self.autorange.SetValue(self.device.get_autorange())
        self.range.SetEnabled(not self.autorange.Value)
        self.resolution.SetEnabled(not self.autorange.Value)
        self.autozero.SetValue(self.device.get_autozero())
        self.highz.SetValue(self.device.get_highz())
        self.sample_count.SetValue(self.device.get_sample_count())
        self.trigger_delay_auto.SetValue(self.device.get_trigger_delay_auto())
        self.trigger_delay.SetValue(self.device.get_trigger_delay())
        self.trigger_delay.SetEnabled(not self.trigger_delay_auto.GetValue())
        if self.device.model == '34461A':
            self.display_on.SetValue(self.device.get_display_state())
        #self.aperture.Value = self.device.get_apertureon()

    def _write_settings(self):
        if self.nplc.IsModified():
            self.device.set_nplc(self.nplc.GetValue())
        if self.range.IsModified():
            self.device.set_range(self.range.GetValue())
        if self.resolution.IsModified():
            self.device.set_resolution(self.resolution.GetValue())

        self.device.set_autorange(self.autorange.Value)
        self.device.set_highz(self.highz.GetValue())
        self.device.set_autozero(self.autozero.Value)

        if self.sample_count.IsModified():
            self.device.set_sample_count(self.sample_count.GetValue())
        if self.trigger_delay_auto.IsModified():
            self.device.set_trigger_delay_auto(self.trigger_delay_auto.GetValue())
        if self.trigger_delay.IsModified():
            self.device.set_trigger_delay(self.trigger_delay.GetValue())
        if self.display_on.IsModified():
            self.device.set_display_state(self.display_on.GetValue())

    def on_reload_timer(self, event):
        start_time = time.perf_counter()
        val = self.device.get_value()
        end_time = time.perf_counter()
        self.timeout.SetValue(str(Decimal(end_time - start_time)*Decimal('1000')))
        if not isinstance(val, list):
            self.value.SetValue(val)
        else:
            self.value.SetValue(', '.join(val))
