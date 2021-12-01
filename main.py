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
        )
    ],
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
    hs.stockhistory(item,period).plotKdiagram()

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