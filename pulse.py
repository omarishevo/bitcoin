import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Bitcoin Pulse  Hourly Dataset from Markets Trends and Fear.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price_change'] = df['BTC_USDT_1h_close'] - df['BTC_USDT_1h_open']
    df['change_type'] = df['price_change'].apply(lambda x: 'Increase' if x > 0 else ('Decrease' if x < 0 else 'No Change'))
    return df

df = load_data()

# Title
st.title("📈 Bitcoin Hourly Price Change Analysis")

# Date Range Filter
start_date = st.date_input("Start date", df['timestamp'].min().date())
end_date = st.date_input("End date", df['timestamp'].max().date())

# Filter by date
filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

# Display Summary
st.subheader("Price Movement Summary")
summary = filtered_df['change_type'].value_counts().rename_axis('Change').reset_index(name='Count')
st.dataframe(summary)

# Line Chart of Close Prices
st.subheader("Bitcoin Hourly Closing Price")
st.line_chart(filtered_df.set_index('timestamp')['BTC_USDT_1h_close'])

# Bar Chart of Price Changes
st.subheader("Hourly Price Change Bar Plot")
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(filtered_df['timestamp'], filtered_df['price_change'], 
       color=filtered_df['price_change'].apply(lambda x: 'green' if x > 0 else 'red'))
ax.set_ylabel("Price Change ($)")
ax.set_xlabel("Time")
st.pyplot(fig)

# Show Raw Data
if st.checkbox("Show raw data"):
    st.write(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])
