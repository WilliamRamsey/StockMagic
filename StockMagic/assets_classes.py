class Holding:
    def __init__(self, ticker=None, quantity=None, price_at_execution=None):
        self.ticker = ticker
        self.quantity = quantity
        self.price_at_execution = price_at_execution
        self.value_at_execution = quantity * price_at_execution
        
class Position:
    def __init__(self, holdings):
        pass