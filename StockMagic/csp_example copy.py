from alpaca_account import *
from analysis_tools import *
from plotly import graph_objects as go
import pandas as pd
from backtesting import *

# Keys for Alpaca API
API_KEY = "PKNZJ7BV3Y133CNN3ZAT"
SEC_KEY = "pqqJpfNpt2RnrTo0q5gXBEMcYxqmvmXit1fzCsyT"

# Gets stock data using alpaca API
account = Alpaca(API_KEY=API_KEY, SEC_KEY=SEC_KEY, paper_account=True, subscribed=True)
df = account.historical_data("QQQ", "Days", period=365)

# Generates list of stocks in sp500
spx_df = pd.read_csv("StockMagic/spx_data.csv")
ticker_list = spx_df["Symbol"].to_list()

for ticker in ticker_list:

    """Error Handling"""
    # My s&p spreadsheet is old and some of the symbols for stocks have changed
    # This code handles the exceptions created by requesting a ticker that doesn't exis in the aplaca SDK
    try:
        # Returns a pandas dataframe full of juicy stock data
        df = account.historical_data(ticker, "Days", period=365)
    except AttributeError:
        print(f"{ticker} not found")
        continue
    
    """Getting SMA"""
    # Custom SMA function built in pandas
    df["sma20"] = simple_moving_average(df["close"], 20)
    df["sma50"] = simple_moving_average(df["close"], 50)
    # SMA returns NaN values for the length of the period at the start of each column
    df = df.dropna() 

    """Getting index"""
    # Gets timestamps in accessable list
    # This code could be written more elegantly
    timestamp_list = []
    for i in range(len(df.index.to_list())):
        timestamp_list.append(df.index[i][1])

    """Finding Crossovers"""
    # Function returns tuple of two lists containing the index of the crossover as an int 
    up_indexs, down_indexes = crossover(df["sma20"], df["sma50"])

    for index in up_indexs:
        """Determining if crossup is recent"""
        # If a stock crossed over during the last frequency
        if index == len(timestamp_list) - 1:
            # Notifies for crossover
            print(f"{ticker} crossed up at {timestamp_list[index]}. Consider buying at ${df['close'][-1]} for a long position")
            
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
        """Determining if crossdown is recent"""
        if index == len(timestamp_list) - 1:
            # Notifies for crossover
            print(f"{ticker} crossed down at {timestamp_list[index]}. Consider selling for ${df['close'][-1]}")
            
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

    """Backtesting"""
    print(ticker)
    try:
        print(backtest_single_stock(up_indexs, down_indexes, df))
    except IndexError:
        continue