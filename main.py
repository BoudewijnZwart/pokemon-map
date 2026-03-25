"""Main Streamlit app module."""

# import streamlit as st

# # Text input
# trainer_name = st.text_input("Wat is je naam?", placeholder="Ash Ketchum")

# # Numbers
# level = st.number_input("Pokemon level", min_value=1, max_value=100)
# hp = st.slider("HP selecteren", 0, 200, 50)  # min, max, default

# # Select
# pokemon_type = st.selectbox("Kies een type", ["Fire", "Water", "Grass", "Electric"])
# team = st.multiselect("Kies je team (max 6)", ["Pikachu", "Charizard", "Blastoise"])

# # Boolean
# is_legendary = st.checkbox("Alleen legendaries")

# # Button (trigger actie)
# if st.button("🚀 Vang Pokemon"):
#     st.success(f"{trainer_name} heeft een {pokemon_type} Pokemon gevangen!")

import streamlit as st
import pandas as pd

# Text
st.write("Simpelste manier om iets te tonen")
st.title("🏆 Grote titel")
st.header("📌 Header")
st.subheader("📍 Subheader")
st.markdown("**Bold** en *italic* tekst")

# ✨ Magic!
st.file_uploader("Upload pokemon...")

# Data
df = pd.DataFrame(
  {
    "pokemon": ["Pikachu", "Charizard", "Bulbasaur"], 
    "hp": [35, 78, 45]
  }
)
st.dataframe(df)  # 📊 Interactieve tabel (sorteerbaar!)
st.table(df)      # 📋 Static tabel

# Metrics: 📈 Met delta
st.metric("Totaal Pokemon", "151", "+1 nieuwe")