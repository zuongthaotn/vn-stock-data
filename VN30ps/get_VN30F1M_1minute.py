import warnings

warnings.filterwarnings('ignore')

import vn_realtime_stock_data.stockHistory as stockHistory
from pathlib import Path
from datetime import datetime

ticker = "VN30F" + str(datetime.now().strftime('%y')) + str(datetime.now().strftime('%m'))
STOCK_DATA_DIR = Path(__file__).parent

prepared_data = stockHistory.getVN30HistoryDataByMinute(ticker=ticker, resolution=1)
prepared_data.to_csv(str(STOCK_DATA_DIR) + '/VN30F1M_1minute.csv')
exit()