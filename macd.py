import matplotlib.patches as mpatches
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import ui
from iexfinance.stocks import get_historical_data
import os
from datetime import datetime, timedelta


def create_df(symbol):
    file_names = os.listdir('./watchlist_history')
    df_cached = False
    for name in file_names:
        print(name)
        if ".pkl" in name and name[0:len(symbol)] == symbol:
            df_cached = True
    if df_cached:
        df = pd.read_pickle("./watchlist_history/{}_history.pkl".format(symbol))
        print(symbol, "is pickled!")
        plot_macd(df, symbol)
    else:
        current_date = datetime.today()
        six_months_ago = current_date - timedelta(days=30 * 3)
        df = get_history(symbol, current_date, six_months_ago)
        plot_macd(df, symbol)
    return df


def get_history(symbol, current_date, six_months_ago):
    content = open('config.json').read()
    config = json.loads(content)
    if six_months_ago < current_date:
        df = pd.DataFrame(get_historical_data(symbol, six_months_ago, current_date, output_format='pandas',
                                              token=config["iex_api_key"]))
        close_26_ewma = df['close'].ewm(span=26, min_periods=0, adjust=True, ignore_na=True).mean()
        close_12_ewma = df['close'].ewm(span=12, min_periods=0, adjust=True, ignore_na=True).mean()
        df['26ema'] = close_26_ewma
        df['12ema'] = close_12_ewma
        df['MACD'] = (df['12ema'] - df['26ema'])
    else:
        df = np.Dataframe()
        ui.error("Invalid start date {} and end date {}".format(current_date, six_months_ago))
    pd.to_pickle(df, "./watchlist_history/{}_history.pkl".format(symbol))
    return df


def plot_macd(df, symbol):
    plt.figure(figsize=(7, 7))

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
            print("Buy at", df.index[i], df["close"][i])
            ma_buy.append(df["close"][i])
        elif df['26ema'][i - 1] < df["12ema"][i - 1] and len(ma_buy) > 0 and i > 0:
            print("Sell at", df.index[i], df["close"][i])
            ma_sell.append(df["close"][i])

    plt.plot(df['MACD'], color="gray")
    signal_line = df['MACD'].ewm(span=9, min_periods=0, adjust=True, ignore_na=True).mean()
    plt.plot(signal_line, color="purple")
    df['signal_line'] = signal_line

    macd_intersections = np.argwhere(np.diff(np.sign(df["MACD"] - df["signal_line"]))).flatten()
    plt.plot(df["signal_line"][macd_intersections], 'ro')

    macd_buy = []
    macd_sell = []
    for i in macd_intersections:
        if df['signal_line'][i - 1] > df["MACD"][i - 1] and len(macd_sell) == len(macd_buy) and i > 0:
            print("Buy at", df.index[i], df["close"][i])
            macd_buy.append(df["close"][i])
        elif df['signal_line'][i - 1] < df["MACD"][i - 1] and len(macd_buy) > 0 and i > 0:
            print("Sell at", df.index[i], df["close"][i])
            macd_sell.append(df["close"][i])

    plt.title('{} Profits\nMACD (\${})   vs.   MA (\${})'.format(symbol, get_profit(macd_buy, macd_sell),
                                                                 get_profit(ma_buy, ma_sell)))
    plt.show()


def get_profit(buy_list, sell_list):
    profit = 0.0
    for i in range(min(len(sell_list), len(buy_list))):
        profit += sell_list[i] - buy_list[i]
    return round(profit, 2)
