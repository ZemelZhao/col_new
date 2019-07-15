import ctypes
import numpy as np
import scipy.signal as sg
from cal import ComTinker

a = np.ones(32)

a[4] = 0

print(np.sum(a == 1))
