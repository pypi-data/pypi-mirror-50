"""
    data_format/stm_data_format.py: Implements the data storaging for stm scans

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

from .text_data_format import TextDataWriter

class StmTextDataWriter(TextDataWriter):
    """A class for formatted data output into text files"""

    def after_sweep(self, num, data_context):
        if num == 1:
            self.save_internal(data_context)
            self.start_new_file()

    def save_file(self, name, data):
        file_name = self.get_filename().replace('.dat', name + '.dat')
        with open(file_name, "w") as text_file:
            for row in data:
                print(*row, file=text_file)

    def save_internal(self, data_context):
        """
        Save data to file
        """
        curves = data_context.all_data.get_data()
        #curve_len = len(curves[0].read_data()[0])
        # Forward current
        rd_data = []
        for curve in curves[::2]:
            rd_data.append(curve.read_data()[0])
        self.save_file('_c_fw', rd_data)
        rd_data = []
        for curve in curves[::2]:
            rd_data.append(curve.read_data()[1])
        self.save_file('_h_fw', rd_data)
        time_data = [curve.time_markers() for curve in curves[::2]]
        self.save_file('_time_fw', time_data)
        rd_data = []
        for curve in curves[1::2]:
            rd_data.append(curve.read_data()[0])
        self.save_file('_c_bw', rd_data)
        rd_data = []
        for curve in curves[1::2]:
            rd_data.append(curve.read_data()[1])
        self.save_file('_h_bw', rd_data)
        time_data = [curve.time_markers() for curve in curves[1::2]]
        self.save_file('_time_bw', time_data)
