import pandas as pd
import platform
import os
import numpy as np
import datetime

dateparse = lambda x: datetime.datetime.strptime(x, '%Y%m%d')

path = os.getcwd()
if platform.system() == 'Windows':
    file = path + '\\VNX.csv'
if platform.system() != 'Windows':
    file = path + '/VNX.csv'
    #
amibroker_file = path + '/cophieu68/amibroker_all_data.txt'
# with open(amibroker_file, "r+") as f: s = f.read(); f.seek(0); f.write("<Ticker>,<DTYYYYMMDD>,<Open>,<High>,<Low>,<Close>,<Volume>\n" + s)
amibroker_data = pd.read_csv(amibroker_file, parse_dates=['<DTYYYYMMDD>'], date_parser=dateparse)
amibroker_data.columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
vnx_csv_data = pd.read_csv(file, usecols=["ticker"])
ticker_ids = np.array(vnx_csv_data)
for ticker in ticker_ids:
    ticker_id = ticker[0]
    newdf = amibroker_data[(amibroker_data.Ticker == ticker_id)]
    new_file = path + "/cophieu68/" + ticker_id + ".csv"
    newdf.to_csv(new_file, index=False)
