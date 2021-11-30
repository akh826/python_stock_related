import yfinance as yf

def main():
    msft = yf.Ticker("MSFT")
    result = msft.actions
    print(result)
    

if __name__ == "__main__":
    main()
