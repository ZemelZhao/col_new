import ctypes
import numpy as np
import scipy.signal as sg
import cal

so = ctypes.cdll.LoadLibrary
lib = so('./filter.so')

[b, a] = sg.butter(3, [0.05, 0.9], 'bandpass')
func_make_filter = lib.makeFilter
func_change_stat = lib.changeStat
func_run_filter = lib.runFilter
func_run = lib.run

func2 = lib.test

func_make_filter.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                  np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                  ctypes.c_int, ctypes.c_int]
func_change_stat.argtypes = [ctypes.c_int, ctypes.c_int]
func_run_filter.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS')]
func_run.argtypes = [ctypes.c_char_p,
                    np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                     ctypes.c_int]

a = np.array([1, 2, 3, 4], dtype=np.float64)
b = np.array([2, 3, 4, 5], dtype=np.float64)

func_change_stat(2, 0)
func_make_filter(a, b, 4, 0)

data = [0x55, 0xAA, 0x7A, 0x01, 0x7B, 0x02, 0x07, 0x12, 0xB5, 0xD0,
        0x55, 0xAA, 0x7A, 0x01, 0x7B, 0x04, 0x12, 0x14, 0x17, 0x41]
data = bytes(data)

res = np.array(4*[0], dtype=np.float64)

func_run(data, res, len(data))

print(res)


