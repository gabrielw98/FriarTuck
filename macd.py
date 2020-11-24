from iexfinance.stocks import Stock
import json
import matplotlib.patches as mpatches
import requests
import urllib
import pprint
import sseclient
import threading
import pyEX
import numpy as np





df = pd.read_pickle("./spy_history.pkl")
dates = df.index.values.tolist()

plt.figure(figsize=(7, 12))
df = df.tail(120)
close = plt.plot(df["close"], color="orange", label='close price')
ema_26 = plt.plot(df["26ema"], color="b", label='26 Day MA')
ema_12 = plt.plot(df["12ema"], color="g", label='12 Day MA')

orange_entry = mpatches.Patch(color='orange', label='Close Price')
blue_entry = mpatches.Patch(color='blue', label='26 Day MA')
green_entry = mpatches.Patch(color='green', label='12 Day MA')
plt.legend(handles=[orange_entry, blue_entry, green_entry])

plt.grid(True)

plt.plot(df['MACD'])
plt.grid(True)

print(type(np.arange(0, 1000)))
print(type(np.array(ema_26)))
idx = np.argwhere(np.diff(np.sign(df["26ema"] - df["12ema"]))).flatten()
plt.plot(df["12ema"][idx], 'ro')
plt.plot(df["26ema"][idx], 'ro')
plt.show()
print(df)
#pd.to_pickle(df, "./spy_history.pkl")




"""from perspective import PerspectiveWidget
psp = PerspectiveWidget([], 'y_line', columns=['bidPrice', 'askPrice'])

c.topsSSE(symbols='AAPL', on_data=psp.update)"""
"""messages = SSEClient('https://cloud-sse.iexapis.com/stable/stocksUS5Second?token={}&symbols=spy'.format(config["iex_api_key"]))
for message in messages:
    print(message)"""
