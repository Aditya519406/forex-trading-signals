
import streamlit as st
import pandas as pd
import numpy as np

st.title("Forex Signal App")

def generate_signal(data):
    if data.empty:
        return "No data available"
    signal = "BUY" if data['Close'].iloc[-1] > data['Open'].iloc[-1] else "SELL"
    return f"Signal: {signal}"

uploaded_file = st.file_uploader("Upload CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head())
    signal = generate_signal(df)
    st.success(signal)
