# python_stock_related

written in python 3.9.6 and windows 10

talib link: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

On Windows
```bash
$py -m venv venv #create venv
$venv\Scripts\activate.bat #use venv
$py -m pip install -r requirements.txt #install lib
$py -m pip install lib/TA_Lib-0.4.21-cp39-cp39-win_amd64.whl
$py -m main.py #un program
```

On linux (Ubuntu 20.04,python3.8.10):
```
$python -m venv venv
$source venv\bin\activate
$pip install -r requirements.txt
$sudo apt install python3-tk
$cd lib/ta-lib/
$./configure --prefix=/usr
$make
$sudo make install
$pip install ta-lib
$python main.py
```