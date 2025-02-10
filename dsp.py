# Import libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import get_indicators as gi
#import seaborn as sns


# Streamlit app title
st.title("Stock Trading Companion")

# Sidebar input
st.sidebar.header("Input Stock Information")
stock_ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.Timestamp("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp("2023-01-01"))
indicators = st.sidebar.multiselect("Select Indicators", ["SMA10", "SMA100", "SMA200", "Daily Returns", "RSI", "Volatility"])


# Fetch stock data
#@st.cache_data #cache the data for faster loading

def fetch_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

#Create the data dataframe

data = fetch_data(stock_ticker, start_date, end_date)


#Show last rows of the dataframe
st.subheader(f"Raw Data for {stock_ticker}")
st.write(data.tail())


# plotting indicators

st.subheader("Stock Price and Indicators")
fig, ax = plt.subplots()
ax.plot(data['Close'], label='Close Price', alpha=0.8)
for indicator in indicators:
    if indicator == "SMA10":
        ax.plot(gi.SMA10(data), label='SMA10', alpha=0.8, linestyle="--")
        data['SMA10'] = gi.SMA10(data)
    elif indicator == "SMA100":
        ax.plot(gi.SMA100(data), label='SMA100', alpha=0.8, linestyle="--")
        data['SMA100'] = gi.SMA100(data)
    elif indicator == "SMA200":
        ax.plot(gi.SMA200(data), label='SMA200', alpha=0.8, linestyle="--")
        data['SMA200'] = gi.SMA200(data)
    elif indicator == "Daily Returns":
        ax2 = ax.twinx()
        ax2.set_ylabel("Daily Returns in %")
        ax2.set_ylim(0, 1)
        #data['Daily Returns'] = gi.daily_returns(data)
        ax2.plot(gi.daily_returns(data), label='Daily Returns', alpha=0.8, linestyle="-", color = 'red')
        plt.xticks(rotation=45, ha='right')
    elif indicator == "RSI":
        ax.plot(gi.RSI(data), label='RSI', alpha=0.8, linestyle="--")
        data['RSI'] = gi.RSI(data)
    elif indicator == "Volatility":
        ax.plot(gi.volatility(data), label='Volatility', alpha=0.8, linestyle="--")
        data['Volatility'] = gi.volatility(data)
#ax.plot(data[indicator], label=indicator, alpha = 0.8, linestyle="--")
ax.set_title(f"{stock_ticker} Indicators Overview")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.xticks(rotation=45, ha='right')
ax.legend()
st.pyplot(fig)

# Footer
st.write("Good luck! And may the odds be ever in your favor.")

# to add
# sentiment analysis
# random forrest + UI for parametere tuning
# comparing multiple stocks