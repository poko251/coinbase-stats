import streamlit as st
import pandas as pd
from src.etl import get_file_path, load_transactions, clean_currency_columns, convert_dates

st.set_page_config(
    page_title=" Coinbase Stats",
    page_icon="",
    layout="wide"
)

st.title("Coinbase Stats Dashboard")

# Choose data source
st.subheader("Data Source")
data_option = st.radio(
    "Select how you want to load data:",
    ("Use file from data/raw", "Upload file manually")
)

df = None

if data_option == "Use file from data/raw":
    try:
        filepath = get_file_path()
        df = load_transactions(filepath)
    except Exception as e:
        st.error(f"Error: {e}")

elif data_option == "Upload file manually":
    uploaded_file = st.file_uploader("Upload your Coinbase CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, skiprows=3, encoding="utf-8")

# If we have a DataFrame, clean and save it into session_state
if df is not None:
    df = clean_currency_columns(df)
    df = convert_dates(df)
    st.session_state["df"] = df

    st.success("Data loaded successfully!")
    st.dataframe(df.head())

    #  Export button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=" Download Clean Dataset as CSV",
        data=csv,
        file_name="coinbase_clean.csv",
        mime="text/csv",
    )
else:
    st.warning("No data loaded yet.")
