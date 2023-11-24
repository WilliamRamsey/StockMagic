from alpaca_account import *
from analysis_tools import *

API_KEY = "PKNZJ7BV3Y133CNN3ZAT"
SEC_KEY = "pqqJpfNpt2RnrTo0q5gXBEMcYxqmvmXit1fzCsyT"

account = Alpaca(API_KEY=API_KEY, SEC_KEY=SEC_KEY, paper_account=True, subscribed=True)
data = account.historical_data("QQQ", "Days", bars=365)
# data["close"]

data["sma20"] = simple_moving_average(data["close"], 20)
data["sma50"] = simple_moving_average(data["close"], 50)
# data["sma50"] = data["close"].rolling(2).mean()
data = data.dropna() 


# print(len(data["sma20"]))
# print(len(data["sma50"]))
# crossover(data["sma20"], data["sma50"])
