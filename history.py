from numpy import equal
import yfinance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import talib as ta
import pandas as pd
from scipy.signal import argrelextrema
import numpy as np

class stockhistory():
    diagram =None
    block = True
    save = True
    valid = False
    def __init__(self, ticker, period):
        self.ticker = yf.Ticker(ticker)
        self.check()
        self.period = period
        self.data= self.ticker.history(period)

    def check(self):
        if (self.ticker.info['regularMarketPrice'] != None):
            self.valid = True
        else:
            self.valid = False
    
    def printhistory(self):
        if self.valid:
            print(self.ticker.history(period=self.period))

    def style():
        return mpf.available_styles()

    def allhistory(self):
        if self.valid:
            print(self.stock.history(period="max"))

    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    def somehistory(self,period):
        if self.valid:
        # Open        High         Low       Close    Volume  Dividends  Stock Splits
            return self.stock.history(period=period)

    def plotKdiagram(self):
        if self.valid:
            aplot =[]

            #volume
            self.data['Volume'] = self.data['Volume'] / 1000

            #macd
            self.data["macd"], self.data["macd_signal"], self.data["macd_hist"] = ta.MACD(self.data['Close'])
            colors = ['g' if v >= 0 else 'r' for v in self.data["macd_hist"]]
            if self.period not in ['1d','5d','1mo']:
                aplot.append(mpf.make_addplot(self.data["macd_hist"], type='bar', panel=1, color=colors))

            #moving average
            open_mav10 = self.data["Open"].rolling(10).mean().values
            open_mav20 = self.data["Open"].rolling(20).mean().values
            mavdf = pd.DataFrame(dict(OpMav10=open_mav10,OpMav20=open_mav20))
            if self.period not in ['1d','5d']:
                aplot.append(mpf.make_addplot(mavdf,type='line'))

            self.data.index.name = 'Date'
            self.data.shape
            self.data.head(3)
            self.data.tail(3)

            #peaks & nadir
            max = np.maximum(self.data["Open"].values,self.data["Close"].values)
            min = np.minimum(self.data["Open"].values,self.data["Close"].values)
            peaksdate = argrelextrema(max, np.greater, order=5)
            nadirdate = argrelextrema(min, np.less, order=5)
            peak = np.empty(len(self.data))
            peak[:] = np.NaN
            nadir = np.empty(len(self.data))
            nadir[:] = np.NaN
            for num in peaksdate[0]:
                peak[num] = max[num]#self.data["Open"][num]
            for num in nadirdate[0]:
                nadir[num] = min[num]#self.data["Open"][num]
            aplot.append(mpf.make_addplot(peak, type='scatter', marker='o', markersize=20, color='r'))
            aplot.append(mpf.make_addplot(nadir, type='scatter', marker='o', markersize=20, color='g'))
            if self.save:
                mpf.plot(self.data,type='candle',style='charles', addplot=aplot, title=f"\n{self.ticker}\n{self.period}", ylabel='', savefig=f'file/{self.ticker.info["symbol"]}_{self.period}.png')
            else: 
                mpf.plot(self.data,type='candle',style='charles', addplot=aplot, title=f"\n{self.ticker}\n{self.period}", ylabel='', block=self.block)
            plt.close()

def main():
    h1 = stockhistory("MSFT","2y")
    # h1.save = False
    # h1.plotKdiagram()
    h1.printhistory()

if __name__ == "__main__":
    main()

