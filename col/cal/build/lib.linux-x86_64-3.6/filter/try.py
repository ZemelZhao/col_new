import ctypes
import numpy as np
import scipy.signal as sg
from cal import ComTinker

cal = ComTinker()

[b, a] = sg.butter(3, [0.05, 0.9], 'bandpass')
cal.dict_data['filter0 A'][2] = len(a)
cal.dict_data['filter0 B'][2] = len(b)
[d, c] = sg.butter(5, [0.1, 0.2], 'bandstop')
cal.dict_data['filter1 A'][2] = len(c)
cal.dict_data['filter1 B'][2] = len(d)

a = cal.listdouble2listbyte(a)
b = cal.listdouble2listbyte(b)
c = cal.listdouble2listbyte(c)
d = cal.listdouble2listbyte(d)

list_data = ['filter0 A', 'filter0 B', 'filter1 A', 'filter1 B']
list_data_data = [a, b, c, d]
list_command = ['channel num', 'freq sample']
list_command_data = [[255], [3, 249]]
c = cal.make_command(list_command, list_command_data, list_data, list_data_data)
data = []

a = 2000
b = bytes(ctypes.c_int(a))
print(b)
