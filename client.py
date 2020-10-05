import json
import robin_stocks as rh
import ui
import fear_greed
from trade_history import TradeHistory
import datetime

# *Make client a class and initialize vars
# *Populate trade history
# TODO Pretty print the trade_history
# TODO Deploy in cloud


class Client:

    held_positions = {}

    def __init__(self):
        # Log into the client
        self.login()
        self.test_purcahse()

        # Set get the held positions of the client's portfolio
        Client.held_positions = rh.build_holdings()


    def login(self):
        content = open('config.json').read()
        config = json.loads(content)
        result = rh.login(config['email'], config["password"])
        ui.success("Success: Logged In") if result is None or \
            result["detail"] == "logged in using authentication in robinhood.pickle" else ui.error(result)

    def test_purcahse(self):
        print("purchase")
        # purchase a dollar of AAPL
        # view result and determine success credentials
        # use success credentials to update the trade history dict.

        price = 1.0
        symbol = "AAPL"
        #result = rh.order_buy_fractional_by_price(symbol, price, extendedHours=True, timeInForce="gfd")


        current_date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        TradeHistory.update_trade_history(TradeHistory.trade_history, symbol, price, "buy", current_date_time)

        '''if result is not None and 'account' in result.keys():
            ui.success(result)
            # Add to trade history here
            current_date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            TradeHistory.update_trade_history(symbol, price, "buy", current_date_time)

        else:
            ui.error(result)'''


    def trade_on_fear_and_greed(self, investors_are_greedy, investors_are_fearful, trade_history):
        owns_spy = fear_greed.owns_spy()

        if investors_are_greedy and owns_spy:
            # Sell entire SPY position
            result = rh.order_sell_fractional_by_price(fear_greed.symbol,
                                                       fear_greed.get_sell_equity_amount(), extendedHours=True)
            ui.success(result)
        elif investors_are_fearful and not owns_spy:
            # Buy initial SPY investment or the last sold equity
            result = rh.order_buy_fractional_by_price(fear_greed.symbol, fear_greed.
                                                      get_buy_equity_amount(trade_history), extendedHours=True)
            ui.success(result)
        else:
            print("-Skip Trading on Fear-")
