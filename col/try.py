import numpy as np
import os

data = np.load('save/20190731124145f.npy')
a = data[data[:, -1] != 0]
print(a)

