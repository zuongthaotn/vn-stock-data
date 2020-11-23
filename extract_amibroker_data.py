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
vnx_csv_data = pd.read_csv(file, usecols=["ticker"])
ticker_ids = np.array(vnx_csv_data)
for ticker in ticker_ids:
    ticker_id = ticker[0]
    newdf = amibroker_data[(amibroker_data.Ticker == ticker_id)]
    newdf.drop(['Ticker'], axis=1)
    new_file = path + "/VNX/" + ticker_id + ".csv"
    newdf.to_csv(new_file, index=False)
