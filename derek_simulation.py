# Import necessary modules
import profile_class
import main


# # This is commented out because we will be Derek object once, later we load the profile
# derek = profile_class.Profile('derek')
# derek.set_cash(20)  # Load $20 to Derek's profile

derek = profile_class.load_profile_from_pickle('Derek')  # Load Derek object


if derek.get_pending_purchase():  # If I have a pending purchase
    derek.complete_trade()  # Attempt to complete the purchase

if derek.get_pending_sells():  # If I have a pending sell
    derek.complete_sell()  # Attempt to complete the sell

# If Derek is holding a stock and the percentage change is greater than 0.3%, sell the stock
if derek.get_current_stock_holding() is not None and derek.get_current_percentage_change() > 0.3:
    derek.submit_sell()  # Initiates sell

# If Derek is not holding a stock & there are no pending purchases
if derek.get_current_stock_holding() is None and not derek.get_pending_purchase():
    instance_model_performance_stocks = main.build_complete_stock_data()  # Get Ridged first derivative stock data
    # Receive sorted solution
    instance_top_performing_ticker = main.recommend_top_stock(instance_model_performance_stocks)
    cash_balance = derek.get_cash()  # Get current cash balance
    derek.submit_order(instance_top_performing_ticker, cash_balance)  # Initiates purchase

derek.export_trading_df('hi.xlsx')
