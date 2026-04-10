"""Assignment 2: Filters and more widgets."""

from pathlib import Path

import pandas as pd
import streamlit as st


def get_sprite_url(pokemon_id):
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{int(pokemon_id)}.png"


# Load data
@st.cache_data
def load_data():
    project_path = Path(__file__).resolve().parent.parent.parent
    csv_path = project_path / "data" / "Pokemon_Stats.csv"
    pokemon_df = pd.read_csv(csv_path, delimiter=";", encoding="latin-1")
    pokemon_df["sprite"] = pokemon_df["Id"].apply(get_sprite_url)
    return pokemon_df


def run_assignment() -> None:
    """Run the Streamlit app for Assignment 2."""
    # Page config and title
    st.set_page_config(layout="wide", page_title="Pokemon Streamlit workshop")
    st.title("Pokemon Streamlit workshop")

    pokemon_df = load_data()

    # Tabs
    tab_overview, tab_charts, tab_table = st.tabs(["Overview", "Charts", "Table"])


import re


def extract_lat_lon(location_str):
    """Extract longitude and latitude from 'POINT (lon lat)' string."""
    try:
        match = re.search(r"POINT \(([-\d\.]+) ([-\d\.]+)\)", location_str)
        lon = float(match.group(1))
        lat = float(match.group(2))
        return lat, lon
    except:
        return None, None


def run_assignment() -> None:
    st.set_page_config(layout="wide", page_title="Pokemon Streamlit workshop")
    st.title("Pokemon Streamlit workshop")

    pokemon_df = load_data()

    # --- Extract coordinates ---
    pokemon_df[["lat", "lon"]] = pokemon_df["location"].apply(
        lambda x: pd.Series(extract_lat_lon(str(x)))
    )

    # Drop rows without coordinates
    pokemon_df = pokemon_df.dropna(subset=["lat", "lon"])

    # --- Sidebar filters ---
    st.sidebar.header("Filters")

    type_filter = st.sidebar.multiselect(
        "Select Type",
        options=sorted(pokemon_df["Type 1"].dropna().unique()),
        default=pokemon_df["Type 1"].dropna().unique(),
    )

    generation_filter = st.sidebar.multiselect(
        "Select Generation",
        options=sorted(pokemon_df["Generation"].unique()),
        default=pokemon_df["Generation"].unique(),
    )

    legendary_filter = st.sidebar.selectbox(
        "Legendary", options=["All", "True", "False"]
    )

    # --- Apply filters ---
    filtered_df = pokemon_df[
        (pokemon_df["Type 1"].isin(type_filter))
        & (pokemon_df["Generation"].isin(generation_filter))
    ]

    if legendary_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Legendary"].astype(str) == legendary_filter.upper()
        ]

    # --- Tabs ---
    tab_overview, tab_charts, tab_table = st.tabs(["Overview", "Charts", "Table"])

    with tab_overview:
        st.subheader("Pokemon Locations")

        st.write(f"Showing {len(filtered_df)} Pokémon")

        # --- Map ---
        st.map(filtered_df[["lat", "lon"]])
