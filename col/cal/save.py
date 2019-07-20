from ctypes import(cdll, Structure, POINTER, c_int, c_double,
                   c_char_p, )
import numpy as np
from scipy import signal as sg
import os
import sys
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
try:
    from base.log import Log
    from base.conf import ConfigProcess
    from base.val import GlobalConstValue as gcv
except ImportError:
    print('fuck')
import random
import matplotlib
matplotlib.rcParams['backend'] = 'SVG'
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
from scipy import signal as sg

class FileSave(object):
    """ DocString for FileSave"""
    def __init__(self, conf, log):
        #@todo: to be defined.
        self.conf = conf
        self.log = log
        self.cpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '_filter.cpython-36m-x86_64-linux-gnu.so')
        self.lib = cdll.LoadLibrary(self.cpath)

        self.func_change_stat = self.lib.changeStat
        self.func_change_stat.argtypes = [c_int, c_int]

        self.func_run = self.lib.run
        self.func_run.argtypes = [c_char_p, np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'), c_int]

        self.list_cache_res = []

    def data_exact(self):
        """DocString for data_exact"""
        #@todo: to be defined.
        index = 0
        time_record = index
        index_max = len(self.cache)
        num_leap_data = self.channel_num * 2 + 6
        num_leap_flag = 512
        while index < index_max:
            temp_res = np.zeros(self.channel_num + 2)
            if self.cache[index] == 0x55 and self.cache[index+1] == 0xAA:
                temp_num = self.func_run(self.cache[index : index + num_leap_data], temp_res, num_leap_data)
                if temp_num:
                    temp_res[-1] = time_record
                    time_record += self.time_freq_sample
                    self.list_cache_res.append(temp_res)
                    index += num_leap_data
                else:
                    index += 1
            elif self.cache[index] == self.cache[index + 1]:
                flag = self.make_flag(index)
                if flag:
                    self.list_cache_res[-1][-2] = flag
                    index += num_leap_flag
                else:
                    index += 1
            else:
                index += 1
        return np.array(self.list_cache_res)

    def make_flag(self, index):
        """DocString for make_flag"""
        #@todo: to be defined.
		#:index: @todo.
        temp = self.cache[index]
        for i in range(512):
            if self.cache[index + i] != temp:
                return 0
        return temp + 1

    def run(self, data_ini, f=False):
        """DocString for file_save"""
        #@todo: to be defined.
        #:file_path_data: @todo.
		#:file_path_save: @todo.
		#:filter: @todo.

        dict_res = self.conf.config_read()
        self.channel_num = int(dict_res['Data']['channel_num'])
        self.time_freq_sample = 1 / int(dict_res['Filter']['sampling_freq'])
        self.func_change_stat(self.channel_num, 0)
        self.func_change_stat(250, 1)

        self.cache = data_ini

        res = self.data_exact()
        res[:, :self.channel_num] -= 32768
        if filter:
            pass
        return res

class PicSave(object):
    """ DocString for Save"""
    def __init__(self, conf, log):
        #@todo: to be defined.
        #:conf: @todo.
		#:log: @todo.
        self.conf = conf
        self.log = log
        self.val = gcv()

    def draw(self, data, path_pic='temp.svg', all=0):
        """DocString for draw"""
        #@todo: to be defined.
		#:data: @todo.
		#:path_pic: @todo.
        dict_config = self.conf.config_read()
        channel_num = data.shape[1]
        show_second = self.val.gui_show_second
        data *= 20
        freq_sample = int(dict_config['Filter']['sampling_freq'])
        if data.shape[0] < show_second*freq_sample:
            temp = np.zeros((show_second*freq_sample - data.shape[0], channel_num))
            data = np.vstack((temp, data))
        t = np.arange(data.shape[0])* 10 / (data.shape[0])
        plt.figure(figsize=(19.2, 10.8 / 64 * channel_num), )

        plt.gca().invert_yaxis()
        plt.subplots_adjust(left=0.019,
                            right=1 - 0.014*64 / channel_num,
                            bottom=0.025 * 64 / channel_num,
                            top=1+0.03 * 64 / channel_num)
        plt.yticks(np.arange(1, channel_num+1))
        plt.xlim(0, 10)
        plt.ylim(0, channel_num+4)
        plt.plot((2, 2), (0, 300), c='black')
        plt.plot((4, 4), (0, 300), c='black')
        plt.plot((6, 6), (0, 300), c='black')
        plt.plot((8, 8), (0, 300), c='black')
        data = data.T
        for i in range(channel_num):
            plt.plot(t, data[i] / 1+i+1, )
        plt.savefig(path_pic, format='svg')

class DataProcess(object):
    """ DocString for Save"""
    def __init__(self, conf, log, save=1, filt=0):
        #@todo: to be defined.
        #:conf: @todo.
		#:log: @todo.
        #:save:
        #   1: start with the final option.
        #   0: start with the start

        self.conf = conf
        self.log = log
        self.save = save
        self.filt = filt
        self.val = gcv()
        self.flag = self.val.flag_trigger

        self.cpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '_filter.cpython-36m-x86_64-linux-gnu.so')
        self.lib = cdll.LoadLibrary(self.cpath)

        self.func_change_stat = self.lib.changeStat
        self.func_change_stat.argtypes=[c_int, c_int]

        self.func_run = self.lib.run
        self.func_run.argtypes=[c_char_p, np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'), c_int]

        self.res = []


    def run(self, data):
        """DocString for run"""
        #@todo: to be defined.
		#:data: @todo.
        self.data = data
        if self.save:
            self.find_final_option_flag()
        else:
            self.find_start_flag()
        self.get_data()
        return self.res

    def find_final_option_flag(self, ):
        """DocString for find_start_flag"""
        data_temp = self.data[::-1]
        index = len(data_temp) - data_temp.find(self.flag[4])
        self.data = self.flag[4] + self.data[index: ]

    def find_start_flag(self, ):
        """DocString for find_start_flag"""
        #@todo: to be defined.
        index = self.data.find(self.flag[0])
        self.data = self.data[index:]

    def get_data(self, ):
        self.__get_data_pre()
        self.__get_data_raw()
        self.__get_data_float()
        if self.filt:
            self.__get_data_filt()

    def __get_data_pre(self, ):
        """DocString for __get_data_pre"""

        if self.save:
            if self.data[:512] == self.flag[4]:
                pass
            else:
                return False
        else:
            if self.data[:512] == self.flag[0]:
                pass
            else:
                return False
        dict_conf = self.conf.config_read()
        self.channel_num = int(dict_conf['Data']['channel_num'])
        self.sample_freq = int(dict_conf['Filter']['sampling_freq'])
        self.time_sample = 1 / self.sample_freq
        if self.filt:
            self.filter_notch_able = int(dict_conf['Filter']['filter_notch_able'])
            self.filter_band_able = int(dict_conf['Filter']['filter_band_able'])
            self.filter_notch = int(dict_conf['Filter']['filter_notch'])
            self.filter_band_high = int(dict_conf['Filter']['filter_band_high'])
            self.filter_band_low = int(dict_conf['Filter']['filter_band_low'])

        self.func_change_stat(self.channel_num, 0)
        leap_times = 1
        self.func_change_stat(leap_times*250, 1)

    def __get_data_raw(self, ):
        """DocString for __get_data_run"""
        #@todo: to be defined.
        index = 0
        time_record = 0
        flag_record = 0
        index_max = len(self.data)
        num_leap_data = self.channel_num*2 + 6
        num_leap_flag = len(self.flag[0])
        while index < index_max - 1:
            temp_res = np.zeros(self.channel_num + 2)
            if self.data[index] == 0x55 and self.data[index+1] == 0xAA:
                temp_num = self.func_run(self.data[index : index + num_leap_data], temp_res, num_leap_data)
                if temp_num:
                    temp_res[-2] = time_record
                    time_record += self.time_sample
                    temp_res[-1] = flag_record
                    flag_record = 0
                    self.res.append(temp_res)
                    index += num_leap_data
                else:
                    index += 1
            elif self.data[index] == self.data[index+1]:
                flag = self.__get_data_check_flag(index)
                if flag:
                    flag_record = flag
                    index += num_leap_flag
                else:
                    index += 1
            else:
                index += 1
        self.res = np.array(self.res)

    def __get_data_check_flag(self, index):
        """DocString for __get_data_check_flag"""
        #@todo: to be defined.
   		#:index: @todo.
        temp = self.data[index]
        for i in range(1, len(self.flag[0])):
            if self.data[index+i] != temp:
                return False

        return temp + 1

    def __get_data_filt(self, ):
        """DocString for __get_data_filt"""
        #@todo: to be defined.
        if self.filter_notch_able or self.filter_band_able:
            pass

    def __get_data_float(self, ):
        """DocString for __get_data_float"""
        #@todo: to be defined.
        self.res[:, :self.channel_num] -= 32768
        self.res[:, :self.channel_num] *= (4.5 / (65536 * 24))

class Save(object):
    """ DocString for Save"""

    def __init__(self, conf, log, save_loc=1, filt=0):
        #@todo: to be defined.
        #:conf: @todo.
		#:log: @todo.

        self.conf = conf
        self.log = log
        self.data_process = DataProcess(self.conf, self.log, save_loc, filt)
        self.save_pic = PicSave(self.conf, self.log)
        self.save_file = FileSave(self.conf, self.log)
        self.val = gcv()


    def run(self, data):
        """DocString for run"""
        #@todo: to be defined.
		#:data: @todo.
        self.data = self.data_process.run(data)
        data = self.data[:, 62]
        a = [0 for i in range(30-1)]
        a.insert(0, 1)
        a.append(-0.965081805687581)
        b = [0 for i in range(30-1)]
        b.insert(0, 0.98254090284379)
        b.append(-0.98254090284379)
        data = sg.filtfilt(b, a, data)
        [b, a] = sg.butter(5, [0.03, 0.9], 'bandpass')
        data = sg.filtfilt(b, a, data)
        yy = fft(data)
        yy = np.abs(yy)
        print(len(data))
        x = np.linspace(0, 1000/2, len(data) // 2)
        print(max(data) - min(data))
        plt.subplot(211)
        plt.plot(data)
        plt.xlabel('time(s)')
        plt.ylabel('Volt')
        plt.subplot(212)
        plt.plot(x, yy[:len(data) // 2])
        plt.xlabel('freq(Hz)')
        plt.show()



    def __find_flag(self):
        """DocString for find_flag"""
        #@todo: to be defined.
        list_res = []





if __name__ == '__main__':
    pass
