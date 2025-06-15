import streamlit as st
import pandas as pd

st.title("📈 Bitcoin Hourly Price Change Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Bitcoin CSV dataset", type=["csv"])

if uploaded_file:
    # Load and process data
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price_change'] = df['BTC_USDT_1h_close'] - df['BTC_USDT_1h_open']
    df['change_type'] = df['price_change'].apply(lambda x: 'Increase' if x > 0 else ('Decrease' if x < 0 else 'No Change'))

    # Date Range Filter
    start_date = st.date_input("Start date", df['timestamp'].min().date())
    end_date = st.date_input("End date", df['timestamp'].max().date())

    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Display Summary
    st.subheader("Price Movement Summary")
    summary = filtered_df['change_type'].value_counts().rename_axis('Change').reset_index(name='Count')
    st.dataframe(summary)

    # Line Chart of Closing Prices
    st.subheader("Bitcoin Hourly Closing Price")
    st.line_chart(filtered_df.set_index('timestamp')['BTC_USDT_1h_close'])

    # Bar Chart of Price Change
    st.subheader("Hourly Price Change Bar Chart")
    st.bar_chart(data=filtered_df.set_index('timestamp')['price_change'])

    # Show Raw Data
    if st.checkbox("Show raw data"):
        st.write(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])

else:
    st.warning("Please upload a CSV file to proceed.")
