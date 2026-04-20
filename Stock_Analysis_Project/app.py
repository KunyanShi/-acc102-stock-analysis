import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Page config (MUST be at the start!)
st.set_page_config(page_title="Financial Data Analysis Tool", layout="wide")
st.title("📊 Tech Stocks Deep Analysis Dashboard")

# Sidebar interactive components
ticker = st.sidebar.selectbox("Select Asset", ["AAPL", "MSFT", "NVDA", "GOOG"])
period = st.sidebar.slider("Select Time Range (Years)", 1, 5, 2)

# Simulated stock data generation
@st.cache_data
def generate_stock_data(ticker, years):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    
    # Base price for realistic simulation
    base_price_map = {"AAPL": 190, "MSFT": 400, "NVDA": 850, "GOOG": 150}
    base_price = base_price_map[ticker]
    
    # Generate realistic returns
    returns = np.random.normal(0.0006, 0.02, len(dates))
    close_prices = base_price * (1 + returns).cumprod()
    
    # Generate OHLCV data
    df = pd.DataFrame({
        "Adj Close": close_prices * 0.99,
        "Close": close_prices,
        "High": close_prices * 1.015,
        "Low": close_prices * 0.985,
        "Open": close_prices * 1.003,
        "Volume": np.random.randint(20_000_000, 80_000_000, len(dates))
    }, index=dates)
    df.index.name = "Date"
    return df

# Load data
df = generate_stock_data(ticker, period)

# Drop missing values
df = df.dropna()

# Core analysis: 20-day moving average
df['MA20'] = df['Close'].rolling(window=20).mean()

# Calculate daily return
df['Daily_Return'] = df['Close'].pct_change()

# Plot: Price and MA20
st.subheader(f"{ticker} Stock Price & 20-Day Moving Average")
fig = px.line(df, y=['Close', 'MA20'], title=f"{ticker} Price Trend")
fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# Data summary
st.subheader("Data Summary")
st.dataframe(df.describe())