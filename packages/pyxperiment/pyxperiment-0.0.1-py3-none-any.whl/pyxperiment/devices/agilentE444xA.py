import re
from pyxperiment.controller import VisaInstrument

class AgilentE444xA(VisaInstrument):
    """Agilent E444xA spectrum analyzer"""

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.write('FORM ASC')
        self.x_data = []

    @staticmethod
    def driver_name():
        return 'Agilent E444xA'

    @property
    def channels_num(self):
        return 1

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + value[1]

    def __marker_pos_to_x(self, pos):
        self.write('CALC:MARK1:X:POS ' + str(pos))
        return self.query('CALC:MARK1:X?')

    def __get_freq_data(self):
        self.write("MMEM:DEL 'C:/RES.CSV'")
        self.write(":MMEM:STOR:TRAC TRACE1,'C:/RES.CSV'")
        data = self.query("MMEM:DATA? 'C:/RES.CSV'")
        mtc = re.match("#([0-9])([0-9]+) .*", data)
        size = int(mtc.group(2))+2-len(data)+int(mtc.group(1))
        read = []
        while len(read) < size:
            read += self.inst.read_raw()
        data = "".join(map(chr, read))
        return [line.split(',')[0] for line in data.split('\n')[14:-2]]

    def __wait_until_sweep_finished(self):
        """Delay until the sweep is complete"""
        cond = self.query('STAT:OPER:COND?')
        while int(cond) & (1<<3):
            cond = self.query('STAT:OPER:COND?')

    def to_remote(self):
        self.write('INIT:CONT OFF')
        self.write('INIT:IMM')
        self.__wait_until_sweep_finished()
        self.x_data = self.__get_freq_data()

    def to_local(self):
        self.write('INIT:CONT ON')

    def get_sweep_x(self):
        return self.x_data

    def get_sweep(self):
        self.write('INIT:IMM')
        self.__wait_until_sweep_finished()
        data = self.query('TRAC? TRACE1').split(',')
        return data
