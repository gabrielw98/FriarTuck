import requests
import ui
import client
from bs4 import BeautifulSoup

buy_threshold = 20
sell_threshold = 80
initial_spy_investment = 100
symbol = "SPY"


def scrape_fear_greed_index():
    fear_greed_url = "https://money.cnn.com/data/fear-and-greed/"
    fear_greed_phrase = "Fear &amp; Greed Now: "
    request = requests.get(fear_greed_url)
    scraper = BeautifulSoup(request.content, features="html.parser")
    div = scraper.find_all(id='needleChart')
    div = str(div[0])
    position = div.find(fear_greed_phrase)
    position += len(fear_greed_phrase)
    return int(div[position:position+3].strip())


def get_buy_equity_amount(trade_history):
    spy_sell_history_dict = {}
    price_to_buy = initial_spy_investment
    min_date = None

    for trade in trade_history:
        is_spy_sell = trade["symbol"] == symbol and trade["action"] == "sell"
        if is_spy_sell and min_date is None or trade["date"] > min_date:
            price_to_buy = trade["price"]
    print(spy_sell_history_dict)
    return price_to_buy


def get_sell_equity_amount():
    return client.get_held_positions()[symbol]["equity"]


def owns_spy():
    try:
        spy_position = client.get_held_positions()["SPY"]
        ui.success(spy_position)
        return True
    except KeyError:
        return False



