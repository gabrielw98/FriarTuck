import fear_greed
import json
from client import Client
from trade_history import TradeHistory

# Trade history
TradeHistory()
print(TradeHistory.trade_history)

# Log into client
client = Client()

# Get trade history
content = open('trade_history.json').read()
trade_history_dict = json.loads(content)

# Trade based on Fear & Greed Index
current_fear_greed_index = fear_greed.scrape_fear_greed_index()
investors_are_greedy = current_fear_greed_index >= fear_greed.sell_threshold
investors_are_fearful = current_fear_greed_index <= fear_greed.buy_threshold
client.trade_on_fear_and_greed(investors_are_greedy, investors_are_fearful, trade_history_dict)

