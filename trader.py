import fear_greed
from client import Client
from trade_history import TradeHistory

# Cron job script:
'''
15 11 * * 1-5 cd ~/Desktop/workspaces/FriarTuck && /usr/local/bin/python3 trader.py 
>> ~/Desktop/workspaces/FriarTuck/trader_logs.txt 2>&1
'''

# Trade history
TradeHistory()

# Log into client
client = Client()

# Trade based on Intraday Market Open Strategy
# client.trade_on_intraday_strategy()

# Trade based on Fear & Greed Index
current_fear_greed_index = fear_greed.scrape_fear_greed_index()
client.trade_on_fear_and_greed(current_fear_greed_index)

# Trade based on golden cross
# client.trade_on_golden_cross()

# Trade based on moving average convergence divergence
client.trade_on_macd()


