import json
import robin_stocks as rh
import ui
import fear_greed

# *Make client a class and initialize vars
# TODO Populate trade history
# TODO Deploy in cloud


class Client:

    held_positions = {}

    def __init__(self):
        # Log into the client
        self.login()

        # Set get the held positions of the client's portfolio
        Client.held_positions = rh.build_holdings()


    def login(self):
        content = open('config.json').read()
        config = json.loads(content)
        result = rh.login(config['email'], config["password"])
        ui.success("Success: Logged In") if result is None or \
            result["detail"] == "logged in using authentication in robinhood.pickle" else ui.error(result)


    def trade_on_fear_and_greed(self, investors_are_greedy, investors_are_fearful, trade_history):
        owns_spy = fear_greed.owns_spy()

        if investors_are_greedy and owns_spy:
            # Sell entire SPY position
            result = rh.order_sell_fractional_by_price(fear_greed.symbol,
                                                       fear_greed.get_sell_equity_amount(), extendedHours=True)
            ui.success(result)
        elif investors_are_fearful and not owns_spy:
            # Buy initial SPY investment or the last sold equity
            result = rh.order_buy_fractional_by_price(fear_greed.symbol,
                                                      fear_greed.get_buy_equity_amount(trade_history), extendedHours=True)
            ui.success(result)
        else:
            print("-Skip Trading on Fear-")
