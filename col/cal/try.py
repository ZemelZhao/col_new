import ctypes
import numpy as np
import os
from ctypes import cdll, c_double


cpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'test.so')
lib = cdll.LoadLibrary(cpath)

func = lib.test
func.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64,
                                        ndim=1,
                                        flags='C_CONTIGUOUS'),
                 ctypes.c_int]

a = np.arange(1, 100, 1)
a = np.array(a, dtype=np.float64)

func(a, len(a))

