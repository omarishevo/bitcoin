import streamlit as st
import pandas as pd

st.title("📈 Bitcoin Hourly Price Change Analysis")

# Upload file
uploaded_file = st.file_uploader("Upload your Bitcoin CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Load and process the data
    try:
        df = pd.read_csv(uploaded_file)

        # Check if required columns exist
        if 'timestamp' in df.columns and 'BTC_USDT_1h_close' in df.columns and 'BTC_USDT_1h_open' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['price_change'] = df['BTC_USDT_1h_close'] - df['BTC_USDT_1h_open']
            df['change_type'] = df['price_change'].apply(
                lambda x: 'Increase' if x > 0 else ('Decrease' if x < 0 else 'No Change')
            )

            # Date Range Selection
            start_date = st.date_input("Start date", df['timestamp'].min().date())
            end_date = st.date_input("End date", df['timestamp'].max().date())
            filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

            # Display summary
            st.subheader("Price Movement Summary")
            summary = filtered_df['change_type'].value_counts().rename_axis('Change').reset_index(name='Count')
            st.dataframe(summary)

            # Charts
            st.subheader("Bitcoin Hourly Closing Price")
            st.line_chart(filtered_df.set_index('timestamp')['BTC_USDT_1h_close'])

            st.subheader("Hourly Price Change")
            st.bar_chart(filtered_df.set_index('timestamp')['price_change'])

            # Raw data toggle
            if st.checkbox("Show raw data"):
                st.write(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])
        else:
            st.error("Uploaded file is missing required columns: 'timestamp', 'BTC_USDT_1h_open', or 'BTC_USDT_1h_close'.")

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")

else:
    st.info("📂 Please upload a CSV file to begin.")
