import click, ui, json
import robin_stocks as rh


@click.group()
def main():
    print("-Starting Friar Tuck-")
    content = open('config.json').read()
    config = json.loads(content)
    rh.login(config['email'], config["password"])


@main.command(help="Gets a stock quote for one or more symbols")
@click.argument('symbols', nargs=-1)
def quote(symbols):
    for symbol in symbols:
        print("Getting stock quote for: {}".format(symbol))
    quotes = rh.get_quotes(symbols)
    for stock_quote in quotes:
        print("{} | {}".format(stock_quote["symbol"], stock_quote["ask_price"]))


@main.command(help="View quotes for all stocks in your watchlist")
def watchlist():
    with open('watchlist') as file:
        symbols = file.read().split()
        quotes = rh.get_quotes(symbols)
        for stock_quote in quotes:
            print("{} | {}".format(stock_quote["symbol"], stock_quote["ask_price"]))


@main.command(help="Buy a given quantity of stocks")
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def buy(quantity, symbol, limit):
    if limit is not None:
        ui.success("Buying {} quantity of {} at {}".format(quantity, symbol, limit))
        result = rh.order_buy_limit(symbol, quantity, limit)
    else:
        ui.success("Buying {} quantity of {} at market price".format(quantity, symbol))
        result = rh.order_buy_market(symbol, quantity)
    ui.success(result)


@main.command(help="Sell a given quantity of stocks")
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def sell(quantity, symbol, limit):
    if limit is not None:
        ui.success("Selling {} quantity of {} at {}".format(quantity, symbol, limit))
        result = rh.order_buy_limit(symbol, quantity, limit)
    else:
        ui.success("Selling {} quantity of {} at market price".format(quantity, symbol))
        result = rh.order_sell_market(symbol, quantity)
    ui.success(result)


if __name__ == '__main__':
    main()
