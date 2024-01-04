import pandas as pd
import platform
import os
import numpy as np
import datetime

path = os.getcwd()

amibroker_file = path + '/amibroker_all_data.txt'

with open(amibroker_file) as f:
    lines = f.readlines()

lines[0] = "<Ticker>,<DTYYYYMMDD>,<Open>,<High>,<Low>,<Close>,<Volume>\n"

with open(amibroker_file, "w") as f:
    f.writelines(lines)

if platform.system() == 'Windows':
    file = path + '\\VNX.csv'
if platform.system() != 'Windows':
    file = path + '/VNX.csv'
#
#
dateparse = lambda x: datetime.datetime.strptime(x, '%Y%m%d')
amibroker_data = pd.read_csv(amibroker_file, parse_dates=['<DTYYYYMMDD>'], date_parser=dateparse)
amibroker_data.columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

ticker_ids = ['ticker']
for index, ticker in amibroker_data.Ticker.iteritems():
    if len(ticker) == 3:
        if not ticker in ticker_ids:
            if ticker.find('^') == -1:
                ticker_ids.append(ticker)


data = np.asarray(ticker_ids)
data_r = data.reshape(len(data), 1)
new_file = path + "/Tickers.csv"
np.savetxt(new_file, data_r, fmt="%s", delimiter=",")
