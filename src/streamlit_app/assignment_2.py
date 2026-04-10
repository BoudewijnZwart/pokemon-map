"""Assignment 2: Filters and more widgets."""

from pathlib import Path

import pandas as pd
import streamlit as st


# Load data
@st.cache_data
def load_data():
    project_path = Path(__file__).resolve().parent.parent.parent
    csv_path = project_path / "data" / "Pokemon_Stats.csv"
    return pd.read_csv(csv_path, delimiter=";", encoding='latin-1')


def run_assignment() -> None:
    """Run the Streamlit app for Assignment 2."""
    # Page config and title
    st.set_page_config(layout="wide", page_title="Pokemon Streamlit workshop")
    st.title("Pokemon Streamlit workshop")

    pokemon_df = load_data()

    # Tabs
    tab_overview, tab_charts, tab_table = st.tabs(["Overview", "Charts", "Table"])

    # Overview Tab
    with tab_overview:
        st.header("Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Pokémon", len(pokemon_df))
        col2.metric("Total Legendaries", pokemon_df["Legendary"].sum())
        col3.metric("Generations", pokemon_df["Generation"].nunique())
        all_types = pokemon_df[["Type 1", "Type 2"]].stack().reset_index(drop=True)
        col4.metric("Unique Types", all_types.nunique())

    # Charts Tab
    with tab_charts:
        st.header("Charts")

        # Type 1 Bar Chart
        st.subheader("Type 1 Distribution")
        df_type1_count = pokemon_df["Type 1"].value_counts().reset_index()
        df_type1_count.columns = ["Type 1", "Count"]
        st.bar_chart(df_type1_count, x="Type 1", y="Count")

        # Type 2 Bar Chart
        st.subheader("Type 2 Distribution")
        df_type2_count = pokemon_df["Type 2"].value_counts(dropna=False).reset_index()
        df_type2_count.columns = ["Type 2", "Count"]
        st.bar_chart(df_type2_count, x="Type 2", y="Count")

        # Combined Type Bar Chart
        st.subheader("Combined Type Distribution")
        pokemon_df["Type all"] = pokemon_df["Type 1"] + " - " + pokemon_df["Type 2"].fillna('')
        df_type_all_count = pokemon_df["Type all"].value_counts().reset_index()
        df_type_all_count.columns = ["Type all", "Count"]
        st.bar_chart(df_type_all_count, x="Type all", y="Count")

        # Water Scatter Plot
        st.subheader("Attack vs. Defense Water Pokémon")
        water_flying_attack = pokemon_df[
            (pokemon_df["Type 1"] == "Water")
        ][["Name", "Attack", "Defense"]].reset_index(drop=True)
        st.scatter_chart(water_flying_attack, x="Defense", y="Attack")

    # Table Tab
    with tab_table:
        st.header("Filtered Pokémon")

        # Filters (only shown in Table tab)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            legendary_yes_check = st.checkbox("Show Legendary Only", value=False)
        with col2:
            generations = ["All"] + sorted(pokemon_df["Generation"].unique().astype(str).tolist())
            generation_select = st.selectbox('Generation', generations, index=0)
        with col3:
            all_types = ["All"] + sorted(pokemon_df["Type 1"].unique().tolist())
            type_1_select = st.selectbox('Type 1', all_types, index=0)
        with col4:
            type_2_select = st.selectbox('Type 2', ["All", "None"] + all_types, index=0)

        # Apply filters
        pokemon_show = pokemon_df.copy()
        if legendary_yes_check:
            pokemon_show = pokemon_show[pokemon_show["Legendary"]]
        if generation_select != "All":
            pokemon_show = pokemon_show[pokemon_show["Generation"] == int(generation_select)]
        if type_1_select != "All":
            pokemon_show = pokemon_show[pokemon_show["Type 1"] == type_1_select]
        if type_2_select != "All":
            if type_2_select == "None":
                pokemon_show = pokemon_show[pokemon_show["Type 2"].isna()]
            else:
                pokemon_show = pokemon_show[pokemon_show["Type 2"] == type_2_select]

        st.dataframe(pokemon_show, width='stretch')
