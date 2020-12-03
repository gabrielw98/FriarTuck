import json
import robin_stocks as rh
import ui
import fear_greed
import macd
import golden_cross
from trade_history import TradeHistory
from datetime import datetime, timedelta
from collections import Counter

# *Make client a class and initialize vars
# *Populate trade history
# *Pretty print the trade_history
# *Run trader.py every morning at 11AM EST
# *create df's for each stock in watch list
# *every day at the same time append the new value and determine if a trade should be made
# *use the intersection of the signal line and MACD to make a trade
# TODO use 2fa to bypass token issue
# Entry/Exit Signals: Alligator, Bollinger Bands
# Indicators (use indicators for multiplier price and potentially sell if the position has gained enough): VWAP
# Eventually add an intraday strategy
    # 15 minute buy point
    # Every Tue and Thur check use indicators to determine what's the best position
    # Buy 1000k of the position. Use stop limit order of +75/-50


class Client:
    held_positions = {}
    current_user_id = ""

    def __init__(self):
        # Log into the client
        self.login()

        # Set get the held positions of the client's portfolio
        Client.held_positions = rh.build_holdings()

    def login(self):
        content = open('config.json').read()
        config = json.loads(content)
        result = rh.login(config['email'], config["password"])
        Client.current_user_id = config['email']
        if result is not None and result["detail"] != "logged in using authentication in robinhood.pickle":
            ui.error(result)

    def trade_on_intraday_strategy(self):
        symbols = ["TWLO", "FB"]

        account_info = rh.helper.request_get("https://api.robinhood.com/accounts/5XB92092/")["margin_balances"]
        print(account_info)
        day_trade_count = int(float(account_info["day_trade_ratio"])/0.25)
        print("Day trades:", day_trade_count)

    def trade_on_fear_and_greed(self, current_fear_greed_index):

        investors_are_greedy = current_fear_greed_index >= fear_greed.sell_threshold
        investors_are_fearful = current_fear_greed_index <= fear_greed.buy_threshold
        owns_spy = fear_greed.owns_spy()
        current_date_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        if investors_are_greedy and owns_spy:
            # Sell entire SPY position
            price = fear_greed.get_sell_equity_amount()
            result = rh.order_sell_fractional_by_price(fear_greed.symbol,
                                                       price, extendedHours=True, timeInForce="gfd")

            if result is not None and 'account' in result.keys():
                TradeHistory.update_trade_history(fear_greed.algo, current_fear_greed_index, fear_greed.symbol, price,
                                                  "sell", current_date_time, Client.current_user_id)
            else:
                ui.error(result)
        elif investors_are_fearful and not owns_spy:
            # Buy initial SPY investment or the last sold equity
            price = fear_greed.get_buy_equity_amount(TradeHistory.trade_history['trades'])
            result = rh.order_buy_fractional_by_price(fear_greed.symbol, price, extendedHours=True, timeInForce="gfd")

            if result is not None and 'account' in result.keys():
                TradeHistory.update_trade_history(fear_greed.algo, current_fear_greed_index, fear_greed.symbol, price,
                                                  "buy", current_date_time, Client.current_user_id)
            else:
                ui.error(result)
        else:
            # Skip SPY trade because there is not yet a significant fear or greed value
            skipped_dict = {
                "algo": fear_greed.algo,
                "index": current_fear_greed_index,
                "action": "skipped",
                "date": current_date_time,
                "price": "N/A",
                "symbol": "N/A",
                "user_id": Client.current_user_id
            }
            ui.success(skipped_dict)
            return

    def trade_on_macd(self):
        symbols = ["SE", "TTD", "DDOG", "SHOP", "SQ", "DRIP", "CHWY", "OSTK", "NET",
                   "CHGG", "PINS", "DAL", "SNAP", "BABA", "NET", "IRBT", "MDB", "DKNG",
                   "BYND", "GRUB", "SPOT", "GPS", "INO", "ENPH", "GOLD", "IDXX", "CRNC"]

        restricted_stocks = ["AAPL", "WORK", "PLTR", "ROKU", "ETSY"]
        symbols = list((Counter(symbols) - Counter(restricted_stocks)).elements())

        current_date_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        no_transactions = True
        for symbol in symbols:
            df = macd.create_df(symbol)
            df = macd.add_entry_for_today(symbol, df)
            # macd.plot_macd(df, symbol)

            action = macd.get_trade_action(df)
            if action == "buy" and not TradeHistory.already_holding_position(symbol, macd.algo) and False:
                no_transactions = False
                # Buy initial investment or the last sold equity
                price = TradeHistory.get_buy_equity_amount(symbol, "macd")
                result = rh.order_buy_fractional_by_price(symbol, price, extendedHours=True,
                                                          timeInForce="gfd")
                if result is not None and 'account' in result.keys():
                    TradeHistory.update_trade_history(macd.algo, "N/A", symbol, price,
                                                      "buy", current_date_time, Client.current_user_id)
                else:
                    ui.error(result)
            elif action == "sell" and TradeHistory.already_holding_position(symbol, macd.algo):
                # Sell entire position
                price = TradeHistory.get_sell_equity_amount(symbol, "macd")
                no_transactions = False
                result = rh.order_sell_fractional_by_price(symbol, price,
                                                           extendedHours=True, timeInForce="gfd")
                if result is not None and 'account' in result.keys():
                    TradeHistory.update_trade_history(macd.algo, "N/A", symbol, price, "sell",
                                                      current_date_time, Client.current_user_id)
                else:
                    ui.error(result)
            else:
                continue
        if no_transactions:
            skipped_dict = {
                "algo": macd.algo,
                "index": "N/A",
                "action": "skipped",
                "date": current_date_time,
                "price": "N/A",
                "symbol": "N/A",
                "user_id": Client.current_user_id
            }
            ui.success(skipped_dict)

    def trade_on_golden_cross(self):
        held_tickers = Client.held_positions.keys()
        spy_tickers = golden_cross.get_spy_tickers()
        print(spy_tickers)
        print(len(spy_tickers - held_tickers))
