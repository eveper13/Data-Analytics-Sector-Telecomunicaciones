

# utils.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)