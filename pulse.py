import streamlit as st
import pandas as pd

# Direct path to the dataset in Documents (make sure this path is correct)
DATA_FILE = r"C:\Users\Administrator\Documents\Bitcoin Pulse  Hourly Dataset from Markets Trends and Fear.csv"

# Load and process the data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price_change'] = df['BTC_USDT_1h_close'] - df['BTC_USDT_1h_open']
    df['change_type'] = df['price_change'].apply(
        lambda x: 'Increase' if x > 0 else ('Decrease' if x < 0 else 'No Change')
    )
    return df

# App title
st.title("📊 Bitcoin Hourly Price Change Analysis")

try:
    df = load_data()

    # Date filter
    start_date = st.date_input("Start date", df['timestamp'].min().date())
    end_date = st.date_input("End date", df['timestamp'].max().date())

    # Filter data
    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Summary
    st.subheader("📈 Price Movement Summary")
    summary = filtered_df['change_type'].value_counts().rename_axis('Change').reset_index(name='Count')
    st.dataframe(summary)

    # Charts
    st.subheader("📉 Bitcoin Hourly Closing Price")
    st.line_chart(filtered_df.set_index('timestamp')['BTC_USDT_1h_close'])

    st.subheader("📊 Hourly Price Change")
    st.bar_chart(filtered_df.set_index('timestamp')['price_change'])

    # Show raw data
    if st.checkbox("Show raw data"):
        st.write(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])

except FileNotFoundError:
    st.error(f"⚠️ File not found:\n`{DATA_FILE}`\n\nPlease confirm the file exists at that exact location.")
except KeyError as e:
    st.error(f"⚠️ Missing column in dataset: {e}")
except Exception as e:
    st.error(f"⚠️ An unexpected error occurred:\n{e}")
