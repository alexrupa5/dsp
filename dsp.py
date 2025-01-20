# Import libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit app title
st.title("Stock Trading Guide")

# Sidebar input
st.sidebar.header("Input Stock Information")
stock_ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.Timestamp("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp("2023-01-01"))

# Fetch stock data
@st.cache_data
def fetch_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

data = fetch_data(stock_ticker, start_date, end_date)

# Show raw data (optional)
st.subheader(f"Raw Data for {stock_ticker}")
st.write(data.tail())

# Add technical analysis
def add_technical_indicators(data):
    # Moving Averages
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    # Daily Returns
    data['Daily Return'] = data['Close'].pct_change()

    # Volatility (Standard Deviation of returns)
    data['Volatility'] = data['Daily Return'].rolling(window=20).std()

    # RSI (Relative Strength Index)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data

data = add_technical_indicators(data)

# Plot price and indicators
st.subheader("Stock Price and Indicators")
fig, ax = plt.subplots()
ax.plot(data['Close'], label="Close Price", alpha=0.8)
ax.plot(data['SMA50'], label="SMA 50", linestyle="--")
ax.plot(data['SMA200'], label="SMA 200", linestyle="--")
ax.set_title(f"{stock_ticker} Price and Moving Averages")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
st.pyplot(fig)

# Key Metrics
st.subheader("Key Metrics")
st.metric("Current Price", round(data['Close'].iloc[-1], 2))
st.metric("50-Day SMA", round(data['SMA50'].iloc[-1], 2))
st.metric("200-Day SMA", round(data['SMA200'].iloc[-1], 2))
st.metric("Volatility", f"{round(data['Volatility'].iloc[-1] * 100, 2)}%")
st.metric("RSI", round(data['RSI'].iloc[-1], 2))

# Analysis logic
st.subheader("Analysis and Recommendation")

current_price = float(data['Close'].iloc[-1])
sma50 = float(data['SMA50'].iloc[-1])
sma200 = float(data['SMA200'].iloc[-1])
rsi = float(data['RSI'].iloc[-1])


#just a test
#st.write(f"SMA50 is {sma50} and also {data['SMA50']} and btw {data['SMA50'].iloc[-1]}")



# Simple recommendations based on conditions
if current_price > sma200 and sma50 > sma200:
    recommendation = "Buy (Uptrend Confirmed)"
elif current_price < sma200:
    recommendation = "Sell (Below Long-Term Average)"
elif rsi > 70:
    recommendation = "Sell (Overbought)"
elif rsi < 30:
    recommendation = "Buy (Oversold)"
else:
    recommendation = "Hold"

st.write(f"**Recommendation**: {recommendation}")

# Risk vs Return Estimation
avg_daily_return = data['Daily Return'].mean()
daily_volatility = data['Volatility'].mean()
annual_return = avg_daily_return * 252
annual_volatility = daily_volatility * np.sqrt(252)

st.subheader("Risk and Return Estimation")
st.write(f"**Expected Annual Return**: {round(annual_return * 100, 2)}%")
st.write(f"**Expected Annual Volatility (Risk)**: {round(annual_volatility * 100, 2)}%")

# Footer
st.write("Good luck! And may the odds be ever in your favor.")


