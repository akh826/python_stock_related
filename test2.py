import yfinance as yf
from scipy.signal import argrelextrema
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
 

def main():
    msft = yf.Ticker("MSFT")

    
    data_x = np.arange(start = 0, stop = 25, step = 1, dtype='int')
    data_y = np.random.random(25)*6

    # Find peaks(max).
    peak_indexes = signal.argrelextrema(data_y, np.greater)
    peak_indexes = peak_indexes[0]
        
    # Plot main graph.
    (fig, ax) = plt.subplots()
    ax.plot(data_x, data_y)
    
    # Plot peaks.
    peak_x = peak_indexes
    peak_y = data_y[peak_indexes]
    print(len(data_x))
    print(len(data_y))
    print(len(peak_x))
    print(len(peak_y))
    ax.plot(peak_x, peak_y, marker='o', linestyle='dashed', color='green', label="Peaks")

    # Save graph to file.
    plt.title('Find peaks and valleys using argrelextrema()')
    plt.legend(loc='best')
    plt.show()
    

if __name__ == "__main__":
    main()
