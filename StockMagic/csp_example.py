from alpaca_account import *
from analysis_tools import *
from plotly import graph_objects as go
import pandas as pd


"""
---SMA Crossover---
"""

"""
-Getting stock data-
"""

# Keys for Alpaca API
API_KEY = "PKNZJ7BV3Y133CNN3ZAT"
SEC_KEY = "pqqJpfNpt2RnrTo0q5gXBEMcYxqmvmXit1fzCsyT"

# Gets stock data using alpaca API
account = Alpaca(API_KEY=API_KEY, SEC_KEY=SEC_KEY, paper_account=True, subscribed=True)
df = account.historical_data("QQQ", "Days", period=365)


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


"""
-For each stock in S&P 500-
"""
spx_df = pd.read_csv("StockMagic/spx_data.csv")
ticker_list = spx_df["Symbol"].to_list()

for ticker in ticker_list:

    # My s&p spreadsheet is old and some of the symbols for stocks have changed
    # This code handles the exceptions created by requesting a ticker that doesn't exis in the aplaca SDK
    try:
        df = account.historical_data(ticker, "Days", period=365)
    except AttributeError:
        print(f"{ticker} not found")
        continue

    df["sma20"] = simple_moving_average(df["close"], 20)
    df["sma50"] = simple_moving_average(df["close"], 50)
    df = df.dropna() 

    # Gets the timestamps
    # Needs real optimization
    timestamp_list = []
    for i in range(len(df.index.to_list())):
        timestamp_list.append(df.index[i][1])

    up_indexs, down_indexes = crossover(df["sma20"], df["sma50"])

    for index in up_indexs:
        # If a stock crossed over during the last frequency
        if index == len(timestamp_list) - 1:
            # Notifies for crossover
            print(f"{ticker} crossed up. Consider buying at ${df['close'][-1]} for a long position")
            
            # Displays graph
            fig = go.Figure(data=[go.Candlestick(x=timestamp_list,
                                                 open=df['open'],
                                                 high=df['high'],
                                                 low=df['low'],
                                                 close=df['close'],
                                                 name=ticker)])
            fig.add_trace(go.Scatter(x=timestamp_list, y=df['sma50'], mode='lines', name='sma50'))
            fig.add_trace(go.Scatter(x=timestamp_list, y=df['sma20'], mode='lines', name='sma20'))
            fig.show()


    for index in down_indexes:
        if index == len(timestamp_list) - 1:
            # Notifies for crossover
            print(f"{ticker} crossed down. Consider selling for ${df['close'][-1]}")
                
            # Displays graph
            fig = go.Figure(data=[go.Candlestick(x=timestamp_list,
                                                 open=df['open'],
                                                 high=df['high'],
                                                 low=df['low'],
                                                 close=df['close'],
                                                 name=ticker)])
            fig.add_trace(go.Scatter(x=timestamp_list, y=df['sma50'], mode='lines', name='sma50'))
            fig.add_trace(go.Scatter(x=timestamp_list, y=df['sma20'], mode='lines', name='sma20'))
            fig.show()          
