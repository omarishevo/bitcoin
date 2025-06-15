import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Bitcoin Dashboard", layout="wide")

# --- Logo and Title ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("C:\Users\Administrator\Pictures\kanchanara-5ixVD22x22o-unsplash.jpg")
with col2:
    st.title("🚀 Bitcoin Hourly Price Change Analysis")

# --- Sidebar Upload ---
st.sidebar.header("📂 Upload & Filter")
uploaded_file = st.sidebar.file_uploader("Upload your Bitcoin CSV dataset", type=["csv"])

# --- Load Data ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price_change'] = df['BTC_USDT_1h_close'] - df['BTC_USDT_1h_open']
    df['change_type'] = df['price_change'].apply(
        lambda x: '📈 Increase' if x > 0 else ('📉 Decrease' if x < 0 else '➖ No Change'))

    # --- Filter by Date ---
    start_date = st.sidebar.date_input("Start date", df['timestamp'].min().date())
    end_date = st.sidebar.date_input("End date", df['timestamp'].max().date())
    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    # --- Summary ---
    st.subheader("📊 Price Movement Summary")
    col3, col4, col5 = st.columns(3)
    counts = filtered_df['change_type'].value_counts()
    col3.metric("📈 Increases", counts.get("📈 Increase", 0))
    col4.metric("📉 Decreases", counts.get("📉 Decrease", 0))
    col5.metric("➖ No Change", counts.get("➖ No Change", 0))

    # --- Charts ---
    st.markdown("### 📉 Visualizations")
    col6, col7 = st.columns(2)
    with col6:
        st.write("**Hourly Closing Prices**")
        st.line_chart(filtered_df.set_index('timestamp')['BTC_USDT_1h_close'])
    with col7:
        st.write("**Hourly Price Changes**")
        st.bar_chart(filtered_df.set_index('timestamp')['price_change'])

    # --- Raw Data ---
    with st.expander("🗃️ View Raw Data Table"):
        st.dataframe(filtered_df[['timestamp', 'BTC_USDT_1h_open', 'BTC_USDT_1h_close', 'price_change', 'change_type']])

    st.markdown("---")
    st.caption("📌 Built with ❤️ using Streamlit | Data based on hourly market trends.")

else:
    st.warning("📤 Please upload a CSV file using the sidebar to continue.")
