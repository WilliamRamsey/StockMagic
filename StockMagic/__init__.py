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
        params = StockBarsRequest(symbol_or_symbols=symbol,
                                  timeframe=frequency,
                                  start=start,
                                  end=end)
        return self.market_client.get_stock_bars(params).df

class DataBase:
    def __init__(self):
        # Established local directory for storing data
        self.rootdir = os.getcwd()
        if not os.path.exists(self.rootdir + "\\database"):
            os.makedirs(self.rootdir + "\\database")
        if not os.path.exists(self.rootdir + "\\database\\securities"):
            os.makedirs(self.rootdir + "\\database\\securities")
        if not os.path.exists(self.rootdir + "\\database\\datasets"):
            os.makedirs(self.rootdir + "\\database\\datasets")



    def reset(self):
        # Deletes all files in the database
        for dir in os.listdir(self.rootdir + "\\database\\securities"):
            for file in os.listdir(self.rootdir + "\\database\\securities\\" + dir):
                os.remove(f"{self.rootdir}\\database\\securities\\{dir}\\{file}")
            
        for dir in os.listdir(self.rootdir + "\\database\\datasets"):
            for file in os.listdir(self.rootdir + "\\database\\datasets\\" + dir):
                os.remove(f"{self.rootdir}\\database\\datasets\\{dir}\\{file}")

    class Security:
        def __init__(self, data=None, path=None, symbol=None, frequency=None):
            self.rootdir = os.getcwd()

            if data is not None:
                self.data = data
                self.symbol = data.index.to_list()[0][0]
                time1 = data.index.to_list()[0][1]
                time2 = data.index.to_list()[1][1]
                timedelta = time2 - time1
                dif = timedelta.total_seconds() / 60

                if dif == 1:
                    self.frequency = "Minute"
                elif dif == 60:
                    self.frequency = "Hour"
                else:  
                    self.frequency = "Day"
    
                self.datapath = f"{self.rootdir}\\database\\securities\\{self.symbol}"

                if not os.path.exists(self.datapath):
                    os.makedirs(self.datapath)
                if not os.path.exists(f"{self.datapath}\\{self.frequency}"):
                    os.makedirs(f"{self.datapath}\\{self.frequency}")

        """
        def __call__(self):
            return self.data
        """

        def add(self):
            # Write file in /database/{type}/{frequency}/
            # Data will be imputted as dataframe and saved to CSV
            start = self.data.index.to_list()[0][1]
            end = self.data.index.to_list()[-1][1]
            self.time_range = f"{start.strftime('[%Y-%m-%d %H-%M-%S]')} - {end.strftime('[%Y-%m-%d %H-%M-%S]')}"
            path = f"{self.datapath}/{self.frequency}/{self.time_range}.csv"
            print(path)
            self.data.to_csv(path)

        def remove(self):
            # Deletes file in /database/{type}/{frequency}/
            os.remove(self.datapath)
        
        """
        def normalize(self, output_length):
            if len(self.data['close'].to_numpy()) < output_length:
                return None
            else:
                unormalized_data = self.data['close'].to_numpy()[-output_length:]
                normalized_data = (unormalized_data - unormalized_data.min()) / (unormalized_data.max() - unormalized_data.min())
                return normalized_data
        """

    class DataSet:
        pass

account = Alpaca("PKKYD9REBHS0NIZILM0K", "6YFj01fzxhMT23jH5R8Y7cSmObOUYgfrohQ3NK4D", True, True)
# print(account.historical_data("AAPL", "Day", bars=3))
# print(account.order("AAPL", "buy", 1))

base = DataBase()
datapoint = base.Security(data=account.historical_data("AAPL", "Day", bars=10))
# print(datapoint.normalize(3))
datapoint.add()
# base.reset()
