import streamlit as st
import pandas as pd

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

# Bar Chart of Price Change
st.subheader("Hourly Price Change Bar Chart")
st.bar_chart(data=filtered_df.set_index('timestamp')['price_change'])

# Show Raw Data
if st.checkbox("Show raw data"):
    st.write(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])
