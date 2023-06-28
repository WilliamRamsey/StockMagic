from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime as dt
import tensorflow
import os
import pandas as pd

class Alpaca:
    def __init__(self, API_KEY, SEC_KEY, paper_account, subscribed):
        self.API_KEY = API_KEY
        self.SEC_KEY = SEC_KEY
        self.paper_account = paper_account
        self.subscribed = subscribed

        self.market_client = StockHistoricalDataClient(self.API_KEY, self.SEC_KEY)
        self.trading_client = TradingClient(self.API_KEY, self.SEC_KEY, paper=True)
        self.account = self.trading_client.get_account()
    
    def order(self, symbol, buy, qty):
        if buy:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
        
        order_data = MarketOrderRequest(symbol=symbol, side=side, qty=qty, time_in_force=TimeInForce.GTC)
        market_order = self.trading_client.submit_order(order_data)
        return market_order

    def historical_data(self, symbol, frequency, start=None, end=None, bars=None):
        if bars is not None:
            if frequency == "Minute":
                time_dif = bars
                frequency = TimeFrame.Minute
            elif frequency == "Hour":
                time_dif = 60 * bars
                frequency = TimeFrame.Hour
            else:
                time_dif = 1440 * bars
                frequency = TimeFrame.Day

            end = dt.datetime.now()
            start = end - dt.timedelta(minutes=time_dif)
        print(start.strftime("%Y-%m-%d"))
        params = StockBarsRequest(symbol_or_symbols=symbol,
                                  timeframe=frequency,
                                  start=start,
                                  end=end)
        return self.market_client.get_stock_bars(params).df

account = Alpaca("PKKYD9REBHS0NIZILM0K", "6YFj01fzxhMT23jH5R8Y7cSmObOUYgfrohQ3NK4D", True, True)
print(account.historical_data("AAPL", "Day", bars=3))
# print(account.order("AAPL", "buy", 1))


# Datastructure
# database
# -
class DataBase:
    def __init__(self):
        # Established local directory for storing data
        self.rootdir = os.getcwd()
        if not os.path.exists(self.rootdir + "\\database"):
            os.makedirs(self.rootdir + "\\database")
        if not os.path.exists(self.rootdir + "/database\\raw"):
            os.makedirs(self.rootdir + "\\database\\raw")
        if not os.path.exists(self.rootdir + "\\database\\normalized"):
            os.makedirs(self.rootdir + "\\database\\normalized")
        if not os.path.exists(self.rootdir + "\\database\\raw\\Minute"):
            os.makedirs(self.rootdir + "\\database\\raw\\Minute")
        if not os.path.exists(self.rootdir + "\\database\\raw/Hour"):
            os.makedirs(self.rootdir + "\\database\\raw\\Hour")
        if not os.path.exists(self.rootdir + "\\database\\raw\\Day"):
            os.makedirs(self.rootdir + "\\database\\raw\\Day")
        if not os.path.exists(self.rootdir + "\\database\\normalized\\Minute"):
            os.makedirs(self.rootdir + "\\database\\normalized\\Minute")
        if not os.path.exists(self.rootdir + "\\database\\normalized\\Hour"):
            os.makedirs(self.rootdir + "\\database\\normalized\\Hour")
        if not os.path.exists(self.rootdir + "\\database\\normalized\\Day"):
            os.makedirs(self.rootdir + "\\database\\normalized\\Day")

    def reset_database(self):
        # Deletes all files in the database
        for dir in os.listdir(self.rootdir + "\\database\\raw"):
            for file in os.listdir(self.rootdir + "\\database\\raw\\" + dir):
                open(f"{self.rootdir}\\database\\raw\\{dir}\\{file}", "w").close()
            
        for dir in os.listdir(self.rootdir + "\\database\\normalized"):
            for file in os.listdir(self.rootdir + "\\database\\normalized\\" + dir):
                open(f"{self.rootdir}\\database\\normalized\\{dir}\\{file}", "w").close()

    def add_entry(self, data, symbol, frequency, normalized=False):
        # Write file in /database/{type}/{frequency}/
        # Data will be imputted as dataframe and saved to CSV
        if normalized:
            data.to_csv(f"{self.rootdir}\\database\\normalized\\{frequency}\\{symbol}.csv")
        else:
            data.to_csv(f"{self.rootdir}\\database\\raw\\{frequency}\\{symbol}.csv")

base = DataBase()
base.reset_database()
base.add_entry(account.historical_data("AAPL", "Minute", bars=3), "AAPL", "Minute", normalized=False)
