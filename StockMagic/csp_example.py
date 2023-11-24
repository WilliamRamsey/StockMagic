from alpaca_account import *
from analysis_tools import *
from plotly import graph_objects as go

"""
-Getting stock data-
"""

# Keys for Alpaca API
API_KEY = "PKNZJ7BV3Y133CNN3ZAT"
SEC_KEY = "pqqJpfNpt2RnrTo0q5gXBEMcYxqmvmXit1fzCsyT"

# Gets stock data using alpaca API
account = Alpaca(API_KEY=API_KEY, SEC_KEY=SEC_KEY, paper_account=True, subscribed=True)
df = account.historical_data("QQQ", "Days", bars=365)


"""-Calculating SMA-"""
# Calculates simlple moving average
df["sma20"] = simple_moving_average(df["close"], 20)
df["sma50"] = simple_moving_average(df["close"], 50)
# data["sma50"] = data["close"].rolling(2).mean()
df = df.dropna() 

"""-Visualizing SMA + OHLC stock data-"""
# Gets the timestamps
# Needs real optimization
timestamp_list = []
for i in range(len(df.index.to_list())):
    timestamp_list.append(df.index[i][1])

fig = go.Figure(data=[go.Candlestick(x=timestamp_list,
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close'],
                                     name="QQQ")])
fig.add_trace(go.Scatter(x=timestamp_list, y=df['sma50'], mode='lines', name='sma50'))
fig.add_trace(go.Scatter(x=timestamp_list, y=df['sma20'], mode='lines', name='sma20'))
fig.show()

"""
-Detecting Crossover-
"""

up_indexs, down_indexes = crossover(df["sma20"], df["sma50"])
print("Crossing up:")
for index in up_indexs:
    print(timestamp_list[index])
print("Crossing down:")
for index in down_indexes:
    print(timestamp_list[index])

