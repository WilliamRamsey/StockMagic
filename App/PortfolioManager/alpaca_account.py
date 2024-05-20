from typing import Any
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, OptionBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime as dt

class Alpaca:
    def __init__(self, API_KEY, SEC_KEY, paper_account, subscribed):
        self.API_KEY = API_KEY
        self.SEC_KEY = SEC_KEY
        self.paper_account = paper_account
        self.subscribed = subscribed

        self.market_client = StockHistoricalDataClient(self.API_KEY, self.SEC_KEY)
        self.option_client = OptionHistoricalDataClient(self.API_KEY, self.SEC_KEY)
        self.trading_client = TradingClient(self.API_KEY, self.SEC_KEY, paper=True)
        self.account = self.trading_client.get_account()

        print(self.account.options_approved_level)
        print(self.account.options_trading_level)
        print(self.account.options_buying_power)

    def order(self, symbol, buy, qty):
        if buy:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
        
        order_data = MarketOrderRequest(symbol=symbol, side=side, qty=qty, time_in_force=TimeInForce.GTC)
        market_order = self.trading_client.submit_order(order_data)
        return market_order

    def historical_stock_prices(self, symbol, frequency, start=None, end=None, period=None):
        if period is not None:
            if frequency == "Minute":
                time_dif = period
                frequency = TimeFrame.Minute
            elif frequency == "Hour":
                time_dif = 60 * period
                frequency = TimeFrame.Hour
            else:
                time_dif = 1440 * period
                frequency = TimeFrame.Day

            end = dt.datetime.now()
            start = end - dt.timedelta(minutes=time_dif)
            
        params = StockBarsRequest(symbol_or_symbols=symbol,
                                  timeframe=frequency,
                                  start=start,
                                  end=end)
        return self.market_client.get_stock_bars(params).df
    
    def historical_option_prices(self, symbol, frequency, start=None, end=None, period=None):
        if period is not None:
            if frequency == "Minute":
                time_dif = period
                frequency = TimeFrame.Minute
            elif frequency == "Hour":
                time_dif = 60 * period
                frequency = TimeFrame.Hour
            else:
                time_dif = 1440 * period
                frequency = TimeFrame.Day

            end = dt.datetime.now()
            start = end - dt.timedelta(minutes=time_dif)
            
        params = OptionBarsRequest(symbol_or_symbols=symbol,
                                  timeframe=frequency,
                                  start=start,
                                  end=end)
        return self.market_client.get_stock_bars(params).df


account = Alpaca("PKQFAGYL283JTWQL7G31", "nf73HbHvmUHnx3oSHdQby0hGFagsOWThXU3XRT91", True, True)
print(account.historical_option_prices("scwx", "Day", period=10))
print(account.historical_stock_prices("scwx", "Day", period=10))
