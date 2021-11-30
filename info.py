import yfinance as yf
import json
def actions(stock):
    return stock.actions

def dividends(stock):
    return stock.dividends

def spilt(stock):
    return stock.Splits

def pretty(d, indent=0):
       for key, value in d.items():
            print('\t' * indent + str(key)+':')
            if isinstance(value, dict):
                pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))

def printinfo(stock):
    pretty(stock.info)

def main():
    msft = yf.Ticker("MSFT")
    list = printinfo(msft)
    

if __name__ == "__main__":
    main()