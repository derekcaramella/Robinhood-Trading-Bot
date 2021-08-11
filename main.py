# Import necessary modules
import robin_stocks.robinhood as r
import requests
import pandas as pd
import yfinance as yf
import openpyxl
from sklearn import linear_model
import numpy as np


def query_sp_500_tickers():
    """Call function with no parameters to obtain list of stock symbols"""
    # Mimic a search engine
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/75.0.3770.100 Safari/537.36'}
    url = 'https://www.slickcharts.com/sp500'  # Website that holds S&P tickers
    content = requests.get(url, headers=header)  # Retrieve data from website
    dfs = pd.read_html(content.text)  # Parse the data to pandas dataframe
    tickers = dfs[0]['Symbol'].to_list()  # Convert the first column to a list
    return tickers  # Return the list


def query_yahoo(stock_list):
    """Queries yahoo finance that returns Date, Ticker, Adjusted Close, High, Low, Open, & Volume panel dataframe"""
    # Get stock data by ticker every 15 minutes on a 1 minute interval, the threads increase efficiency
    df = yf.download(stock_list, group_by='Ticker', period='15m', interval='1m', threads=4)
    df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()  # Reshape the the dataframe for panel data
    return df  # return the dataframe


def calculate_percent_change_df(dataframe):
    """Returns dataframe with open percent change column
    :param dataframe: pandas dataframe
    """
    # Grouping by ticker, calculate the percentage change
    dataframe['Open Percent Change'] = (dataframe.groupby('Ticker')['Open'].pct_change() * 100)
    dataframe.fillna(0, inplace=True)  # Fill na to calculate ridge model
    return dataframe  # Return dataframe


def build_ridge_analysis_dataframe(percent_change_dataframe):
    """Returns a dataframe: Ticker Average Growth, R Squared, Growth Percentage Coefficient
    :param percent_change_dataframe: pandas dataframe with percent change built into the df
    """
    correlation_list = []  # A staged list for dataframe (ticker, median of Percent Change, R Squared, Coefficient)
    retrieved_tickers = percent_change_dataframe['Ticker'].values.tolist()  # Convert ticker column to list for looping
    # Remove duplicates with enumerate
    retrieved_tickers = [ticker for _index, ticker in enumerate(retrieved_tickers)
                         if ticker not in retrieved_tickers[:_index]]
    for ticker in retrieved_tickers:
        # Retrieve respective ticker's percent change values & timestamp
        instance_df = percent_change_dataframe[percent_change_dataframe['Ticker'] == ticker]  # Filter by ticker
        reputation = instance_df['Reputation Weight'].mean()  # Obtain reputation weight
        ridge_x = instance_df['Date'].values.astype(float).reshape(-1, 1)  # Reshape x for the ridge model
        ridge_y = instance_df['Open Percent Change'].values  # Obtain the percent changes
        reg = linear_model.Ridge(alpha=0.5).fit(ridge_x, ridge_y)  # Fit the model
        # Append values to the correlation list
        correlation_list.append((ticker, reputation, np.median(ridge_y), reg.score(ridge_x, ridge_y), float(reg.coef_)))
    # After all ticker data has been obtained convert correlation list to a dataframe
    correlation_df = pd.DataFrame(correlation_list,
                                  columns=['Ticker', 'Reputation Weight', 'Average Growth',
                                           'R Squared', 'Growth Percentage Coefficient'])
    return correlation_df

def build_complete_stock_data():
    """From stock symbol acquisition to ridge modeling, this will sort return a complete dataframe of the top 300'
    S&P companies"""
    ticker_list = query_sp_500_tickers()  # Requests GET to retrieve S&P 300 tickers
    # Obtain top 100 stock tickers. We split it up because batch GET does not reliably work
    stock_data_1 = query_yahoo(ticker_list[:100])  # Obtain top 99 stock tickers
    stock_data_2 = query_yahoo(ticker_list[100:200])  # Obtain 100 - 199 stock tickers
    stock_data_3 = query_yahoo(ticker_list[200:300])  # Obtain top 200 - 299 stock tickers
    stock_data_1['Reputation Weight'] = 3  # Set reputation weight to heaviest
    stock_data_2['Reputation Weight'] = 2  # Set reputation weight to medium
    stock_data_3['Reputation Weight'] = 1  # Set reputation weight to lightest
    total_stock_df = pd.concat([stock_data_1, stock_data_2, stock_data_3])  # Stack dataframes
    total_stock_df = calculate_percent_change_df(total_stock_df)  # Calculate the percent change
    total_stock_df = build_ridge_analysis_dataframe(total_stock_df)  # Obtain ridge regression analysis
    # Sort for purchase analysis
    total_stock_df.sort_values(by=['Reputation Weight', 'R Squared', 'Average Growth', 'Growth Percentage Coefficient'])
    return total_stock_df  # Return data frame

# login = r.login(settings.username, settings.password)
# profile_dictionary = r.build_user_profile()
# cash = profile_dictionary['cash']
# print(cash)