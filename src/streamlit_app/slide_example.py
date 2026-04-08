import streamlit as st

with st.expander("Geavanceerde filters"):
    hp_range = st.slider("HP Range", 0, 200, (50, 150))
    st.write(f"HP tussen {hp_range[0]} en {hp_range[1]}")
