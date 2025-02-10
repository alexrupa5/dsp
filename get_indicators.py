import pandas as pd
import numpy as np


# 14 days relative strength index
def RSI(data):
    difference = data['Close'].diff() #compares the current day's close price with the previous day's close price
    gain = difference.where(difference > 0, 0).rolling(window=14).mean()
    loss = -difference.where(difference < 0, 0).rolling(window=14).mean()

    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data['RSI']


# moving avg
def SMA10(data):
    data['SMA10'] = data['Close'].rolling(window=10).mean()
    return data['SMA10']

def SMA100(data):
    data['SMA100'] = data['Close'].rolling(window=100).mean()
    return data['SMA100']

def SMA200(data):
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    return data['SMA200']

# daily returns/pct change in close price
def daily_returns(data):
    data['Daily Returns'] = data['Close'].pct_change()
    return data['Daily Returns']


# volatility st dev of returns 20 days
def volatility(data):
    data['Volatility'] = data['Close'].pct_change().rolling(window=20).std()
    return data['Volatility']
