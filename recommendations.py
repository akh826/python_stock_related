import yfinance as yf

def allaction(stock):
    list = {'reit': 0, 'down': 0, 'init': 0, 'main': 0, 'up': 0}
    for item in stock.recommendations.iloc[:].Action:
        if item in list:
            count = list.get(item) +1
            list[item] = count
    return list

def main():
    msft = yf.Ticker("MSFT")
    list = allaction(msft)
    print(list)
    

if __name__ == "__main__":
    main()