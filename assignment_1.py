import streamlit as st
import pandas as pd
import numpy as np


st.title("Pokemon streamlit!")

csv_path = 'Pokemon_Stats.csv'
pokemon_df =pd.read_csv(csv_path)

st.set_page_config(layout="wide")

st.text(f"Total number of pokemon: {len(pokemon_df)}")
st.text(f"Total legendaries: {pokemon_df["Legendary"].sum()}")
st.text(f"Amount of generations: {pokemon_df["Generation"].nunique()}")
all_types = pokemon_df[["Type 1", "Type 2"]]
stacked_types = all_types.stack().reset_index(drop=True)
st.text(f"Unique types: {stacked_types.nunique()}")

df_type = pokemon_df[["Type 1"]]
df_type1_count = df_type.value_counts(dropna=False).reset_index()

st.bar_chart(df_type1_count, x='Type 1', y='count')

df_type = pokemon_df[["Type 2"]]
df_type2_count = df_type.value_counts(dropna=False).reset_index()

st.bar_chart(df_type2_count, x='Type 2', y='count')

pokemon_df["Type all"] = pokemon_df["Type 1"] + " - " + pokemon_df["Type 2"].fillna('')

df_type_all = pokemon_df[["Type all"]]

df_type_all_count = df_type_all.value_counts().reset_index()

st.bar_chart(df_type_all_count, x='Type all', y='count')

st.text("Attack defense for Water Type")

attack = pokemon_df[["Name", "Type all", "Type 1", "Type 2", "Attack", "Defense"]]
water_attack = attack[attack["Type 1"] == 'Water']
water_flying_attack = water_attack[attack["Type 2"] == 'Flying'].reset_index()
print(water_flying_attack)

st.scatter_chart(water_flying_attack[["Name", "Attack", "Defense"]], x="Name", color=["red", "green"])

types = ["All"]
all_types = [str(i) for i in pokemon_df["Type 1"].unique()]
total_types = ["All"] + all_types

col_1, col_2, col_3, col_4 = st.columns(4)
with col_1: 
    legendary_yes_check = st.checkbox("show Legendary")
with col_2:
    generations = ["All"]
    generations = generations + [str(i) for i in pokemon_df["Generation"].unique()]
    generation_select = st.selectbox('Choose generation', (generations), index=0)
with col_3:
    type_1_select = st.selectbox('Type 1', (total_types), index=0)
with col_4:
    total_types_none = ["All", "None"] + all_types
    type_2_select = st.selectbox('Type 2', (total_types_none), index=0)

pokemon_show = pokemon_df

if legendary_yes_check:
    pokemon_show = pokemon_show[pokemon_show["Legendary"] is True]
if generation_select != "All":
    pokemon_show = pokemon_show[pokemon_show["Generation"] == int(generation_select)]
if type_1_select != "All":
    pokemon_show = pokemon_show[pokemon_show["Type 1"] == type_1_select]
if type_2_select != "All":
    if type_2_select == "None":
        pokemon_show = pokemon_show[pokemon_show["Type 2"].isna()]
    else:
        pokemon_show = pokemon_show[pokemon_show["Type 2"] == type_2_select]

st.dataframe(pokemon_show)

st.text(f"legendary: {legendary_yes_check}")
st.text(f"generation: {generation_select}")
st.text(f"type 1: {type_1_select}")
st.text(f"type 2: {type_2_select}")

