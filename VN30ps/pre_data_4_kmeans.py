import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import pandas_ta as ta
import AI.constants as ai_constants


def prepareData(htd):
    htd['Next_Low'] = htd['Low'].shift(-1)
    htd['Next_Low_Is_Lower'] = htd.apply(
        lambda x: (1 if (x["Next_Low"] < x["Low"]) else 0), axis=1)

    htd['today_return'] = htd.apply(
        lambda x: (100 * (x["Close"] - x["Open"]) / (x["High"] - x["Low"])), axis=1)
    htd['pass_1_return'] = htd['today_return'].shift(1)
    htd['pass_2_return'] = htd['today_return'].shift(2)

    htd["EMA_5"] = ta.ema(htd["Close"], length=5)
    htd["EMA_20"] = ta.ema(htd["Close"], length=20)
    htd['EMA_H'] = htd.apply(
        lambda x: (x['EMA_20'] - x['EMA_5']), axis=1)
    htd["RSI_20"] = ta.rsi(htd["Close"], length=20)
    htd['prev_RSI_20'] = htd['RSI_20'].shift(1)
    htd['RSI_trend'] = htd.apply(
        lambda x: (x['RSI_20'] - x['prev_RSI_20']), axis=1)
    htd['RSI_trend'] = htd['RSI_trend'].round(2)
    htd['RSI_20'] = htd['RSI_20'].round(2)
    htd['EMA_H'] = htd['EMA_H'].round(2)
    htd['today_return'] = htd['today_return'].round(2)
    htd['pass_1_return'] = htd['pass_1_return'].round(2)

    return htd

if __name__ == "__main__":
    vn30f1m_file = '{0}/VN30ps/VN30F1M.csv'.format(str(ai_constants.AI_DIR))
    htd = pd.read_csv(vn30f1m_file, index_col=0, parse_dates=True)
    save_data = prepareData(htd)

    from pathlib import Path

    current_folder = Path(__file__).parent
    save_data.to_csv(str(current_folder) + '/VN30F1M_KMeans.csv')
    exit()
