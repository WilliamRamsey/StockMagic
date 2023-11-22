from StockMagic import *

account = Alpaca("PKKYD9REBHS0NIZILM0K", "6YFj01fzxhMT23jH5R8Y7cSmObOUYgfrohQ3NK4D", True, True)
print(account.historical_data("AAPL", "Day", bars=3))