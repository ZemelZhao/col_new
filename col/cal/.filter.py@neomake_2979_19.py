from ctypes import(cdll, Structure, POINTER, c_int, c_double,
                   c_char_p)
import numpy as np
ll = cdll.LoadLibrary
lib = ll('./filter.so')


a = np.array([1, 2, 3, 4, 5, 6, 7], dtype='float64')
b = np.array([1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1], dtype='float64')

func = lib.makeFilt1
func.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                 np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                 c_int]

func = lib.readFromTCP
func.argtypes = [c_char_p, c_int]
c = b'ab12345'




