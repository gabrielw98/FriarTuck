def with_urllib3(url):
    """Get a streaming response for the given event feed using urllib3."""
    import urllib3
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False)


def with_requests(url):
    """Get a streaming response for the given event feed using requests."""
    import requests
    return requests.get(url, stream=True)


"""def lookup(symbol):

    # Contact API
    try:

        api_key = config["iex_api_key"]
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None
    print(lookup("AAPL"))"""

"""def printit():
  threading.Timer(5.0, printit).start()
  print(iex_client.price(symbol=sym))

content = open('config.json').read()
config = json.loads(content)
iex_client = pyEX.Client(config["iex_api_key"])
#iex_client.tradesSSE(symbols='AAPL', on_data=print)
sym='TWTR'
printit()"""

from iexfinance.stocks import get_historical_data
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

""""## You can adjust your dates here ##
start = datetime(2020, 1, 2)
end = datetime(2020, 6, 27)

## You can change your stock symbol here ##
ticker = 'SPY'
content = open('config.json').read()
config = json.loads(content)

df = pd.DataFrame(get_historical_data(ticker, start, end, output_format='pandas', token=config["iex_api_key"]))
dates = df.index.values.tolist()

close_26_ewma = df['close'].ewm(span=26, min_periods=0, adjust=True, ignore_na=True).mean()
close_12_ewma = df['close'].ewm(span=12, min_periods=0, adjust=True, ignore_na=True).mean()
df['26ema'] = close_26_ewma
df['12ema'] = close_12_ewma

df['MACD'] = (df['12ema'] - df['26ema'])"""