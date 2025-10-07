import warnings

warnings.filterwarnings('ignore')

from pathlib import Path
import vn_realtime_stock_data.stockHistory as stockHistory

ticker = "VN30F1M"
STOCK_DATA_DIR = Path(__file__).parent

prepared_data = stockHistory.getVN30HistoryDataByMinute(ticker=ticker, resolution="1H")
prepared_data.to_csv(str(STOCK_DATA_DIR) + '/VN30F1M_1H.csv')
exit()
