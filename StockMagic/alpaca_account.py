from typing import Any
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

import datetime as dt
import math

from assets_classes import *

class Alpaca:
    def __init__(self, API_KEY, SEC_KEY, paper_account, subscribed, positions=[]):
        self.API_KEY = API_KEY
        self.SEC_KEY = SEC_KEY
        self.paper_account = paper_account
        self.subscribed = subscribed
        self.positions = positions

        self.market_client = StockHistoricalDataClient(self.API_KEY, self.SEC_KEY)
        self.trading_client = TradingClient(self.API_KEY, self.SEC_KEY, paper=True)
        self.account = self.trading_client.get_account()
    
    def market_order_shares(self, symbol, buy, qty):
        if buy:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
        
        order_data = MarketOrderRequest(symbol=symbol, side=side, qty=qty, time_in_force=TimeInForce.GTC)
        market_order = self.trading_client.submit_order(order_data)
        return market_order
    
    def market_order_dollars(self, symbol, buy, cost):
        qty = math.floor(self.historical_data(symbol, "Minute", periods=1).iloc[-1]["close"] / cost, 9)
        self.market_order_shares(symbol, buy, qty)

    def historical_data(self, symbol, frequency, start=None, end=None, periods=None):
        if periods is not None:
            if frequency == "Minute":
                time_dif = periods
                frequency = TimeFrame.Minute
            elif frequency == "Hour":
                time_dif = 60 * periods
                frequency = TimeFrame.Hour
            else:
                time_dif = 1440 * periods
                frequency = TimeFrame.Day

            end = dt.datetime.now()
            start = end - dt.timedelta(minutes=time_dif)
            
        params = StockBarsRequest(symbol_or_symbols=symbol,
                                  timeframe=frequency,
                                  start=start,
                                  end=end)
        return self.market_client.get_stock_bars(params).df

