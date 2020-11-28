import matplotlib.patches as mpatches
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import ui
from iexfinance.stocks import get_historical_data
import pyEX
import os
from datetime import datetime, timedelta

algo = "macd"


def create_df(symbol):
    file_names = os.listdir('./watchlist_history')
    df_cached = False
    for name in file_names:
        if ".pkl" in name and name[0:len(symbol)] == symbol:
            df_cached = True
    if df_cached:
        df = pd.read_pickle("./watchlist_history/{}_history.pkl".format(symbol))
    else:
        current_date = datetime.today()
        three_months_ago = current_date - timedelta(days=30 * 3)
        df = query_iex_history(symbol, current_date, three_months_ago)
        df = add_entry_for_today(symbol, df)
    return df


def query_iex_history(symbol, current_date, six_months_ago):
    content = open('config.json').read()
    config = json.loads(content)
    if six_months_ago < current_date:
        df = pd.DataFrame(get_historical_data(symbol, six_months_ago, current_date, output_format='pandas',
                                              token=config["iex_api_key"]))
        update_df_with_macd(df)
    else:
        df = np.Dataframe()
        ui.error("Invalid start date {} and end date {}".format(current_date, six_months_ago))
    extra_columns = ["open", "high", "low", "volume"]
    df = df.drop(columns=extra_columns)
    pd.to_pickle(df, "./watchlist_history/{}_history.pkl".format(symbol))
    return df


def update_df_with_macd(df):

    # Moving Averages
    close_26_ewma = df['close'].ewm(span=26, min_periods=0, adjust=True, ignore_na=True).mean()
    close_12_ewma = df['close'].ewm(span=12, min_periods=0, adjust=True, ignore_na=True).mean()
    df['26ema'] = close_26_ewma
    df['12ema'] = close_12_ewma

    # MACD values
    df['MACD'] = (df['12ema'] - df['26ema'])
    signal_line = df['MACD'].ewm(span=9, min_periods=0, adjust=True, ignore_na=True).mean()
    df['signal_line'] = signal_line


def plot_macd(df, symbol):
    plt.figure(figsize=(12, 7))

    plt.plot(df["close"], color="orange")
    plt.plot(df["26ema"], color="b")
    plt.plot(df["12ema"], color="g")

    plt.plot()
    orange_entry = mpatches.Patch(color='orange', label='Close Price')
    blue_entry = mpatches.Patch(color='blue', label='26 Day MA')
    green_entry = mpatches.Patch(color='green', label='12 Day MA')
    purple_entry = mpatches.Patch(color='purple', label='Signal Line')
    macd_entry = mpatches.Patch(color='gray', label='MACD')
    plt.legend(handles=[orange_entry, blue_entry, green_entry, purple_entry, macd_entry])
    plt.grid(True)

    ma_intersections = np.argwhere(np.diff(np.sign(df["12ema"] - df["26ema"]))).flatten()
    plt.plot(df["12ema"][ma_intersections], 'ro')

    ma_buy = []
    ma_sell = []
    for i in ma_intersections:
        if df['26ema'][i - 1] > df["12ema"][i - 1] and len(ma_sell) == len(ma_buy) and i > 0:
            ma_buy.append(df["close"][i])
        elif df['26ema'][i - 1] < df["12ema"][i - 1] and len(ma_buy) > 0 and i > 0:
            ma_sell.append(df["close"][i])

    plt.plot(df['MACD'], color="gray")
    plt.plot(df['signal_line'], color="purple")

    # macd_intersections = np.argwhere(np.diff(np.sign(df["MACD"] - df["signal_line"]))).flatten()

    macd_buy, macd_buy_indexes, macd_sell, macd_sell_indexes = get_signal_crosses(df)
    plt.plot(df["signal_line"][macd_buy_indexes], 'go')
    plt.plot(df["signal_line"][macd_sell_indexes], 'ro')

    plt.title('{} Profits\nMACD (\${})   vs.   MA (\${})'.format(symbol, get_profit(macd_buy, macd_sell),
                                                                 get_profit(ma_buy, ma_sell)))
    plt.show()


def add_entry_for_today(symbol, df):

    # IEX Client
    content = open('config.json').read()
    config = json.loads(content)
    iex_client = pyEX.Client(config["iex_api_key"])

    # New DF Entry
    current_date = datetime.today().strftime('%Y-%m-%d')
    current_price = iex_client.quote(symbol)["latestPrice"]

    '''
    # For testing transaction
    tomorrow = datetime.today() + timedelta(days=1)
    last_macd_entry = df.iloc[len(df) - 1, df.columns.get_loc('MACD')]
    last_signal_entry = df.iloc[len(df) - 1, df.columns.get_loc('signal_line')]
    sell_row = pd.Series(data={'close': current_price, '26ema': 0.0, '12ema': 0.0, "MACD": last_macd_entry - 5.0, "signal_line" : last_signal_entry + 5.0}, name=current_date)
    #buy_row = pd.Series(data={'close': current_price, '26ema': 0.0, '12ema': 0.0, "MACD": last_macd_entry + 10.0,
    #                         "signal_line": last_signal_entry - 10.0}, name=tomorrow)
    df = df.append(sell_row, ignore_index=False)
    #df = df.append(buy_row, ignore_index=False)
    '''

    new_row = pd.Series(data={'close': current_price, '26ema': 0.0, '12ema': 0.0, "MACD": 0.0}, name=current_date)
    df = df.append(new_row, ignore_index=False)
    update_df_with_macd(df)

    pd.to_pickle(df, "./watchlist_history/{}_history.pkl".format(symbol))
    return df


def get_profit(buy_list, sell_list):
    profit = 0.0
    for i in range(min(len(sell_list), len(buy_list))):
        profit += sell_list[i] - buy_list[i]
    return round(profit, 2)


def get_signal_crosses(df):
    macd_buy = []
    macd_buy_indexes = []
    macd_sell = []
    macd_sell_indexes = []

    for i in range(len(df) - 1):
        # buy when the MACD crosses above its signal line
        # sell when the MACD crosses below the signal line

        prev_macd = df.iloc[i, df.columns.get_loc('MACD')]
        prev_signal = df.iloc[i, df.columns.get_loc('signal_line')]

        curr_macd = df.iloc[i + 1, df.columns.get_loc('MACD')]
        curr_signal = df.iloc[i + 1, df.columns.get_loc('signal_line')]
        curr_close = df.iloc[i + 1, df.columns.get_loc('close')]

        if prev_signal - prev_macd > 0 and curr_macd - curr_signal > 0 and len(macd_sell) == len(macd_buy):
            macd_buy.append(curr_close)
            macd_buy_indexes.append(i + 1)
        elif prev_macd - prev_signal > 0 and curr_signal - curr_macd > 0 and len(macd_buy) > 0:
            macd_sell.append(curr_close)
            macd_sell_indexes.append(i + 1)

    return macd_buy, macd_buy_indexes, macd_sell, macd_sell_indexes


def get_trade_action(df):
    macd_buy, macd_buy_indexes, macd_sell, macd_sell_indexes = get_signal_crosses(df)
    last_index = len(df) - 1
    if last_index in macd_buy_indexes:
        return "buy"
    elif last_index in macd_sell_indexes:
        return "sell"
    else:
        return "skip"
