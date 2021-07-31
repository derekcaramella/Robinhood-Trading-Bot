# Import necessary moduless
import robin_stocks.robinhood as r
import requests
import pandas as pd
import yfinance as yf
import openpyxl
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt


def query_sp_500_tickers():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/75.0.3770.100 Safari/537.36'}
    url = 'https://www.slickcharts.com/sp500'
    content = requests.get(url, headers=header)
    dfs = pd.read_html(content.text)
    tickers = dfs[0]['Symbol'].to_list()
    return tickers


def query_yahoo(stock_list):
    df = yf.download(stock_list, group_by='Ticker', period='15m', interval='1m', threads=4)
    df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
    return df


# login = r.login(settings.username, settings.password)
# profile_dictionary = r.build_user_profile()
# cash = profile_dictionary['cash']
# print(cash)

ticker_list = query_sp_500_tickers()  # Requests GET to retrieve S&P 500 tickers
# Obtain top 100 stock tickers. We split it up because batch GET does not reliably work
stock_data_1 = query_yahoo(ticker_list[:100])
# Calculate percent change based on ticker
stock_data_1['Open Percent Change'] = (stock_data_1.groupby('Ticker')['Open'].apply(pd.Series.pct_change) + 1)
stock_data_1['Open Percent Change'] = stock_data_1['Open Percent Change'].fillna(0)  # Fill NaN values with 0
stock_data_1 = stock_data_1.sort_values(by=['Ticker', 'Date'])  # Sort the values
stock_data_1[stock_data_1['Ticker'] == 'AAPL'].plot('Date', 'Open')  # Test plot
plt.show()  # Show plot

correlation_list = []  # A staged list for dataframe (ticker, median of Percent Change, R Squared, Coefficient)
retrieved_tickers = stock_data_1['Ticker'].values.tolist()  # Convert ticker column to list for looping
# Remove duplicates with enumerate
retrieved_tickers = [ticker for _index, ticker in enumerate(retrieved_tickers)
                     if ticker not in retrieved_tickers[:_index]]
for ticker in retrieved_tickers:
    # Retrieve respective ticker's percent change values & timestamp
    instance_df = stock_data_1[stock_data_1['Ticker'] == ticker]  # Filter by respective ticker
    ridge_x = instance_df['Date'].values.astype(float).reshape(-1, 1)  # Reshape x for the ridge model
    ridge_y = instance_df['Open Percent Change'].values  # Obtain the percent changes
    reg = linear_model.Ridge(alpha=0.5).fit(ridge_x, ridge_y)  # Fit the model
    # Append values to the correlation list
    correlation_list.append((ticker, np.median(ridge_y), reg.score(ridge_x, ridge_y), float(reg.coef_)))
# After all ticker data has been obtained convert correlation list to a dataframe
correlation_df = pd.DataFrame(correlation_list,
                              columns=['Ticker', 'Average Growth', 'R Squared', 'Growth Percentage Coefficient'])

correlation_df.sort_values(by=['R Squared', 'Average Growth', 'Growth Percentage Coefficient'])
print(correlation_df.head(20))

# stock_data_2 = query_yahoo(ticker_list[100:200])
# stock_data_3 = query_yahoo(ticker_list[200:300])
# stock_data_4 = query_yahoo(ticker_list[300:400])