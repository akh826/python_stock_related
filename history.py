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
    def __init__(self, ticker, period):
        self.ticker = ticker
        self.period = period
        self.data= ticker.history(period)
    
    def printhistory(self):
        print(self.ticker.history(period=self.period))

    def style():
        return mpf.available_styles()

    def allhistory(stock):
        print(stock.history(period="max"))

    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    def somehistory(stock,period):
        # Open        High         Low       Close    Volume  Dividends  Stock Splits
        return stock.history(period=period)

    def plotKdiagram(self):
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
        peaksdate = argrelextrema(self.data["Open"].values, np.greater, order=5)
        nadirdate = argrelextrema(self.data["Open"].values, np.less, order=5)
        peak = np.empty(len(self.data))
        peak[:] = np.NaN
        nadir = np.empty(len(self.data))
        nadir[:] = np.NaN
        for num in peaksdate[0]:
            peak[num] = self.data["Open"][num]
        for num in nadirdate[0]:
            nadir[num] = self.data["Open"][num]
        aplot.append(mpf.make_addplot(peak, type='scatter', marker='o', markersize=20, color='r'))
        aplot.append(mpf.make_addplot(nadir, type='scatter', marker='o', markersize=20, color='g'))
                    
        mpf.plot(self.data,type='candle',style='charles', addplot=aplot, title=f"\n{self.ticker}\n{self.period}", ylabel='')
    
def main():
    h1 = stockhistory(yf.Ticker("MSFT"),"1mo")
    h1.plotKdiagram()

if __name__ == "__main__":
    main()

