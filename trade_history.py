import json
from twilio.rest import Client

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

        # Send transaction report
        content = open('config.json').read()
        config = json.loads(content)
        twilio_client = Client(config['twilio_account_sid'], config['twilio_auth_token'])
        twilio_client.messages.create(
            to=config['phone_number'],
            from_="+12025179574",
            body="Order to {} sell ${} of {} completed".format(action, price, symbol)
        )
