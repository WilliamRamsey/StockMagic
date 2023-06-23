from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca_trade_api import REST, TimeFrame
import datetime as dt

class Alpaca:
    def __init__(self, API_KEY, SEC_KEY, paper_account, subscribed):
        self.API_KEY = API_KEY
        self.SEC_KEY = SEC_KEY
        self.paper_account = paper_account
        self.subscribed = subscribed

        self.api = REST(key_id = API_KEY, secret_key = SEC_KEY)
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

        return(self.api.get_bars(symbol, frequency, start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y"), adjustment='raw').df)


account = Alpaca("PKKYD9REBHS0NIZILM0K", "6YFj01fzxhMT23jH5R8Y7cSmObOUYgfrohQ3NK4D", True, True)
print(account.historical_data("AAPL", "Day", bars=12))
# print(account.order("AAPL", "buy", 1))

