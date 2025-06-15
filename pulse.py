import streamlit as st
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(page_title="Bitcoin Price Analyzer", layout="wide")

# Main Title
st.title("🚀 Bitcoin Hourly Price Change Analysis")

# Sidebar Section
st.sidebar.header("📂 Upload & Filter")
uploaded_file = st.sidebar.file_uploader("Upload your Bitcoin CSV dataset", type=["csv"])

# Load and process the data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price_change'] = df['BTC_USDT_1h_close'] - df['BTC_USDT_1h_open']
    df['change_type'] = df['price_change'].apply(
        lambda x: '📈 Increase' if x > 0 else ('📉 Decrease' if x < 0 else '➖ No Change'))

    # Sidebar date filters
    start_date = st.sidebar.date_input("Start date", df['timestamp'].min().date())
    end_date = st.sidebar.date_input("End date", df['timestamp'].max().date())

    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # Summary Section
    st.subheader("📊 Summary of Price Changes")
    col1, col2, col3 = st.columns(3)
    counts = filtered_df['change_type'].value_counts()

    col1.metric("📈 Increases", counts.get("📈 Increase", 0))
    col2.metric("📉 Decreases", counts.get("📉 Decrease", 0))
    col3.metric("➖ No Change", counts.get("➖ No Change", 0))

    # Charts Section
    st.markdown("### 🔍 Visual Analysis")

    col4, col5 = st.columns(2)

    with col4:
        st.write("**Hourly Closing Prices**")
        st.line_chart(filtered_df.set_index('timestamp')['BTC_USDT_1h_close'])

    with col5:
        st.write("**Hourly Price Changes**")
        st.bar_chart(filtered_df.set_index('timestamp')['price_change'])

    # Expand to show raw data
    with st.expander("🗃️ View Raw Data"):
        st.dataframe(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])

    # Footer
    st.markdown("---")
    st.markdown("📌 *Data analyzed from hourly market trends.* Built with ❤️ using Streamlit.")

else:
    st.warning("📤 Please upload a CSV file using the sidebar to proceed.")
