import matplotlib.pyplot as plt
import numpy as np

data = np.load('../save/20190728151608.npy')

plt.plot(data[:, 15])
plt.show()

