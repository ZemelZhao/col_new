        data = self.data[:, 62]
        a = [0 for i in range(30-1)]
        a.insert(0, 1)
        a.append(-0.965081805687581)
        b = [0 for i in range(30-1)]
        b.insert(0, 0.98254090284379)
        b.append(-0.98254090284379)
        data = sg.filtfilt(b, a, data)
        [b, a] = sg.butter(5, [0.03, 0.9], 'bandpass')
        data = sg.filtfilt(b, a, data)
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



