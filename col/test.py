
import numpy as np
import time

a = np.arange(100000)
b = np.arange(100000)

c = a.tolist()
d = b.tolist()

h = 1000

e = time.time()
for i in range(h):
    g = np.hstack((a, b))
print(time.time() - e)

f = time.time()
for i in range(h):
    g = c + d
print(time.time() - f)



