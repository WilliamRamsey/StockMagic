from alpaca_account import *


API_KEY = "PKNZJ7BV3Y133CNN3ZAT"
SEC_KEY = "pqqJpfNpt2RnrTo0q5gXBEMcYxqmvmXit1fzCsyT"

account = Alpaca(API_KEY=API_KEY, SEC_KEY=SEC_KEY, paper_account=True, subscribed=True)
data = account.historical_data("QQQ", "Hour", bars=20)

print(data['close'])
