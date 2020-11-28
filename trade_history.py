import json
from twilio.rest import Client
import datetime

class TradeHistory:
    trade_history = {}
    trade_history_path = "trade_history.json"
    initial_investment = 100.0

    def __init__(self):
        with open(TradeHistory.trade_history_path) as f:
            TradeHistory.trade_history = json.load(f)

    @staticmethod
    def get_sell_equity_amount(symbol, algo):
        min_date = None
        price_to_sell = 0.0
        for trade in TradeHistory.trade_history["trades"]:
            is_symbol_sell = trade["symbol"] == symbol and trade["action"] == "buy" and trade["algo"] == algo
            current_date = datetime.datetime.strptime(trade["date"], '%m/%d/%Y %H:%M:%S')
            if is_symbol_sell and (min_date is None or current_date > min_date):
                price_to_sell = trade["price"]
                min_date = current_date
        return price_to_sell

    @staticmethod
    def get_buy_equity_amount(symbol, algo):
        price_to_buy = TradeHistory.initial_investment
        min_date = None

        for trade in TradeHistory.trade_history["trades"]:
            is_symbol_sell = trade["symbol"] == symbol and trade["action"] == "sell" and trade["algo"] == algo
            current_date = datetime.datetime.strptime(trade["date"], '%m/%d/%Y %H:%M:%S')
            if is_symbol_sell and (min_date is None or current_date > min_date):
                price_to_buy = trade["price"]
                min_date = current_date
        return price_to_buy

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
            body="Order to {} ${} of {} completed".format(action, price, symbol)
        )
