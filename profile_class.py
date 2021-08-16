# Import necessary modules
import pickle
from datetime import datetime
import pandas as pd
import yfinance as yf
from numpy import nan


class Profile:
    """Class that creates investing profiles. Each object will have cash, invested capital, capital gains, pending
    trades, & pending sells. The cash is liquid cash available for investing. Invested capital is capital illiquid
    assets tied up in stocks. Capital gains is a running tracking that tracks total gains. Pending trades & sells
    records a boolean value that logs if a trade/sell is initiated."""

    def __init__(self, first_name):
        self.first_name = first_name
        self.cash = 0
        self.invested_capital = 0
        self.capital_gains = 0
        self.pending_purchase = False
        self.pending_sells = False
        self.current_stock_holding = None
        self.current_stock_purchase_price = None
        self.current_percentage_change = None
        self.current_number_of_shares = None
        self.trading_history = pd.DataFrame({'Stock Ticker': [],
                                             'Buy Invested Amount': [],
                                             'Buy Submission Time': [],
                                             'Buy Completed Time': [],
                                             'Completed Order Price': [],
                                             'Shares Holding': [],
                                             'Sell Order Time': [],
                                             'Sell Completed Time': [],
                                             'Profit': []})
        self.dump_profile_to_pickle()  # Save changes to profile
        
    def __str__(self):
        cash = self.get_cash()
        invested_capital = self.get_invested_capital()
        capital_gains = self.get_capital_gains()
        pending_purchase = self.get_pending_purchase()
        pending_sells = self.get_pending_sells()
        current_stock_holding = self.get_current_stock_holding()
        current_stock_purchase_price = self.get_current_stock_purchase_price()
        current_percentage_change = self.get_current_percentage_change()
        current_number_of_shares = self.get_current_number_of_shares()
        
        tuple_print_list = [('Cash: $', round(cash, 2)), ('Invested Capital: $', round(invested_capital, 2)), ('Pending Purchase: ', pending_purchase),
                            ('Pending Sell: ', pending_sells), ('Current Stock Holding: ', current_stock_holding),
                            ('Current Stock Purchase Price: $', round(current_stock_purchase_price, 2)), ('Current Percentage Change: ', round(current_percentage_change, 2)),
                            ('Current Number of Shares: ', round(current_number_of_shares, 2))]
        output_string = ''
        
        for instance in tuple_print_list:
            instance_string = instance[0] + str(instance[1]) + '\n'
            output_string += instance_string
        
        return output_string

    def set_cash(self, new_balance):
        """
        Method that sets the attribute self.cash, it will return the attribute if successful
        :param new_balance: float
        :rtype: float
        """
        self.cash = new_balance
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.cash

    def set_invested_capital(self, new_invested_capital):
        """
        Method that sets the attribute self.invested_capital, it will return the attribute if successful
        :param new_invested_capital: float
        :rtype: float
        """
        self.invested_capital = new_invested_capital
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.invested_capital

    def set_capital_gains(self, new_capital_gains):
        """
        Method that sets the attribute self.new_capital_gains, it will return the attribute if successful
        :param new_capital_gains: float
        :rtype: float
        """
        self.capital_gains = new_capital_gains
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.capital_gains

    def set_pending_purchase(self, boolean):
        """
        Method that sets the attribute self.pending_purchase, it will return the attribute if successful
        :param boolean: bool
        :rtype: bool
        """
        self.pending_purchase = boolean
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.pending_purchase

    def set_pending_sells(self, boolean):
        """
        Method that sets the attribute self.pending_sells, it will return the attribute if successful
        :param boolean: bool
        :rtype: bool
        """
        self.pending_sells = boolean
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.pending_sells

    def set_current_stock_holding(self, stock_ticker):
        """
        Method that sets the attribute self.current_stock_holding, it will return the attribute if successful
        :param stock_ticker: string
        :rtype: bool
        """
        self.current_stock_holding = stock_ticker
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.current_stock_holding

    def set_current_stock_purchase_price(self, current_stock_price):
        """
        Method that sets the attribute self.current_stock_purchase_price, it will return the attribute if successful
        :param current_stock_price: float
        :rtype: float
        """
        self.current_stock_purchase_price = current_stock_price
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.current_stock_purchase_price

    def set_current_percentage_change(self, percent_change):
        """
        Method that sets the attribute self.current_percent_change, it will return the attribute if successful
        :param percent_change: float
        :rtype: float
        """
        self.current_percentage_change = percent_change
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.current_percentage_change

    def set_current_number_of_shares(self, current_number_of_shares):
        """
        Method that sets the attribute self.current_number_of_shares, it will return the attribute if successful
        :param current_number_of_shares: float
        :rtype: float
        """
        self.current_number_of_shares = current_number_of_shares
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.current_number_of_shares

    def add_cash(self, to_add_cash):
        """
        Method that increases the attribute self.cash by the amount defined, returns the attribute if successful
        :param to_add_cash: float
        :rtype: float
        """
        self.cash += to_add_cash
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.cash

    def add_invested_capital(self, to_add_invested_capital):
        """
        Increases the attribute self.invested_capital by the amount defined,if successful return attribute
        :param to_add_invested_capital: float
        :rtype: float
        """
        self.invested_capital += to_add_invested_capital
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.cash

    def add_capital_gains(self, to_add_capital_gains):
        """
        Increases the attribute self.capital_gains by the amount defined, if successful return attribute
        :param to_add_capital_gains: float
        :rtype: float
        """
        self.capital_gains += to_add_capital_gains
        self.dump_profile_to_pickle()  # Save changes to profile
        return self.capital_gains

    def get_cash(self):
        """
        Returns the attribute self.cash
        :rtype: float
        """
        return self.cash

    def get_invested_capital(self):
        """
        Returns the attribute self.invested_capital
        :rtype: float
        """
        return self.invested_capital

    def get_capital_gains(self):
        """
        Returns the attribute self.capital_gains
        :rtype: float
        """
        return self.capital_gains

    def get_pending_purchase(self):
        """
        Returns the attribute self.pending_purchase
        :rtype: bool
        """
        return self.pending_purchase

    def get_pending_sells(self):
        """
        Returns the attribute self.pending_sells
        :rtype: bool
        """
        return self.pending_sells

    def get_current_stock_holding(self):
        """
        Returns the attribute self.current_stock_holding
        :rtype: string
        """
        return self.current_stock_holding

    def get_current_stock_purchase_price(self):
        """
        Returns the attribute self.current_stock_purchase_price
        :rtype: float
        """
        return self.current_stock_purchase_price

    def get_current_percentage_change(self):
        """
        Returns the attribute self.current_percentage_change
        :rtype: float
        """
        return self.current_percentage_change

    def get_trading_history(self):
        """
        Returns the attribute self.trading_history
        :rtype: pandas dataframe
        """
        return self.trading_history

    def get_current_number_of_shares(self):
        """
        Returns the attribute self.current_number_of_shares
        :rtype: float
        """
        return self.current_number_of_shares

    def submit_order(self, stock_symbol, invested_capital):
        """Method that submits order for a stock. The trade is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & add a record with the stock symbol,
        invested capital, & purchase time stamp."""
        purchase_timestamp = datetime.now()  # Obtain currant time that trade was initiated

        if self.get_cash() >= invested_capital:  # If we have sufficient cash to initiate the trade
            # We create a half empty record
            instance = pd.Series([stock_symbol, invested_capital, purchase_timestamp,
                                  nan, nan, nan, nan, nan, nan],
                                 index=['Stock Ticker', 'Buy Invested Amount', 'Buy Submission Time',
                                        'Buy Completed Time', 'Completed Order Price', 'Shares Holding',
                                        'Sell Order Time', 'Sell Completed Time', 'Profit'])
            # Append the new record to the global dataframe
            self.trading_history = self.trading_history.append(instance, ignore_index=True)
            self.set_pending_purchase(True)  # Set the pending trade attribute to true
            self.dump_profile_to_pickle()  # Save changes to profile
            return True  # Return true if successful
        else:  # We did not have enough cash to initiate the trade
            print(r'You do not have enough cash to initiate the trade.')  # Print error out
            self.dump_profile_to_pickle()  # Save changes to profile
            return False  # Return false

    def complete_trade(self):
        """Method that completes order for a stock. The trade is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & update a record with the buy completed order
        time, completed order price, & shares holding. Additionally, only one stock can be bought a time, so we
        will use the the dataframe index strategy to update the rows. We will filter for the opening by the Buy
        Completed Time, then retrieve that row index & update the values."""
        # Obtain the row index that the incomplete order exists on
        pending_trade_index = self.trading_history.index[self.trading_history['Buy Completed Time'].isnull()].tolist()
        # If there are pending trades & a row exists for completion
        if self.get_pending_purchase() and pending_trade_index is not None:
            # Obtain the stock ticker at that row index. Values will return a list, so we use 0 index for the value
            pending_stock = self.trading_history.iloc[pending_trade_index]['Stock Ticker'].values[0]
            # Obtain the invested amount at that row index. Values will return a list, so we use 0 index for the value
            invested_capital = self.trading_history.iloc[pending_trade_index]['Buy Invested Amount'].values[0]
            current_stock_price = get_stock_price(pending_stock)  # A function that obtains the current stock price
            # Obtain the buy time at that row index. Values will return a list, so we use 0 index for the value
            buy_time = self.trading_history.iloc[pending_trade_index]['Buy Submission Time'].values[0]
            current_time = pd.Timestamp.now()  # Get the current time with the pandas method
            elapsed_time = (current_time - buy_time).total_seconds()  # Delta time for elapsed time in seconds

            if elapsed_time > 60 * 10:  # If it has been ten minutes since purchase initiation
                shares_holding = invested_capital / current_stock_price  # Calculate shares holding
                self.trading_history.at[pending_trade_index, 'Buy Completed Time'] = current_time  # Add completed time
                # Insert Completed Order Price
                self.trading_history.at[pending_trade_index, 'Completed Order Price'] = current_stock_price
                # Shares holding is invested capital divided by current stock price, insert into record
                self.trading_history.at[pending_trade_index, 'Shares Holding'] = shares_holding
                self.add_cash(-invested_capital)  # Adjust cash balance for the trade
                self.set_invested_capital(invested_capital)  # Set the transaction as the attribute
                self.set_pending_purchase(False)  # Change attribute to close pending trade
                self.set_current_stock_holding(pending_stock)  # Set the attribute to the current stock
                self.set_current_stock_purchase_price(current_stock_price)  # Set the attribute as the purchase price
                self.set_current_number_of_shares(shares_holding)  # Set the current number of shares holding
                self.dump_profile_to_pickle()  # Save changes to profile
                return True  # Return true, it was successful
        else:  # No trades pending
            self.dump_profile_to_pickle()  # Save changes to profile
            return False  # Return false

    def submit_sell(self):
        """Method that submits sell order for a stock. The sell is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & update a record with the stock symbol,
        invested capital, & purchase time stamp. Additionally, only one stock can be bought a time, so we will use
        the dataframe index strategy to update the rows. We will filter for the opening by the Sell Completed Time,
        then retrieve that row index &  update the values."""
        # If there is an active trade, there will be only one, we want to sell that stock
        pending_trade_index = self.trading_history.index[self.trading_history['Sell Order Time'].isnull()].tolist()
        # If we have a completed trade that is not sold
        if (not self.get_pending_sells()) and (pending_trade_index is not None):
            current_time = pd.Timestamp.now()  # Obtain the current timestamp with pandas method
            self.trading_history.at[pending_trade_index, 'Sell Order Time'] = current_time  # Update the record
            self.set_pending_sells(True)  # Set the attribute to true
            self.dump_profile_to_pickle()  # Save changes to profile
            return True  # Return true for success
        else:  # We already have a pending trade
            self.dump_profile_to_pickle()  # Save changes to profile
            return False  # Return false

    def complete_sell(self):
        """Method that completes sell order for a stock. The trade is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & update a record with the sell order time &
        profit. Additionally, only one stock can be bought a time, so we will use the dataframe index strategy to
        update the rows. We will filter for the opening by the Sell Completed Time, then retrieve that row index &
        update the values."""

        # If there is an active trade, there will be only one, we want to sell that stock
        pending_trade_index = self.trading_history.index[self.trading_history['Sell Completed Time'].isnull()].tolist()
        print(pending_trade_index)
        if self.get_pending_sells() and pending_trade_index != []:
            # Obtain the stock ticker at that row index. Values will return a list, so we use 0 index for the value
            pending_stock = self.trading_history.iloc[pending_trade_index]['Stock Ticker'].values[0]
            # Obtain the invested capital at that row index. Values will return a list, so we use 0 index for the value
            invested_capital = self.trading_history.iloc[pending_trade_index]['Buy Invested Amount'].values[0]
            # Obtain the shares holding at that row index. Values will return a list, so we use 0 index for the value
            shares_holding = self.trading_history.iloc[pending_trade_index]['Shares Holding'].values[0]
            current_stock_price = get_stock_price(pending_stock)  # A function that obtains the current stock price
            capital_yield = current_stock_price * shares_holding  # Calculates total active capital in stock
            net_capital_gain = capital_yield - invested_capital  # Calculates delta, which is net capital gain
            # Obtain the sell order time at that row index. Values will return a list, so we use 0 index for the value
            sell_time = self.trading_history.iloc[pending_trade_index]['Sell Order Time'].values[0]
            current_time = pd.Timestamp.now()  # Retrieve current time with pandas method
            elapsed_time = (current_time - sell_time).total_seconds()  # Calculate elapsed time in seconds
            if elapsed_time > 60 * 10:  # If it has been ten minutes since purchase initiation
                # Insert Sell Completed Time
                self.trading_history.at[pending_trade_index, 'Sell Completed Time'] = current_time
                self.trading_history.at[pending_trade_index, 'Profit'] = net_capital_gain  # Insert Profit
                self.add_cash(capital_yield)  # Add the capital yield to the cash balance
                self.set_invested_capital(0)  # Set invested capital to 0
                self.add_capital_gains(net_capital_gain)  # Add the net capital gains to the existing capital gains
                self.set_pending_sells(False)  # Set pending sells to false, because we closed this transaction
                self.set_current_stock_holding(None)  # We are currently holding no stocks
                self.set_current_stock_purchase_price(None)  # Set the current stock purchase price to none
                self.set_current_percentage_change(None)  # Set the current stock percentage change to none
                self.set_current_number_of_shares(None)  # Set the current number of shares holding
                self.dump_profile_to_pickle()  # Save changes to profile
                return True  # Return true
        else:  # No pending sells for completion
            self.dump_profile_to_pickle()  # Save changes to profile
            return False  # Return false

    def calculate_current_percentage(self):
        """A method that calculates the current percent change of the stock holding. The method gets the purchase level
        of stock, then retrieves the current price level of the stock; lastly, it calculate percentage change."""
        current_stock = self.get_current_stock_holding()  # Get the current stock you're holding
        percentage_change = None  # Unresolved attribute reference solved
        if current_stock is not None:  # If we are holding a stock
            purchase_stock_level = self.get_current_stock_purchase_price()  # Get initial purchase price of stock
            current_stock_price = get_stock_price(self.get_current_stock_holding())  # Get current stock price of stock
            percentage_change = ((current_stock_price - purchase_stock_level)/purchase_stock_level) * 100  # pct change
            self.set_current_percentage_change(percentage_change)
            self.dump_profile_to_pickle()  # Save changes to profile
        return percentage_change

    def dump_profile_to_pickle(self):
        """Saves profile to pickle file for recovery"""
        with open(self.first_name + '.pkl', 'wb') as file:  # Open the pickle file
            pickle.dump(self, file)  # Dump all the current data into the pickle file
        return True  # Return true for success

    def reset_trading_dataframe(self):
        """"Resets the trading data frame pickle file for whatever reason you want"""
        # All columns of the trading history with no data
        df = pd.DataFrame({'Stock Ticker': [],
                           'Buy Invested Amount': [],
                           'Buy Submission Time': [],
                           'Buy Completed Time': [],
                           'Completed Order Price': [],
                           'Shares Holding': [],
                           'Sell Order Time': [],
                           'Sell Completed Time': [],
                           'Profit': []})
        self.trading_history = df  # Dump the dataframe into the trading history attribute
        return True  # Return true for success

    def export_trading_df(self, export_location):
        """Export the trading dataframe to specified location
        :param export_location: str
        """
        df = self.get_trading_history()  # Get trading history dataframe
        if '.xlsx' in export_location:
            df.to_excel(export_location)
        else:
            df.to_excel(export_location + '.xlsx')


def load_profile_from_pickle(profile_first_name):
    """Loads  the data from a profile"""
    with open(profile_first_name + '.pkl', 'rb') as file:  # Open the pickle file
        profile = pickle.load(file)  # Load the trading_data_frame pickle file
    return profile  # Return the trading_data_frame file


def get_stock_price(stock_symbol):
    """Get the last closing price of a stock"""
    # Obtain 1 day history of the stock, one day is the lowest interval
    data = yf.Ticker(stock_symbol).history(period='1d')
    # Look at the last entry, most recent, & retrieve the last one
    current_stock_price = (data.tail(1)['Close'].iloc[0])
    return current_stock_price  # Return the value
