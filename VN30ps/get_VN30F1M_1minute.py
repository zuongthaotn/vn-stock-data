import warnings

warnings.filterwarnings('ignore')

import vn_realtime_stock_data.stockHistory as stockHistory
import AI.constants as constants
from datetime import datetime

ticker = "VN30F" + str(datetime.now().strftime('%y')) + str(datetime.now().strftime('%m'))

prepared_data = stockHistory.getVN30HistoryDataByMinute(ticker=ticker, resolution=1)
vn_stock_data_folder = str(constants.ALGO_DIR) + '/vn-stock-data'
prepared_data.to_csv(str(vn_stock_data_folder) + '/VN30F1M_1minute.csv')
exit()
