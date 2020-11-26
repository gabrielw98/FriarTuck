import requests
import urllib
import pprint
import sseclient
import threading
import pyEX
from iexfinance.stocks import Stock
import json

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

"""from perspective import PerspectiveWidget
psp = PerspectiveWidget([], 'y_line', columns=['bidPrice', 'askPrice'])

c.topsSSE(symbols='AAPL', on_data=psp.update)"""
"""messages = SSEClient('https://cloud-sse.iexapis.com/stable/stocksUS5Second?token={}&symbols=spy'.format(config["iex_api_key"]))
for message in messages:
    print(message)"""
