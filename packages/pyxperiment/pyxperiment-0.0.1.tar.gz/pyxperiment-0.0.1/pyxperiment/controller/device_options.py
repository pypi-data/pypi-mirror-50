"""
    controller/device_options.py: The base classes for options - device
    specific data entities

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

from abc import ABCMeta, abstractmethod
from copy import copy
from .validation import EmptyValidator

class DeviceOption(metaclass=ABCMeta):
    """
    Device option, that generally can not be used for a sweep,
    only in editor, abstract base class
    """

    def __init__(self, name, fget=None, fset=None, immutable=False):
        self._name = name
        self._fget = fget
        self._fset = fset
        self.device = None
        self._immutable = immutable

    @property
    def name(self):
        """The name of the current option"""
        return self._name

    @abstractmethod
    def get_value(self):
        """
        Retrieve the option value
        """

    @abstractmethod
    def set_value(self, value):
        """
        Set the option value
        """

    def is_immutable(self):
        """
        Get if the option is permanent and can't change
        """
        return self._immutable

    def is_readable(self):
        """Readable option can be only read"""
        return self._fset is None

    def is_writable(self):
        """Writable option can be set"""
        return self._fset is not None

    def with_instance(self, device):
        """Used to instantiate options when a specific device is created"""
        ret = copy(self)
        ret.device = device
        return ret

    def description(self):
        """
        Get the description tuple array
        """
        ret = self.device.description()
        ret.append(('Property', self._name))
        return ret

    def driver_name(self):
        return self.device.driver_name()

    def device_name(self):
        return self.device.device_name()

    def is_sweep_based(self):
        return False

    @property
    def location(self):
        return self.device.location

    def to_remote(self):
        self.device.to_remote()

    def to_local(self):
        self.device.to_local()

class ListDeviceOption(DeviceOption):
    """Device option, that accepts only values, present
    in a special list
    TODO: must implement all checks of elements """

    def __init__(self, name, values_list, fget=None, fset=None):
        super().__init__(name, fget, fset)
        self._values_list = values_list

    def values_list(self):
        """return the list of the valid values"""
        return self._values_list

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        self._fset(value)

class SmartListDeviceOption(ListDeviceOption):
    """
    List device option that does data conversion internally
    """

    def __init__(self, name, values_list, get_cmd, set_cmd):
        super().__init__(name, values_list, get_cmd, set_cmd)

    def get_value(self):
        value = self.device.query(self._fget)
        return self._values_list[int(value)]

    def set_value(self, value):
        if value in self._values_list:
            self.device.write(self._fset + str(self._values_list.index(value)))
        else:
            raise ValueError('Invalid value: ' + value)

class BooleanDeviceOption(DeviceOption):
    """Device option, that accepts only two values: true
    or false"""

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        self._fset(value)

class ValueDeviceOption(DeviceOption):
    """
    Device option, that repesents a numerical value of physical
    quantity (a valid x for a sweep).
    """

    def __init__(self, name, phys_q, fget=None, fset=None, channels=1, validator=EmptyValidator, immutable=False):
        super().__init__(name, fget, fset, immutable)
        self._phys_q = phys_q
        self._validator = validator
        self._channels = channels

    def phys_quantity(self):
        """Get physical quantity (if applicable)"""
        return self._phys_q

    def get_value(self):
        if self.device is None:
            return self._fget()
        return self._fget(self.device)

    def set_value(self, value):
        if self.device is None:
            self._fset(value)
        else:
            self._fset(self.device, value)

    def check_values(self, values):
        """Check the ability to set all the values present in collection"""
        return self._validator.check_values(values)

    @property
    def channels_num(self):
        """Return the length of the output data vector"""
        return self._channels

class StateDeviceOption(DeviceOption):
    """
    Device option, that can only be read, and represents
    certain state (string)
    """

    def __init__(self, name, fget):
        super().__init__(name, fget, None)

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        raise NotImplementedError('set_value not valid for StateDeviceOption')

class ActionDeviceOption(DeviceOption):
    """
    Device option, that can only be set (activated), and
    represents certain action/state transition
    """

    def __init__(self, name, fset):
        super().__init__(name, None, fset)

    def get_value(self):
        raise NotImplementedError('get_value not valid for ActionDeviceOption')

    def set_value(self, value=None):
        self._fset()
