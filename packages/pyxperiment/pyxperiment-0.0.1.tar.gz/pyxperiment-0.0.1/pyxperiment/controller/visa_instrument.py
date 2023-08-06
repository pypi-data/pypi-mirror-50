"""
    controller/device_factory.py: The factory class is used to construst devices

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

import socket
import select

from .instrument import Instrument

class VisaInstrument(Instrument):
    """
    Класс для описания любых устройств, управляемых программой или
    данные с которых могут быть считаны через VISA
    """
    #pylint: disable=W0223

    def __init__(self, rm, resource):
        super().__init__('')
        self.__rm = rm
        self.inst = self.__rm.open_resource(resource)

    @property
    def location(self):
        """
        Get device VISA address
        """
        with self.lock:
            return self.inst.resource_name

    def reset(self):
        """
        Reset connection
        """
        with self.lock:
            self.inst = self.__rm.open_resource(self.location)

    def read(self):
        """
        Raw read
        """
        with self.lock:
            return self.inst.read()

    def read_stb(self):
        """
        Read status byte
        """
        with self.lock:
            return self.inst.read_stb()

    def write(self, data):
        """
        Raw write
        """
        with self.lock:
            self.inst.write(data)

    def query(self, data):
        """
        Write followed by immediate read
        """
        with self.lock:
            return self.inst.query(data)

    def wait_bit(self, bit, max_tries):
        """
        Waits for certain stb bit to be set
        """
        with self.lock:
            stb = self.inst.read_stb()
            while (not stb & (1 << bit)) and max_tries > 0:
                stb = self.inst.read_stb()
                max_tries -= 1

    def clear_buf(self, bit):
        """
        Clears instrument output buffer based on stb bit
        """
        with self.lock:
            stb = self.inst.read_stb()
            while stb & (1 << bit):
                self.inst.read_raw(1)
                stb = self.inst.read_stb()

    def query_id(self):
        """
        Read the instrument ID string
        """
        return self.query("*IDN?")

    def _query_boolean(self, query):
        value = int(self.query(query))
        if value == 1:
            return True
        elif value == 0:
            return False
        raise ValueError('Bad boolean value: "' + str(value) + '"')

    def _write_boolean(self, cmd, value, true_str='1', false_str='0'):
        self.write(cmd + (true_str if value else false_str))

    def _write_value_from_list(self, function, value, val_list):
        if value in val_list:
            self.write(function + str(val_list.index(value)))
        else:
            raise ValueError('Invalid value: ' + value)

class TcpSocketDevice(VisaInstrument):
    #pylint: disable=W0223
    BUFFER_SIZE = 256
    RECV_TIMEOUT = 1

    def __init__(self, rm, resource):
        Instrument.__init__(self, '')
        self.resource = resource
        addr = resource.split('::')
        self.inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inst.connect((addr[1], int(addr[2])))
        self.inst.setblocking(False)

    @property
    def location(self):
        with self.lock:
            return self.resource

    def reset(self):
        with self.lock:
            self.inst.close()
            addr = self.resource.split('::')
            self.inst.connect((addr[1], int(addr[2])))
            self.inst.setblocking(False)

    def read(self):
        with self.lock:
            ready = select.select([self.inst], [], [], TcpSocketDevice.RECV_TIMEOUT)
            if ready[0]:
                return self.inst.recv(TcpSocketDevice.BUFFER_SIZE).decode().translate({ord(c): None for c in ['\r','\n']})
        raise TimeoutError('The instrument failed to answer within a specified timeout')

    def write(self, data):
        with self.lock:
            self.inst.send((data + '\n').encode())

    def query(self, data):
        with self.lock:
            self.inst.send((data + '\n').encode())
            ready = select.select([self.inst], [], [], TcpSocketDevice.RECV_TIMEOUT)
            if ready[0]:
                return self.inst.recv(TcpSocketDevice.BUFFER_SIZE).decode().translate({ord(c): None for c in ['\r', '\n']})
        raise TimeoutError('The instrument failed to answer within a specified timeout')
