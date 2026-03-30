import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    csv_path = 'Pokemon_Stats.csv'
    return pd.read_csv(csv_path)

pokemon_df = load_data()

def update_types():
    st.session_state.types = pokemon_df[pokemon_df["Generation"].isin(st.session_state.generations)]["Type 1"].unique()

st.multiselect(
    "Generatie",
    [1, 2, 3],
    key="generations",
    on_change=update_types
)
st.selectbox(
    "Type",
    st.session_state.get("types", []),
    key="type"
)