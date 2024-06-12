import warnings

warnings.filterwarnings('ignore')

from datetime import date
from datetime import timedelta
from pathlib import Path
import pandas as pd
import pandas_ta as ta
import vn_realtime_stock_data.stockHistory as stockHistory

PIVOT_POINTS_TYPE = 'Traditional'
BACK_DAYS = 90
FAST_EMA_LENGTH = 5
LOW_EMA_LENGTH = 26

STOCK_DATA_DIR = Path(__file__).parent


# ticker = "VN30F1M"


def prepareData(htd):
    _1_d_df = htd.copy()
    _1_d_df['First_Open'] = _1_d_df['Open']
    _1_d_df['First_Close'] = _1_d_df['Close']
    _1_d_df['Second_Open'] = _1_d_df['Open']
    _1_d_df['Second_Close'] = _1_d_df['Close']
    _1_d_df = _1_d_df.resample("D").agg({
        'Open': 'first',
        'Close': 'last',
        'High': 'max',
        'Low': 'min',
        'Volume': 'sum',
        'First_Open': cal_first_open,
        'First_Close': cal_first_close,
        'Second_Open': cal_second_open,
        'Second_Close': cal_second_close
    })
    _1_d_df.dropna(inplace=True)
    _1_d_df = cal_pivots(_1_d_df)
    _1_d_df = _1_d_df[['P', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'First_Open',
                       'First_Close', 'Second_Open', 'Second_Close']]
    _1_d_df.dropna(inplace=True)

    htd = htd.assign(time_d=pd.PeriodIndex(htd.index, freq='1D').to_timestamp())
    htd = pd.merge(htd, _1_d_df, left_on="time_d", right_index=True, how="left")
    htd["current"] = htd.index + pd.DateOffset(minutes=5)
    htd['prev_Close'] = htd['Close'].shift(1)
    htd["ema_f"] = ta.ema(htd["Close"], length=FAST_EMA_LENGTH)
    htd["ema_f_shift"] = htd["ema_f"].shift(1)
    htd["ema_l"] = ta.ema(htd["Close"], length=LOW_EMA_LENGTH)
    htd["ema_l_shift"] = htd["ema_l"].shift(1)

    htd["ma_20"] = htd.Close.rolling(20).mean()
    htd["price_std"] = htd.Close.rolling(20).std()
    htd['upper_bb'] = htd["ma_20"] + 2 * htd["price_std"]
    htd['lower_bb'] = htd["ma_20"] - 2 * htd["price_std"]
    htd['rsi'] = ta.rsi(htd["Close"], length=14)
    htd['cross_pivot'] = htd.apply(lambda row: cal_cross(row), axis=1)

    htd.dropna(inplace=True)
    return htd


def cal_cross(row):
    result = ''
    if row['prev_Close'] < row['S5'] < row['Close'] or \
            row['prev_Close'] < row['S4'] < row['Close'] or row['prev_Close'] < row['S3'] < row['Close'] or \
            row['prev_Close'] < row['S2'] < row['Close'] or row['prev_Close'] < row['S1'] < row['Close'] \
            or row['prev_Close'] < row['P'] < row['Close'] or row['prev_Close'] < row['R1'] < row['Close'] \
            or row['prev_Close'] < row['R2'] < row['Close'] or row['prev_Close'] < row['R3'] < row['Close'] \
            or row['prev_Close'] < row['R4'] < row['Close'] or row['prev_Close'] < row['R5'] < row['Close']:
        result = 'cross_up'
    elif row['prev_Close'] > row['S5'] > row['Close'] or \
            row['prev_Close'] > row['S4'] > row['Close'] or row['prev_Close'] > row['S3'] > row['Close'] or \
            row['prev_Close'] > row['S2'] > row['Close'] or row['prev_Close'] > row['S1'] > row['Close'] \
            or row['prev_Close'] > row['P'] > row['Close'] or row['prev_Close'] > row['R1'] > row['Close'] \
            or row['prev_Close'] > row['R2'] > row['Close'] or row['prev_Close'] > row['R3'] > row['Close'] \
            or row['prev_Close'] > row['R4'] > row['Close'] or row['prev_Close'] > row['R5'] > row['Close']:
        result = 'cross_down'
    return result


def cal_first_open(tick):
    tick = tick[100 * tick.index.hour + tick.index.minute == 900]
    return tick


def cal_first_close(tick):
    tick = tick[100 * tick.index.hour + tick.index.minute == 900]
    return tick


def cal_second_open(tick):
    tick = tick[100 * tick.index.hour + tick.index.minute == 905]
    return tick


def cal_second_close(tick):
    tick = tick[100 * tick.index.hour + tick.index.minute == 905]
    return tick


def cal_pivot(row):
    pivot = (row['High_s'] + row['Low_s'] + row['Close_s']) / 3
    return pivot


def cal_r1(row):
    result = 2 * row['P'] - row['Low_s']
    return result


def cal_r2(row):
    result = row['P'] + row['High_s'] - row['Low_s']
    return result


def cal_r3(row):
    # result = row['P'] + 2 * (row['High_s'] - row['Low_s'])    # Classic
    result = row['P'] * 2 + row['High_s'] - 2 * row['Low_s']
    return result


def cal_r4(row):
    # result = row['P'] + 3 * (row['High_s'] - row['Low_s'])    # Classic
    result = row['P'] * 3 + row['High_s'] - 3 * row['Low_s']
    return result


def cal_r5(row):
    # result = row['P'] + 4 * (row['High_s'] - row['Low_s'])      # Classic
    result = row['P'] * 4 + row['High_s'] - 4 * row['Low_s']
    return result


def cal_r6(row):
    # result = row['P'] + 5 * (row['High_s'] - row['Low_s'])      # Classic
    result = row['P'] * 5 + row['High_s'] - 5 * row['Low_s']
    return result


def cal_s1(row):
    result = 2 * row['P'] - row['High_s']
    return result


def cal_s2(row):
    result = row['P'] - (row['High_s'] - row['Low_s'])
    return result


def cal_s3(row):
    # result = row['P'] - 2 * (row['High_s'] - row['Low_s'])  # Classic
    result = row['P'] * 2 - (2 * row['High_s'] - row['Low_s'])
    return result


def cal_s4(row):
    # result = row['P'] - 3 * (row['High_s'] - row['Low_s'])  # Classic
    result = row['P'] * 3 - (3 * row['High_s'] - row['Low_s'])
    return result


def cal_s5(row):
    # result = row['P'] - 4 * (row['High_s'] - row['Low_s'])  # Classic
    result = row['P'] * 4 - (4 * row['High_s'] - row['Low_s'])
    return result


def cal_s6(row):
    # result = row['P'] - 5 * (row['High_s'] - row['Low_s'])  # Classic
    result = row['P'] * 5 - (5 * row['High_s'] - row['Low_s'])
    return result


def cal_pivots(_1_d_df):
    _1_d_df['High_s'] = _1_d_df['High'].shift(1)
    _1_d_df['Low_s'] = _1_d_df['Low'].shift(1)
    _1_d_df['Close_s'] = _1_d_df['Close'].shift(1)
    _1_d_df['Height_s'] = _1_d_df['High_s'] - _1_d_df['Low_s']
    _1_d_df['Volume_s'] = _1_d_df['Volume'].shift(1)

    _1_d_df['P'] = _1_d_df.apply(
        lambda row: cal_pivot(row), axis=1)
    _1_d_df['R1'] = _1_d_df.apply(
        lambda row: cal_r1(row), axis=1)
    _1_d_df['R2'] = _1_d_df.apply(
        lambda row: cal_r2(row), axis=1)
    _1_d_df['R3'] = _1_d_df.apply(
        lambda row: cal_r3(row), axis=1)
    _1_d_df['R4'] = _1_d_df.apply(
        lambda row: cal_r4(row), axis=1)
    _1_d_df['R5'] = _1_d_df.apply(
        lambda row: cal_r5(row), axis=1)
    _1_d_df['R6'] = _1_d_df.apply(
        lambda row: cal_r6(row), axis=1)
    _1_d_df['S1'] = _1_d_df.apply(
        lambda row: cal_s1(row), axis=1)
    _1_d_df['S2'] = _1_d_df.apply(
        lambda row: cal_s2(row), axis=1)
    _1_d_df['S3'] = _1_d_df.apply(
        lambda row: cal_s3(row), axis=1)
    _1_d_df['S4'] = _1_d_df.apply(
        lambda row: cal_s4(row), axis=1)
    _1_d_df['S5'] = _1_d_df.apply(
        lambda row: cal_s5(row), axis=1)
    _1_d_df['S6'] = _1_d_df.apply(
        lambda row: cal_s6(row), axis=1)
    return _1_d_df


if __name__ == "__main__":
    csv_file = str(STOCK_DATA_DIR) + '/VN30F1M_5minutes.csv'
    data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
    data['ibs'] = data.apply(
        lambda x: (1 if (x["High"] == x["Low"]) else (x["Close"] - x["Low"]) / (x["High"] - x["Low"])), axis=1)
    transformed_data = prepareData(data)
    transformed_data.to_csv(str(STOCK_DATA_DIR) + '/VN30F1M_5minutes_transform.csv')
