import requests
import pandas as pd
import json
from datetime import datetime
import os

if os.path.exists('my_key'):
    with open('my_key') as f:
        key = f.read()
        my_key = key
else:
    print('-' * 50)
    my_key = input('What is your API key? ')
    print('-' * 50)
    with open('my_key', 'w+') as f:
        f.write(my_key)

columns = ['date','open', 'high', 'low', 'close', 'volume']

def get_intraday_data(symbol, interval='1min', key=my_key, mode='save'):
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={key}')
    data = json.loads(response.text)
    data = pd.DataFrame.from_dict(data[f'Time Series ({interval})'], orient='index')
    data.reset_index(inplace=True)
    data.columns = columns
    if mode == 'save':
        data.to_csv(f'./data/intra/{symbol}_{datetime.today().date()}.csv', index=False)
    else:
        return data

def get_daily_data(symbol, key=my_key):
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}')
    data = json.loads(response.text)
    data = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    data.reset_index(inplace=True)
    data.columns = columns
    data.to_csv(f'./data/daily/{symbol}.csv', index=False)

def get_weekly_data(symbol, key=my_key):
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={key}')
    data = json.loads(response.text)
    data = pd.DataFrame.from_dict(data['Weekly Time Series'], orient='index')
    data.reset_index(inplace=True)
    data.columns = columns
    data.to_csv(f'./data/weekly/{symbol}.csv', index=False)

def get_monthly_data(symbol, key=my_key):
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={key}')
    data = json.loads(response.text)
    data = pd.DataFrame.from_dict(data['Monthly Time Series'], orient='index')
    data.reset_index(inplace=True)
    data.columns = columns
    data.to_csv(f'./data/monthly/{symbol}.csv', index=False)