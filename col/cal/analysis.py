import matplotlib.pyplot as plt
import numpy as np

data = np.load('../save/20190730095006.npy')

plt.plot(data[:, 1])
plt.show()
