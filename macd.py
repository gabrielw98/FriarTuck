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
    file_names = os.listdir('.')
    df_cached = False
    for name in file_names:
        if ".pkl" in name and name[0:len(symbol)] == symbol:
            df_cached = True
    if df_cached:
        df = pd.read_pickle("./{}_history.pkl".format(symbol))
        print(symbol, "is pickled!")
        plot_macd(df)
    else:
        current_date = datetime.today()
        six_months_ago = current_date - timedelta(days=30*6)
        df = get_history(symbol, current_date, six_months_ago)
        plot_macd(df)
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
        print(df)
    else:
        df = np.Dataframe()
        ui.error("Invalid start date {} and end date {}".format(current_date, six_months_ago))
    pd.to_pickle(df, "./{}_history.pkl".format(symbol))
    return df


def plot_macd(df):

    plt.figure(figsize=(7, 12))
    df = df.tail(120)

    plt.plot(df["close"], color="orange")
    plt.plot(df["26ema"], color="b")
    plt.plot(df["12ema"], color="g")
    print(df)
    df["zeros"] = np.zeros(len(df["12ema"]))
    plt.plot(df.index, df["zeros"], color="purple")
    plt.plot(df["12ema"], color="g", label='12 Day MA')

    plt.plot()
    orange_entry = mpatches.Patch(color='orange', label='Close Price')
    blue_entry = mpatches.Patch(color='blue', label='26 Day MA')
    green_entry = mpatches.Patch(color='green', label='12 Day MA')
    plt.legend(handles=[orange_entry, blue_entry, green_entry])
    plt.grid(True)

    moving_average_intersections = np.argwhere(np.diff(np.sign(df["12ema"] - df["26ema"]))).flatten()
    plt.plot(df["12ema"][moving_average_intersections], 'ro')
    plt.plot(df["26ema"][moving_average_intersections], 'ro')

    plt.plot(df['MACD'])

    signal_line = df['MACD'].ewm(span=9, min_periods=0, adjust=True, ignore_na=True).mean()
    plt.plot(signal_line, color="red")
    df['signal_line'] = signal_line

    macd_intersections = np.argwhere(np.diff(np.sign(df["MACD"] - df["signal_line"]))).flatten()
    plt.plot(df["signal_line"][macd_intersections], 'ro')
    plt.plot(df["MACD"][macd_intersections], 'ro')

    print("MACD buy sell points:", macd_intersections)
    print("Moving average buy sell points:", moving_average_intersections)
    plt.show()
