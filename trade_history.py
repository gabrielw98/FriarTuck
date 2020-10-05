import json
import pprint


class TradeHistory:
    trade_history = {}
    trade_history_path = "trade_history.json"

    def __init__(self):
        with open(TradeHistory.trade_history_path) as f:
            TradeHistory.trade_history = json.load(f)

    # Update trade history
    def update_trade_history(self, symbol, price, action, date):
        new_transaction = {
            "symbol": symbol,
            "price": price,
            "action": action,
            "date": date
        }
        TradeHistory.trade_history["trades"].append(new_transaction)
        with open(TradeHistory.trade_history_path, 'w') as outfile:
            json.dump(TradeHistory.trade_history, outfile, indent=4, separators=(", ", ": "), sort_keys=True)
