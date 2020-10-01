import json
import robin_stocks as rh
import ui
import fear_greed

# TODO Make client a class and initialize vars
# TODO Populate trade history
# TODO Deploy in cloud
# held_positions = {}


def login():
    content = open('config.json').read()
    config = json.loads(content)
    rh.login(config['email'], config["password"])


def get_held_positions():
    return rh.build_holdings()


def trade_on_fear_and_greed(investors_are_greedy, investors_are_fearful, trade_history):
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
