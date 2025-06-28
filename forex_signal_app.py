
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.title("📈 Forex Auto Signal App")

symbol = st.text_input("Enter Forex Pair (e.g., EURUSD=X)", "EURUSD=X")

@st.cache_data
def load_data(symbol):
    df = yf.download(symbol, period="30d", interval="1h")
    if df.empty:
        return pd.DataFrame()
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    df['EMA200'] = df['Close'].ewm(span=200).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df.dropna(inplace=True)
    return df

def generate_signal(df):
    if df.empty:
        return "No data available", None, None
    last = df.iloc[-1]
    if last['EMA50'] > last['EMA200'] and last['RSI'] < 70:
        return "📈 BUY", last['Close'] * 0.98, last['Close'] * 1.02
    elif last['EMA50'] < last['EMA200'] and last['RSI'] > 30:
        return "📉 SELL", last['Close'] * 1.02, last['Close'] * 0.98
    else:
        return "⏸️ HOLD", None, None

data = load_data(symbol)

if not data.empty:
    st.line_chart(data['Close'])
    signal, sl, tp = generate_signal(data)
    st.subheader(f"Signal: {signal}")
    if sl and tp:
        st.write(f"Stop Loss: {sl:.4f}")
        st.write(f"Take Profit: {tp:.4f}")
else:
    st.warning("No data found. Check your symbol (e.g., EURUSD=X)")
