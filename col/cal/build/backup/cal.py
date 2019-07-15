from ctypes import(cdll, Structure, POINTER, c_int, c_double,
                   c_char_p, )
import numpy as np
from scipy import signal as sg


class Cal(object):
    """ DocString for Cal"""

    def __init__(self, ):
        #@todo: to be defined.
        self.lib = cdll.LoadLibrary('filter.so')

        self.func_change_stat = self.lib.changeStat
        self.func_change_stat.argtypes = [c_int, c_int]

        self.func_make_filter = self.lib.makeFilter
        self.func_make_filter.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                          np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                          c_int, c_int]

        self.func_run = self.lib.run
        self.func_run.argtypes = [c_char_p, np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'), c_int]

        self.temp_num = np.zeros(700)


    def change_status(self, channel_num):
        """DocString for change_status"""
        #@todo: to be defined.

		#:channel_num: @todo.
        self.channel_num = channel_num
        return self.func_change_stat(channel_num, 0)

    def data_from_tcp(self, data):
        """DocString for data_from_tcp"""
        #@todo: to be defined.

		#:data: @todo.
        return self.funcReadFromTCP(data, len(data))

    def design_filter(self, freq_sample):
        """DocString for design_filter"""
        #@todo: to be defined.
		#:freq_sample: @todo.

        # Comb Filter Section
        freq_comb = 50
        a = [0 for i in range(freq_sample//freq_comb + 1)]
        a[0] = 1
        a[-1] = -0.965081805687581
        b = [0 for i in range(freq_sample//freq_comb + 1)]
        b[0] = 0.98254090284379
        b[-1] = -0.98254090284379
        a = np.array(a)
        b = np.array(b)
        self.func_make_filter(a, b, len(a), 0)

        # Notch Filter Section
        freq_notch = 50
        gap = 2
        start = freq_notch - gap
        end = freq_notch + gap
        [b, a] = sg.butter(5, [2 * start / freq_sample, 2 * end / freq_sample], 'bandstop')
        self.func_make_filter(a, b, len(a), 1)

        # Bandpass Filter Section
        start = 20
        end = 450
        [b, a] = sg.butter(7, [2 * start / freq_sample, 2 * end / freq_sample], 'bandpass')
        self.func_make_filter(a, b, len(a), 2)

    def run(self, data):
        """DocString for run"""
        #@todo: to be defined.
        		#:data: @todo.
        num = self.func_run(data, self.temp_num, len(data))
        return self.temp_num[:self.channel_num*num]


if __name__ == '__main__':
    cal = Cal()
    cal.change_status(3)
    c = [0x55, 0xAA, 0x58, 0x02, 0x5A, 0x3F, 0x04, 0xFF, 0xFA, 0x17, 0x19, 0x6C, 0x55, 0xAA, 0x58, 0x02, 0x5A, 0x3F, 0x04, 0xFF, 0xFF, 0x17, 0x19, 0x71]
    c = bytes(c)

    cal.design_filter(1000)
    a = cal.run(c)
    print(a)


