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
    def __init__(self):
        self.cash = None
        self.invested_capital = None
        self.capital_gains = None
        self.pending_trades = False
        self.pending_sells = False
        self.current_stock_holding = None

    def set_cash(self, new_balance):
        """
        Method that sets the attribute self.cash, it will return the attribute if successful
        :param new_balance: float
        :rtype: float
        """
        self.cash = new_balance
        return self.cash

    def set_invested_capital(self, new_invested_capital):
        """
        Method that sets the attribute self.invested_capital, it will return the attribute if successful
        :param new_invested_capital: float
        :rtype: float
        """
        self.invested_capital = new_invested_capital
        return self.invested_capital

    def set_capital_gains(self, new_capital_gains):
        """
        Method that sets the attribute self.new_capital_gains, it will return the attribute if successful
        :param new_capital_gains: float
        :rtype: float
        """
        self.capital_gains = new_capital_gains
        return self.capital_gains

    def set_pending_trades(self, boolean):
        """
        Method that sets the attribute self.pending_trades, it will return the attribute if successful
        :param boolean: bool
        :rtype: bool
        """
        self.pending_trades = boolean
        return self.pending_trades

    def set_pending_sells(self, boolean):
        """
        Method that sets the attribute self.pending_sells, it will return the attribute if successful
        :param boolean: bool
        :rtype: bool
        """
        self.pending_sells = boolean
        return self.pending_sells

    def set_current_stock_holding(self, stock_ticker):
        """
        Method that sets the attribute self.current_stock_holding, it will return the attribute if successful
        :param stock_ticker: string
        :rtype: bool
        """
        self.current_stock_holding = stock_ticker
        return self.current_stock_holding

    def add_cash(self, to_add_cash):
        """
        Method that increases the attribute self.cash by the amount defined, returns the attribute if successful
        :param to_add_cash: float
        :rtype: float
        """
        self.cash += to_add_cash
        return self.cash

    def add_invested_capital(self, to_add_invested_capital):
        """
        Increases the attribute self.invested_capital by the amount defined,if successful return attribute
        :param to_add_invested_capital: float
        :rtype: float
        """
        self.invested_capital += to_add_invested_capital
        return self.cash

    def add_capital_gains(self, to_add_capital_gains):
        """
        Increases the attribute self.capital_gains by the amount defined, if successful return attribute
        :param to_add_capital_gains: float
        :rtype: float
        """
        self.capital_gains += to_add_capital_gains
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

    def get_pending_trades(self):
        """
        Returns the attribute self.pending_trades
        :rtype: bool
        """
        return self.pending_trades

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

    def submit_order(self, stock_symbol, invested_capital):
        """Method that submits order for a stock. The trade is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & add a record with the stock symbol,
        invested capital, & purchase time stamp."""
        global trading_data_frame  # Use trading data frame
        purchase_timestamp = datetime.now()  # Obtain currant time that trade was initiated

        if self.get_cash() >= invested_capital:  # If we have sufficient cash to initiate the trade
            # We create a half empty record
            instance = pd.Series([stock_symbol, invested_capital, purchase_timestamp,
                                  nan, nan, nan, nan, nan, nan],
                                 index=['Stock Ticker', 'Buy Invested Amount', 'Buy Submission Time',
                                        'Buy Completed Time', 'Completed Order Price', 'Shares Holding',
                                        'Sell Order Time', 'Sell Completed Time', 'Profit'])
            # Append the new record to the global dataframe
            trading_data_frame = trading_data_frame.append(instance, ignore_index=True)
            dump_data_to_dataframe_pickle(trading_data_frame)  # Dump that dataframe for later use
            self.set_pending_trades(True)  # Set the pending trade attribute to true
            return True  # Return true if successful
        else:  # We did not have enough cash to initiate the trade
            print(r'You do not have enough cash to initiate the trade.')  # Print error out
            return False  # Return false

    def complete_trade(self):
        """Method that completes order for a stock. The trade is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & update a record with the buy completed order
        time, completed order price, & shares holding. Additionally, only one stock can be bought a time, so we
        will use the the dataframe index strategy to update the rows. We will filter for the opening by the Buy
        Completed Time, then retrieve that row index & update the values."""
        global trading_data_frame  # Use trading data frame
        # Obtain the row index that the incomplete order exists on
        pending_trade_index = trading_data_frame.index[trading_data_frame['Buy Completed Time'].isnull()].tolist()
        # If there are pending trades & a row exists for completion
        if self.get_pending_trades() and pending_trade_index is not None:
            # Obtain the stock ticker at that row index. Values will return a list, so we use 0 index for the value
            pending_stock = trading_data_frame.iloc[pending_trade_index]['Stock Ticker'].values[0]
            # Obtain the invested amount at that row index. Values will return a list, so we use 0 index for the value
            invested_capital = trading_data_frame.iloc[pending_trade_index]['Buy Invested Amount'].values[0]
            current_stock_price = get_stock_price(pending_stock)  # A function that obtains the current stock price
            # Obtain the buy time at that row index. Values will return a list, so we use 0 index for the value
            buy_time = trading_data_frame.iloc[pending_trade_index]['Buy Submission Time'].values[0]
            current_time = pd.Timestamp.now()  # Get the current time with the pandas method
            elapsed_time = (current_time - buy_time).total_seconds()  # Delta time for elapsed time in seconds

            if elapsed_time > 60 * 10:  # If it has been ten minutes since purchase initiation
                trading_data_frame.at[pending_trade_index, 'Buy Completed Time'] = current_time  # Insert Completed Time
                # Insert Completed Order Price
                trading_data_frame.at[pending_trade_index, 'Completed Order Price'] = current_stock_price
                # Shares holding is invested capital divided by current stock price, insert into record
                trading_data_frame.at[pending_trade_index, 'Shares Holding'] = invested_capital / current_stock_price
                self.pending_trades(False)  # Change attribute to close pending trade
                self.set_current_stock_holding(pending_stock)  # Set the attribute to the current stock
                return True  # Return true, it was successful
        else:  # No trades pending
            return False  # Return false

    def submit_sell(self):
        """Method that submits sell order for a stock. The sell is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & update a record with the stock symbol,
        invested capital, & purchase time stamp. Additionally, only one stock can be bought a time, so we will use
        the dataframe index strategy to update the rows. We will filter for the opening by the Sell Completed Time,
        then retrieve that row index &  update the values."""
        global trading_data_frame  # Use trading data frame
        # If there is an active trade, there will be only one, we want to sell that stock
        pending_trade_index = trading_data_frame.index[trading_data_frame['Sell Order Time'].isnull()].tolist()
        # If we have a completed trade that is not sold
        if (not self.get_pending_sells()) and (pending_trade_index is not None):
            current_time = pd.Timestamp.now()  # Obtain the current timestamp with pandas method
            trading_data_frame.at[pending_trade_index, 'Sell Order Time'] = current_time  # Update the record
            self.set_pending_sells(True)  # Set the attribute to true
            return True  # Return true for success
        else:  # We already have a pending trade
            False  # Return false

    def complete_sell(self):
        """Method that completes sell order for a stock. The trade is not completed instantly to simulate a brokerage
        execution rate. The method will use the global trading frame & update a record with the sell order time &
        profit. Additionally, only one stock can be bought a time, so we will use the dataframe index strategy to
        update the rows. We will filter for the opening by the Sell Completed Time, then retrieve that row index &
        update the values."""
        global trading_data_frame  # Use trading data frame
        # If there is an active trade, there will be only one, we want to sell that stock
        pending_trade_index = trading_data_frame.index[trading_data_frame['Sell Completed Time'].isnull()].tolist()
        if self.get_pending_trades() and pending_trade_index is not None:
            # Obtain the stock ticker at that row index. Values will return a list, so we use 0 index for the value
            pending_stock = trading_data_frame.iloc[pending_trade_index]['Stock Ticker'].values[0]
            # Obtain the invested capital at that row index. Values will return a list, so we use 0 index for the value
            invested_capital = trading_data_frame.iloc[pending_trade_index]['Buy Invested Amount'].values[0]
            # Obtain the shares holding at that row index. Values will return a list, so we use 0 index for the value
            shares_holding = trading_data_frame.iloc[pending_trade_index]['Shares Holding'].values[0]
            current_stock_price = get_stock_price(pending_stock)  # A function that obtains the current stock price
            capital_yield = current_stock_price * shares_holding  # Calculates total active capital in stock
            net_capital_gain = capital_yield - invested_capital  # Calculates delta, which is net capital gain
            # Obtain the sell order time at that row index. Values will return a list, so we use 0 index for the value
            sell_time = trading_data_frame.iloc[pending_trade_index]['Sell Order Time'].values[0]
            current_time = pd.Timestamp.now()  # Retrieve current time with pandas method
            elapsed_time = (current_time - sell_time).total_seconds()  # Calculate elapsed time in seconds
            if elapsed_time > 60 * 10:  # If it has been ten minutes since purchase initiation
                # Insert Sell Completed Time
                trading_data_frame.at[pending_trade_index, 'Sell Completed Time'] = current_time
                trading_data_frame.at[pending_trade_index, 'Profit'] = net_capital_gain  # Insert Profit
                self.set_pending_sells(False)  # Set pending sells to false, because we closed this transaction
                self.add_capital_gains(net_capital_gain)  # Add the net capital gains to the existing capital gains
                return True  # Return true
            self.set_current_stock_holding(None)  # We are currently holding no stocks
        else:  # No pending sells for completion
            return False  # Return false


def dump_data_to_dataframe_pickle(up_to_date_df):
    """Saves local dataframe
    :param up_to_date_df: dataframe
    """
    with open('trading_data_frame.pkl', 'wb') as file:  # Open the pickle file
        pickle.dump(up_to_date_df, file)  # Dump all the current data into the pickle data frame
    return True  # Return true for success


def load_data_from_dataframe_pickle():
    """Loads  the data from the trading data frame for global use"""
    with open('trading_data_frame.pkl', 'rb') as file:  # Open the pickle file
        df = pickle.load(file)  # Load the trading_data_frame pickle file
    return df  # Return the trading_data_frame file


def reset_trading_dataframe():
    """"Resets the trading data frame pickle file for whatever reason you want"""
    # All columns of the trading data frame pickle file with no data
    df = pd.DataFrame({'Stock Ticker': [],
                       'Buy Invested Amount': [],
                       'Buy Submission Time': [],
                       'Buy Completed Time': [],
                       'Completed Order Price': [],
                       'Shares Holding': [],
                       'Sell Order Time': [],
                       'Sell Completed Time': [],
                       'Profit': []})
    dump_data_to_dataframe_pickle(df)  # Dump the dataframe into the trading_data_frame pickle file, which overwrites
    return True  # Return true for success


def get_stock_price(stock_symbol):
    """Get the last closing price of a stock"""
    # Obtain 1 day history of the stock, one day is the lowest interval
    data = yf.Ticker(stock_symbol).history(period='1d')
    # Look at the last entry, most recent, & retrieve the last one
    current_stock_price = (data.tail(1)['Close'].iloc[0])
    return current_stock_price  # Return the value


trading_data_frame = load_data_from_dataframe_pickle()  # Load the global trading data frame for updating
