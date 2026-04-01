import streamlit as st
import pandas as pd

# Initialize state
if "data" not in st.session_state:
    st.session_state.data = pd.read_csv('datasets/Pokemon_Stats.csv',delimiter=',')

st.title("Pokemon Data")
st.session_state.data = st.data_editor(st.session_state.data)

st.scatter_chart(st.session_state.data,x="HP",y="Attack")