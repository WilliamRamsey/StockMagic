from alpaca_account import *
from analysis_tools import *
from backtesting import *
from assets_classes import *

from plotly import graph_objects as go
import pandas as pd
import math

# Keys for Alpaca API
API_KEY = "PKNZJ7BV3Y133CNN3ZAT"
SEC_KEY = "pqqJpfNpt2RnrTo0q5gXBEMcYxqmvmXit1fzCsyT"

# Gets stock data using alpaca API
account = Alpaca(API_KEY=API_KEY, SEC_KEY=SEC_KEY, paper_account=True, subscribed=True)
# print(account.historical_data("QQQ", "Minute", periods=3000)['close'])


print("\n\n\n\n\n\n\n\n\n\n--- StockMagic v.0.0.2 ---\n\n\n\n\n\n\n\n")
to_reccommend = input("Do you want to be notifed of SMA crossovers? (y/n)>")
if to_reccommend == "y":
    to_reccommend = True
    to_graph = input("Would you like to graph the crossovers? (y/n)>")
    if to_graph == "y":
        to_graph = True

to_backtest = input("Do you want to backtest the stragety? (y/n)>")
if to_backtest == "y":
    to_backtest = True
    
# Generates list of stocks in sp500
spx_df = pd.read_csv("StockMagic/spx_data.csv")
ticker_list = spx_df["Symbol"].to_list()

# For backtesting later
realized_gain_percent_list = []
unrealized_gain_percent_list = []
total_gain_percent_list = []
stock_performance_list = []

for ticker in ticker_list:
    """Error Handling"""
    # My s&p spreadsheet is old and some of the symbols for stocks have changed
    # This code handles the exceptions created by requesting a ticker that doesn't exis in the aplaca SDK
    try:
        # Returns a pandas dataframe full of juicy stock data
        df = account.historical_data(ticker, "Hour", periods=5000)
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
            if to_reccommend:
                print(f"{ticker} crossed up at {timestamp_list[index]}. Consider buying at ${df['close'][-1]} for a long position")
            if to_graph:
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
            if to_reccommend:
                print(f"{ticker} crossed down at {timestamp_list[index]}. Consider selling for ${df['close'][-1]}")
            
            # Displays graph
            if to_graph:
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
    if to_backtest:
        # Assumes fractional shares are premitted 
        # Account performance
        initial_principle = 1000
        holdings = []

        for index in up_indexs:
            price = df['close'][index]
            quantity = math.floor(initial_principle / price * 1000000000) / 1000000000
            stock = Holding(ticker=ticker, quantity=quantity, price_at_execution=price)
            holdings.append(stock)

        for index in down_indexes:
            price = df['close'][index]
            quantity = - math.floor(initial_principle / price * 1000000000) / 1000000000
            stock = Holding(ticker=ticker, quantity=quantity, price_at_execution=price)
            holdings.append(stock)

        total_quantiy = 0
        account_cash = initial_principle

        for stock in holdings:
            total_quantiy += stock.quantity
            account_cash -= stock.value_at_execution
    
        outstanding_shares_value = total_quantiy * df['close'][-1]
        account_value = account_cash + outstanding_shares_value
        unrealized_gain_percent = (account_value - initial_principle) / initial_principle * 100

        unrealized_gain_percent_list.append(unrealized_gain_percent)

        # Stock Performance
        price_at_start =    df['close'][0]
        price_at_end = df['close'][-1]
        stock_increase = (price_at_end - price_at_start) / price_at_start * 100
        stock_performance_list.append(stock_increase)
    
        print(f"SMA Crossover Performance: {unrealized_gain_percent}%")
        print(f"Stock Performance: {stock_increase}%")

# Stragety is short happy
if to_backtest:
    print(f"SMA Average: {sum(unrealized_gain_percent_list)/len(unrealized_gain_percent_list)}%")
    print(f"S&P 500 Average: {sum(stock_performance_list)/len(stock_performance_list)}%")
