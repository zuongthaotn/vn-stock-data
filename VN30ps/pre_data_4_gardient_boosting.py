import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import pandas_ta as ta
import AI.VN30ps.DecisionTree.constants as constants
import AI.constants as ai_constants


def convertTrend(value):
    if np.isnan(value):
        trend_value = np.nan
    elif value < constants.TREND_WEAK_MAX:
        trend_value = constants.TREND_WEAK
    elif value < constants.TREND_NORMAL_MAX:
        trend_value = constants.TREND_NORMAL
    elif value < constants.TREND_STRONG_MAX:
        trend_value = constants.TREND_STRONG
    else:
        trend_value = constants.TREND_VERY_STRONG

    return trend_value


def convertRSI(value):
    if np.isnan(value):
        rsi = np.nan
    elif value < 30:
        rsi = 20
    elif value < 50:
        rsi = 45
    elif value < 80:
        rsi = 65
    else:
        rsi = 80

    return rsi


def convertATR(value):
    if np.isnan(value):
        atr = np.nan
    elif value < 10:
        atr = 1
    elif value < 20:
        atr = 2
    elif value < 30:
        atr = 3
    elif value < 40:
        atr = 4
    else:
        atr = 5

    return atr


def convertUpDown(open, close):
    if close - open == 0:
        today_updown = constants.TODAY_NO_MOVE
    elif close - open > 0:
        today_updown = constants.TODAY_IS_UP
    else:
        today_updown = constants.TODAY_IS_DOWN

    return today_updown


def calBodyCandlestickRate(open, close, high, low):
    if high == low:
        return 0
    rate = abs(open - close) / (high - low)
    return round(rate, 1)


def calTailCandlestickRate(open, close, high, low):
    u = min(open, close)
    if u == low:
        return 0
    rate = (u - low) / (high - low)
    return round(rate, 1)


def prepareData(htd):
    htd['Next_Open'] = htd['Open'].shift(-1)
    htd['Next_Open_Is_Lower'] = htd.apply(
        lambda x: (1 if (x["Next_Open"] < x["Open"]) else 0), axis=1)
    htd['Next_Low'] = htd['Low'].shift(-1)
    htd['Next_Low_Is_Lower'] = htd.apply(
        lambda x: (1 if (x["Next_Low"] < x["Low"]) else 0), axis=1)

    htd['Next_Close'] = htd['Close'].shift(-1)
    htd['Next_Close_Is_Lower'] = htd.apply(
        lambda x: (1 if (x["Next_Close"] < x["Close"]) else 0), axis=1)

    short_adx = ta.adx(htd['High'], htd['Low'], htd['Close'], length=constants.LENGTH_SHORT_ADX)
    htd["ADX_" + str(constants.LENGTH_SHORT_ADX)] = short_adx["ADX_" + str(constants.LENGTH_SHORT_ADX)]
    htd["short_trend"] = htd.apply(
        lambda row: convertTrend(row.loc["ADX_" + str(constants.LENGTH_SHORT_ADX)]), axis=1
    )

    htd["Today_Up_Down"] = htd.apply(
        lambda row: convertUpDown(row.loc["Open"], row.loc["Close"]), axis=1
    )
    htd['Yesterday_Up_Down'] = htd['Today_Up_Down'].shift(1)
    htd['Next_Up_Down'] = htd['Today_Up_Down'].shift(-1)

    htd["Body_Candlestick_Rate"] = htd.apply(
        lambda row: calBodyCandlestickRate(row.loc["Open"], row.loc["Close"], row.loc["High"], row.loc["Low"]), axis=1
    )

    htd["Tail_Candlestick_Rate"] = htd.apply(
        lambda row: calTailCandlestickRate(row.loc["Open"], row.loc["Close"], row.loc["High"], row.loc["Low"]), axis=1
    )

    htd["RSI_10"] = ta.rsi(htd["Close"], length=10)
    htd["RSI_10_Simple"] = htd.apply(
        lambda row: convertRSI(row.loc["RSI_10"]), axis=1
    )

    htd["ATR_" + str(constants.LENGTH_ATR)] = ta.atr(htd['High'], htd['Low'], htd['Close'], length=constants.LENGTH_ATR)
    htd["Volatility_ATR"] = htd.apply(
        lambda row: convertATR(row.loc["ATR_" + str(constants.LENGTH_ATR)]), axis=1
    )

    htd["EMA_5"] = ta.ema(htd["Close"], length=5)
    htd["EMA_20"] = ta.ema(htd["Close"], length=20)
    htd['MA5-MA20'] = htd.apply(
        lambda row: (row['EMA_5'] - row['EMA_20']) / min(row['EMA_5'], row['EMA_20']), axis=1)
    htd['MA5_MA20'] = htd.apply(
        lambda row: abs(row['EMA_5'] - row['EMA_20']) / min(row['EMA_5'], row['EMA_20']), axis=1)

    htd['MA5-MA20_yesterday'] = htd['MA5-MA20'].shift(1)
    htd['MA5-MA20_2_days_ago'] = htd['MA5-MA20'].shift(2)
    htd['MA5_MA20_yesterday'] = htd['MA5_MA20'].shift(1)
    htd['MA5_MA20_rate'] = htd.apply(
        lambda row: row['MA5_MA20'] / row['MA5_MA20_yesterday'], axis=1)
    htd['MA5_MA20_rate'] = htd['MA5_MA20_rate'].round(0)
    htd['MA5_MA20'] = htd['MA5_MA20'].round(2)
    htd['MA5-MA20'] = htd['MA5-MA20'].round(2)
    htd['MA5-MA20_yesterday'] = htd['MA5-MA20_yesterday'].round(2)
    htd['MA5-MA20_2_days_ago'] = htd['MA5-MA20_2_days_ago'].round(2)
    # The scope of these changes made to
    # pandas settings are local to with statement.
    # with pd.option_context('display.max_rows', None,
    #                        'display.max_columns', None,
    #                        'display.precision', 3,
    #                        ):
    #     print(htd.describe())
    # exit()
    return htd


if __name__ == "__main__":
    vn30f1m_file = '{0}/VN30ps/data/VN30F1M.csv'.format(str(ai_constants.AI_DIR))
    htd = pd.read_csv(vn30f1m_file, index_col=0, parse_dates=True)
    save_data = prepareData(htd)

    from pathlib import Path

    current_folder = Path(__file__).parent
    save_data.to_csv(str(current_folder) + '/VN30F1M_for_gradient_boosting2.csv')
    exit()
