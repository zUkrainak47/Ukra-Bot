from stockdex import Ticker

ticker = Ticker(ticker="AAPL")
print(ticker.yahoo_api_price()['close'].iloc[-1])
