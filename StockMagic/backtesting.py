def backtest_single_stock(bought_on, sold_on, data):
    cost = 0
    number_owned = 0
    for buy_date in bought_on:
        cost += data['close'][buy_date]
        number_owned += 1

    gross = 0
    number_sold = 0
    for sell_date in sold_on:
        gross += data['close'][sell_date]
        number_sold += 1

    realized_profit = gross - cost
    unrealized_profit = realized_profit + (number_owned - number_sold) * data['close'].iloc[-1]

    return unrealized_profit