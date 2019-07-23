import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg
from scipy.fftpack import fft, ifft

if __name__ == '__main__':
    data = np.load('../save/20190721234240.npy')
    print(data.shape)
    """
    data = data[30000:, 44]
    data_temp = data[:]
    a = [0 for i in range(19)]
    a.insert(0, 1)
    a.append(-0.965081805687581)
    b = [0 for i in range(19)]
    b.insert(0, 0.98254090284379)
    b.append(-0.98254090284379)
    data = sg.filtfilt(b, a, data)
    [b, a] = sg.butter(5, [0.01, 0.9], 'bandpass')
    data = sg.filtfilt(b, a, data)
    data = data_temp[:]
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
    """

