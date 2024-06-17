from typing import Any
from alpaca.trading.client import TradingClient, GetAssetsRequest
from alpaca.trading.requests import MarketOrderRequest, GetOptionContractsRequest, LimitOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, AssetStatus, ContractType, QueryOrderStatus
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.historical.option import OptionHistoricalDataClient, OptionLatestQuoteRequest
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

    def order(self, symbol, buy, qty):
        if buy:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
        
        order_data = MarketOrderRequest(symbol=symbol, side=side, qty=qty, time_in_force=TimeInForce.GTC)
        market_order = self.trading_client.submit_order(order_data)
        return market_order
    
    def options_request(self, symbol, min_strike, max_strike=None, limit=None, experation_date=None, min_expiration=None, max_expiration=None):
        if max_strike is not None:
            max_strike = str(max_strike)
        min_strike = str(min_strike)

        experation_date = dt.datetime.strptime(experation_date, "%Y-%m-%d")
        print(experation_date.date())
        
        req = GetOptionContractsRequest(
            underlying_symbols = [symbol],
            status = AssetStatus.ACTIVE,
            expiration_date = experation_date, # Pass datetime object or string (yyyy-mm-dd)
            # For range of experiations
            expiration_date_gte = min_expiration,
            expiration_date_lte = max_expiration,
            root_symbol = symbol,
            type = ContractType.CALL,
            style = None,
            strike_price_gte = min_strike,
            strike_price_lte= max_strike,
            limit = limit,
            page_token = None
        )

        res = self.trading_client.get_option_contract(req)
        print(res.option_contract)

    def buy_put(self):
        pass

    def buy_call(self):
        pass

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


account = Alpaca("PKQFAGYL283JTWQL7G31", "nf73HbHvmUHnx3oSHdQby0hGFagsOWThXU3XRT91", True, True)
account.options_request("AAPL", min_strike = 200, experation_date = "2025-05-22", max_strike = 250)
