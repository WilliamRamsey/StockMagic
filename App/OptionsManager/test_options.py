# 

# net_profit(strike price) = 
# if strike price >= execution price:
#   premium(strike price) + strike price - stock purchase price - broker fee
# if strike price < execution price:
#   premium(stike price) + stock price at expiration - stock purchase price - broker fee

def profit(strike_price):
    
    if execution_price >= strike_price:
        
