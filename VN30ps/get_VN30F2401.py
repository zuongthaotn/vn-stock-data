import warnings
warnings.filterwarnings('ignore')

import pandas as pd

import time
import datetime

import vn_realtime_stock_data.stockHistory as stockHistory

def prepareData(htd):
    if 'Time' in htd.columns:
        from datetime import datetime

        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)

    htd['Date'] = pd.to_datetime(htd['DateStr'])
    ticker_data = htd.set_index('Date')
    ticker_data.drop(columns=['Time', 'DateStr'], inplace=True)
    return ticker_data

if __name__ == "__main__":
    ticker = "VN30F2401"
    date_to = "31/12/2024"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    prepared_data = prepareData(htd)
    save_data = prepared_data.dropna()

    from pathlib import Path
    current_folder = Path(__file__).parent
    save_data.to_csv(str(current_folder) + '/VN30F1M_4_test.csv')
    exit()
