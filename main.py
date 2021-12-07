import PySimpleGUI as sg
import os.path
import history as hs
from pathlib import Path
import csv
import threading

file_list_column = [
    [
        sg.Text("Stock"),
        sg.In(size=(25, 1), enable_events=True, key="-Stock-"),
        # sg.FolderBrowse(),
        sg.Text("Period"),
        sg.Combo(['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'],default_value='1y',key='-Period-'),
        
    ],
    [sg.Button("addfav"),sg.Button("get"),sg.Button("getfav"),],

    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FAV LIST-"
        ),
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        ),
    ],
    [   
        sg.Checkbox('volume', default=True,key='volume'),
        sg.Checkbox('macd', default=True,key='macd'),
        sg.Checkbox('ma', default=True,key='ma'),
        sg.Checkbox('peaks & nadir', default=True,key='pn'),   
    ]
]

image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

filepath = "file"
favfile ="fav.csv"
graph_file_list = []
fav_list =[]

def updategraphlist(window):
    try:
            graph_file_list = os.listdir("file")
    except:
        graph_file_list = []

    fnames = [
        f
        for f in graph_file_list
        if os.path.isfile(os.path.join(filepath, f))
        and f.lower().endswith((".png", ".gif"))
    ]
    window["-FILE LIST-"].update(fnames)
    return graph_file_list

def updatefavlist(window):
    if (Path(favfile).exists()):
        with open(favfile, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            fav_list = [
                    f
                    for f in spamreader
                ]      
            window["-FAV LIST-"].update(fav_list)
            return fav_list
    return []
def readfav():
    if (Path(favfile).exists()):
        with open(favfile, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))

def writetofav(text):
    if (Path(favfile).exists()):
        with open(favfile, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([text])

def mutithreadstock(item,period):
    print(f"{item},{period}")
    ticker = yf.Ticker(item)
    h = hs.stockhistory(item,period)
    plotKdiagram(h.data,ticker,period)
    
import yfinance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import talib as ta
import pandas as pd
from scipy.signal import argrelextrema
import numpy as np
def plotKdiagram(data,ticker,period,values):
    aplot =[]

    #volume
    if (values["volume"]):
        data['Volume'] = data['Volume'] / 1000

    #macd
    data["macd"], data["macd_signal"], data["macd_hist"] = ta.MACD(data['Close'])
    colors = ['g' if v >= 0 else 'r' for v in data["macd_hist"]]
    if period not in ['1d','5d','1mo']:
        aplot.append(mpf.make_addplot(data["macd_hist"], type='bar', panel=1, color=colors))

    #moving average
    open_mav10 = data["Open"].rolling(10).mean().values
    open_mav20 = data["Open"].rolling(20).mean().values
    mavdf = pd.DataFrame(dict(OpMav10=open_mav10,OpMav20=open_mav20))
    if period not in ['1d','5d']:
        aplot.append(mpf.make_addplot(mavdf,type='line'))

    data.index.name = 'Date'
    data.shape
    data.head(3)
    data.tail(3)

    #peaks & nadir
    max = np.maximum(data["Open"].values,data["Close"].values)
    min = np.minimum(data["Open"].values,data["Close"].values)
    peaksdate = argrelextrema(max, np.greater, order=5)
    nadirdate = argrelextrema(min, np.less, order=5)
    peak = np.empty(len(data))
    peak[:] = np.NaN
    nadir = np.empty(len(data))
    nadir[:] = np.NaN
    for num in peaksdate[0]:
        peak[num] = max[num]#self.data["Open"][num]
    for num in nadirdate[0]:
        nadir[num] = min[num]#self.data["Open"][num]
    aplot.append(mpf.make_addplot(peak, type='scatter', marker='o', markersize=20, color='r'))
    aplot.append(mpf.make_addplot(nadir, type='scatter', marker='o', markersize=20, color='g'))
    mpf.plot(data,type='candle',style='charles', addplot=aplot, title=f"\n{ticker}\n{period}", ylabel='', savefig=f'file/{ticker.info["symbol"]}_{period}.png')
    plt.close()

def main():

    Path(filepath).mkdir(parents=True, exist_ok=True)
    if not (Path(favfile).exists()):
        f= open(favfile,"w+")
        f.close()

    
    window = sg.Window("Image Viewer", layout)
    event, values = window.read(timeout=0)
    graph_file_list = updategraphlist(window)
    fav_list = updatefavlist(window)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "get" and values['-Stock-'] != "":
            h1 = hs.stockhistory(values['-Stock-'],values['-Period-'])
            if h1.valid:
                h1.plotKdiagram()

        elif event == "addfav" and [values['-Stock-']] not in fav_list:
            if hs.stockhistory(values['-Stock-'],values['-Period-']).valid:
                writetofav(values['-Stock-'])

        elif event == "-FAV LIST-":
            window['-Stock-'].update(values['-FAV LIST-'][0][0])
            

        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    filepath, values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)
            except:
                pass
        elif event == "getfav":
            thread=[]
            for item in fav_list:
                thread.append(threading.Thread(target = mutithreadstock, args = (item[0],values['-Period-'],)))
            for i in range(len(thread)):
                thread[i].start()
            for i in range(len(thread)):
                thread[i].join()
        graph_file_list = updategraphlist(window)
        fav_list = updatefavlist(window)
        # print(fav_list)
    window.close()

if __name__ == "__main__":
    main()