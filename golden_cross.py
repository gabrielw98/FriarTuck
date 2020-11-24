# Get all s & p 500 indexes into an array
# Get current holdings
# For holdings I dont contain, check for the golden

# If the 50 SMA crosses over the 200 SMA and the crossover candle is above the 200 SMA: buy signal
# If the 50 SMA crosses below the 200 SMA and the crossover candle is below the 200 SMA: sell signal


def get_spy_tickers():
    file = open("spy_tickers.txt", "r")
    tickers = file.read().split('\n')
    return tickers