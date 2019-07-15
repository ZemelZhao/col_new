from ctypes import(cdll, Structure, POINTER, c_int, c_double,
                   c_char_p, )
import numpy as np
from scipy import signal as sg
import os
import sys
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
from base.log import Log
from base.conf import ConfigProcess
import random

class Cal(object):
    """ DocString for Cal"""
    def __init__(self, conf, log):
        #@todo: to be defined.
        self.conf = conf
        self.log = log
        self.cal = ComTinker()
        self.cpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '_filter.cpython-36m-x86_64-linux-gnu.so')
        #self.cpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'filter.so')
        self.lib = cdll.LoadLibrary(self.cpath)

        self.func_change_stat = self.lib.changeStat
        self.func_change_stat.argtypes = [c_int, c_int]

        self.func_make_filter = self.lib.makeFilter
        self.func_make_filter.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                          np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                          c_int, c_int]

        self.func_run = self.lib.run
        self.func_run.argtypes = [c_char_p, np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'), c_int]

        self.temp_num = np.zeros(700)
        self.channel_num = 0
        self.freq_sample = 0

    def change_status(self, test=False, hardware_filter=False, command_default=True):
        """DocString for change_status"""
        #@todo: to be defined.
		#:hardware_filter: @todo.
        dict_res = self.conf.config_read()
        self.log.info(self, 'Change Status')
        self.channel_num = int(dict_res['Data']['channel_num'])
        self.freq_sample = int(dict_res['Filter']['sampling_freq'])
        self.func_change_stat(self.channel_num, 0)
        self.func_change_stat(self.freq_sample, 1)
        list_data, list_data_data = self.design_filter(test, hardware_filter)
        if command_default:
            list_command = ['default']
            list_command_data = [[self.freq_sample // 250 - 1, 250 - 1, self.channel_num - 1]]
        else:
            list_command = ['channel num', 'freq sample']
            list_command_data = [[self.channel_num - 1], [self.freq_sample // 250 - 1, 250 - 1]]
        res = self.cal.make_command(list_command, list_command_data, list_data, list_data_data)
        return bytes(res)

    def design_filter(self, test=True, hardware_filter=False):
        """DocString for design_filter"""
        #@todo: to be defined.
		#:freq_sample: @todo.

        # Comb Filter Section
        if test:
            return None, None
        res = [[], []]
        freq_comb = 50
        a = [0 for i in range(self.freq_sample//freq_comb + 1)]
        a[0] = 1
        a[-1] = -0.965081805687581
        b = [0 for i in range(self.freq_sample//freq_comb + 1)]
        b[0] = 0.98254090284379
        b[-1] = -0.98254090284379
        res[0].append('filter0 A')
        res[0].append('filter0 B')
        self.cal.dict_data['filter0 A'][2] = len(a)
        self.cal.dict_data['filter0 B'][2] = len(a)
        res[1].append(self.cal.listdouble2listbyte(a))
        res[1].append(self.cal.listdouble2listbyte(b))
        a = np.array(a)
        b = np.array(b)
        if not hardware_filter:
            self.func_make_filter(a, b, len(a), 0)

        # Notch Filter Section
        freq_notch = 50
        gap = 2
        start = freq_notch - gap
        end = freq_notch + gap
        [b, a] = sg.butter(5, [2 * start / self.freq_sample, 2 * end / self.freq_sample], 'bandstop')
        res[0].append('filter1 A')
        res[0].append('filter1 B')
        self.cal.dict_data['filter1 A'][2] = len(a)
        self.cal.dict_data['filter1 B'][2] = len(a)
        res[1].append(self.cal.listdouble2listbyte(a))
        res[1].append(self.cal.listdouble2listbyte(b))
        if not hardware_filter:
            self.func_make_filter(a, b, len(a), 1)

        # Bandpass Filter Section
        start = 20
        end = 450
        [b, a] = sg.butter(7, [2 * start / self.freq_sample, 2 * end / self.freq_sample], 'bandpass')
        res[0].append('filter2 A')
        res[0].append('filter2 B')
        self.cal.dict_data['filter2 A'][2] = len(a)
        self.cal.dict_data['filter2 B'][2] = len(a)
        res[1].append(self.cal.listdouble2listbyte(a))
        res[1].append(self.cal.listdouble2listbyte(b))
        if not hardware_filter:
            self.func_make_filter(a, b, len(a), 2)
        self.log.info(self, 'Design Filter')

        if hardware_filter:
            return res
        else:
            return [None, None]

    def run(self, data):
        """DocString for run"""
        #@todo: to be defined.
        		#:data: @todo.
        num = self.func_run(data, self.temp_num, len(data))
        #self.log.debug(self, 'RightNum: %d' % num)
        #print('here %f' % random.random())
        return self.temp_num[:self.channel_num*num]

class ComTinker(object):
    """ DocString for ComTinker"""
    def __init__(self, ):
        #@todo: to be defined.
        self.dict_command = {'channel num': [0x80, 1, 1, 0b00], 'freq sample': [0x81, 2, 1, 0b10],
                             'default': [0x00, 1, 3, 0b00]
                             }
        self.dict_data = {'filter0 A': [0x00, 8, 0, 0b11], 'filter0 B': [0x01, 8, 0, 0b11],
                          'filter1 A': [0x02, 8, 0, 0b11], 'filter1 B': [0x03, 8, 0, 0b11],
                          'filter2 A': [0x04, 8, 0, 0b11], 'filter2 B': [0x05, 8, 0, 0b11],
                          'filter3 A': [0x06, 8, 0, 0b11], 'filter3 B': [0x07, 8, 0, 0b11],
                          'filter4 A': [0x08, 8, 0, 0b11], 'filter4 B': [0x09, 8, 0, 0b11],
                          'filter5 A': [0x0A, 8, 0, 0b11], 'filter5 B': [0x0B, 8, 0, 0b11],
                          'filter6 A': [0x0C, 8, 0, 0b11], 'filter6 B': [0x0D, 8, 0, 0b11],
                          'filter7 A': [0x0E, 8, 0, 0b11], 'filter7 B': [0x0F, 8, 0, 0b11],
                          'filter8 A': [0x10, 8, 0, 0b11], 'filter8 B': [0x11, 8, 0, 0b11],
                          'filter9 A': [0x12, 8, 0, 0b11], 'filter9 B': [0x13, 8, 0, 0b11],
                          'filtera A': [0x14, 8, 0, 0b11], 'filtera B': [0x15, 8, 0, 0b11],
                          'filterb A': [0x16, 8, 0, 0b11], 'filterb B': [0x17, 8, 0, 0b11],
                          'filterc A': [0x18, 8, 0, 0b11], 'filterc B': [0x19, 8, 0, 0b11],
                          'filterd A': [0x1A, 8, 0, 0b11], 'filterd B': [0x1B, 8, 0, 0b11],
                          'filtere A': [0x1C, 8, 0, 0b11], 'filtere B': [0x1D, 8, 0, 0b11],
                          'filterf A': [0x1E, 8, 0, 0b11], 'filterf B': [0x1F, 8, 0, 0b11],
                      }

    def make_command(self, list_command=None, list_command_data=None,
                     list_data=None, list_data_data=None):
        """DocString for make_command"""
        #@todo: to be defined.
        res = []
        if list_command:
            res += self.__make_single_command(self.dict_command, list_command, list_command_data, True, not bool(list_data))
        if list_data:
            res += self.__make_single_command(self.dict_data, list_data, list_data_data, False, True)
        return res

    def listdouble2listbyte(self, data):
        """DocString for listdouble2listbyte"""
        #@todo: to be defined.
   		#:data: @todo.
        res = []
        for i in data:
            temp = list(bytes(c_double(i)))
            res += temp
        return res

    def __make_single_command(self, dict_command, list_command, list_command_data, command=True, stop=True, ):
        """DocString for __make_command"""
        #@todo: to be defined.
		#:list_command: @todo.
		#:list_command_data: @todo.
        res = []
        for i in range(len(list_command) - 1):
            command_temp = dict_command[list_command[i]]
            data_temp = list_command_data[i]
            res_temp = self.__make_command_head(command_temp[0], command_temp[1], command_temp[2], command, False, [command_temp[3]])
            res_temp += list_command_data[i]
            res_temp.append(sum(list_command_data[i]) % 256)
            res += res_temp
        command_temp = dict_command[list_command[-1]]
        data_temp = list_command_data[-1]
        if stop:
            res_temp = self.__make_command_head(command_temp[0], command_temp[1], command_temp[2], command, True, command_temp[3])
        else:
            res_temp = self.__make_command_head(command_temp[0], command_temp[1], command_temp[2], command, False, dtype)
        res_temp += list_command_data[-1]
        res_temp.append(sum(list_command_data[-1]) % 256)
        res += res_temp
        return res

    def __make_command_head(self, command_order, byte, num, command=True, stop=True, dtype=0b00):
        """DocString for make_command_head"""
        #@todo: to be defined.
		#:stop: @todo.
		#:command: @todo.
        # byte : @todo
        # num : @todo
        res = [0x5A, 0xA5, 0x00, 0x00, 0x00]
        if stop:
            res[2] += 1 << 7
        if command:
            res[2] += 1 << 6
        res[2] += byte * 2 - 1
        res[2] += (dtype << 4)
        res[3] += num - 1
        res[4] += command_order
        res.append((res[2] + res[3] + res[4]) % 256)
        return res

if __name__ == '__main__':
    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'log', 'log.out'))
    conf = ConfigProcess(config_ini_path, config_temp_path, log)

    cal = Cal(conf, log)
    a = cal.change_status(True)
    c = [0x55, 0xAA, 0x58, 0x02, 0x5A, 0x3F, 0x04, 0xFF, 0xFA, 0x17, 0x19, 0x6C, 0x55, 0xAA, 0x58, 0x02, 0x5A, 0x3F, 0x04, 0xFF, 0xFF, 0x17, 0x19, 0x71]
    c = bytes(c)
    b = cal.run(c)
    print(b)

