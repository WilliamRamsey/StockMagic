# alpaca imports
from typing import Any
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# tensorflow and data regression imports
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
# misc imports
import datetime as dt
import os


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

        def __call__(self):
            return self.data
        
        def __len__(self):
            return len(self.data)

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
        
        pass
    
    class Dataset:
        def __init__(self, forsee_len, frequency, start=None, end=None, bars=None):
            self.forsee_len = forsee_len
            self.frequency = frequency
            self.start = start
            self.end = end
            self.bars = bars
            self.annotations = {"labels":[], "data":[]}

        def __call__(self):
            return self.annotations
            
        def add_stock(self, data):
            # Normalization and annotation built in
            raw = data['close'].to_numpy()
            normalized = []
            for datapoint in raw:
                normalized_datapoint = (datapoint - raw.min()) / (raw.max() - raw.min())
                normalized.append(normalized_datapoint)
            start_data = normalized[:-self.forsee_len]
            end_data = normalized[-self.forsee_len:]
            label = (max(end_data), min(end_data))
            self.annotations["labels"].append(label)
            self.annotations["data"].append(start_data)


account = Alpaca("PKKYD9REBHS0NIZILM0K", "6YFj01fzxhMT23jH5R8Y7cSmObOUYgfrohQ3NK4D", True, True)

base = DataBase()

train_dataset = base.Dataset(forsee_len=10, frequency="Minute", bars=31)
test_dataset = base.Dataset(forsee_len=10, frequency="Minute", bars=31)

symbols = ['QQQ', 'SPY', 'AAPL', 'ABNB', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'ALGN', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'AZN', 'BIDU', 'BIIB', 'BKNG', 'CDNS', 'CEG', 'CMCSA', 'COST', 'CPRT', 'CRWD', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'DDOG', 'DLTR', 'DOCU', 'DXCM', 'EA', 'EBAY', 'EXC', 'FAST', 'META', 'FISV', 'FTNT', 'GILD', 'GOOG', 'GOOGL', 'HON', 'ILMN', 'INTC', 'INTU', 'ISRG', 'JD', 'KDP', 'KHC', 'KLAC', 'LCID', 'LRCX', 'LULU', 'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MRNA', 'MRVL', 'MSFT', 'MTCH', 'MU', 'NFLX', 'NTES', 'NVDA', 'NXPI', 'ODFL', 'OKTA', 'ORLY', 'PANW', 'PAYX', 'PCAR', 'PDD', 'PEP', 'PYPL', 'QCOM', 'REGN', 'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SPLK', 'SWKS', 'TEAM', 'TMUS', 'TLSA', 'TXN', 'VRSK', 'VRSN', 'VRTX', 'WBA', 'WDAY', 'XEL', 'ZM', 'ZS']

for symbol in symbols[:60]:
    stock = account.historical_data(symbol, "Day", bars=50).tail(31)
    if len(stock) == 31:
        train_dataset.add_stock(stock)

for symbol in symbols[60:]:
    stock = account.historical_data(symbol, "Day", bars=50).tail(31)
    if len(stock) == 31:
        test_dataset.add_stock(stock)


# Generates train data
tf_train = tf.data.Dataset.from_tensor_slices((train_dataset.annotations['data'], train_dataset.annotations['labels']))
tf_train = tf_train.shuffle(buffer_size=len(tf_train))
tf_train = tf_train.cache()
tf_train = tf_train.prefetch(tf.data.experimental.AUTOTUNE)

# Generates test data
tf_test = tf.data.Dataset.from_tensor_slices((test_dataset.annotations['data'], test_dataset.annotations['labels']))
tf_test = tf_test.shuffle(buffer_size=len(tf_test))
tf_test = tf_test.cache()
tf_test = tf_test.prefetch(tf.data.experimental.AUTOTUNE)


# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# print(x_train[0], y_train[0])


model = tf.keras.Sequential([
    tf.keras.Input((21, 1), name="feature"),
    tf.keras.layers.Dense(21),
    tf.keras.layers.Dense(21, activation="relu"),
    tf.keras.layers.Dense(2)
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'], loss='mse')
model.summary()

# Train model'])
model.fit(tf_train, epochs=10, validation_data=tf_test)


# Make predictions
