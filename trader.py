import fear_greed, client, ui
import json

# Log into client
result = client.login()
ui.success("Success: Logged In") if result is None else ui.error(result)

# Get trade history
content = open('trade_history.json').read()
trade_history_dict = json.loads(content)

# Trade based on Fear & Greed Index
current_fear_greed_index = fear_greed.scrape_fear_greed_index()
investors_are_greedy = current_fear_greed_index >= fear_greed.sell_threshold
investors_are_fearful = current_fear_greed_index <= fear_greed.buy_threshold
client.trade_on_fear_and_greed(investors_are_greedy, investors_are_fearful, trade_history_dict)

