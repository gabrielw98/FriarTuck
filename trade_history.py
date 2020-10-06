import json


class TradeHistory:
    trade_history = {}
    trade_history_path = "trade_history.json"

    def __init__(self):
        with open(TradeHistory.trade_history_path) as f:
            TradeHistory.trade_history = json.load(f)

    # Update trade history
    @staticmethod
    def update_trade_history(algo, index, symbol, price, action, date, user_id):
        new_transaction = {
            "algo": algo,
            "index": index,
            "symbol": symbol,
            "price": price,
            "action": action,
            "date": date,
            "user_id": user_id
        }
        TradeHistory.trade_history["trades"].append(new_transaction)
        print(new_transaction)
        with open(TradeHistory.trade_history_path, 'w') as outfile:
            json.dump(TradeHistory.trade_history, outfile, indent=4, separators=(", ", ": "), sort_keys=True)
