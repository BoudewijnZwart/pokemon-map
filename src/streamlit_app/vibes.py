"""Assignment 2: Filters and more widgets."""

import re
from pathlib import Path

import pandas as pd
import streamlit as st


# Load data
@st.cache_data
def load_data():
    project_path = Path(__file__).resolve().parent.parent.parent
    csv_path = project_path / "data" / "Pokemon_Stats.csv"
    return pd.read_csv(csv_path, delimiter=";", encoding="latin-1")


def parse_coordinates(location_str: str):
    """Extract lat/lon from a POINT string like 'POINT (-75.74 -14.08)'."""
    if not isinstance(location_str, str):
        return None, None
    match = re.search(r"POINT\s*\(([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)\)", location_str)
    if match:
        lon = float(match.group(1))
        lat = float(match.group(2))
        return lat, lon
    return None, None


@st.cache_data
def prepare_map_data(df: pd.DataFrame) -> pd.DataFrame:
    """Parse coordinates and clean up for map display."""
    coords = df["location"].apply(lambda x: parse_coordinates(x))
    df = df.copy()
    df["lat"] = [c[0] for c in coords]
    df["lon"] = [c[1] for c in coords]
    return df.dropna(subset=["lat", "lon"])


def get_pokemon_id(row) -> int:
    """Safely return integer Pokémon dex ID."""
    for key in ("Id", "id", "ID"):
        if key in row.index:
            try:
                return int(row[key])
            except ValueError, TypeError:
                pass
    return 0


def sprite_url(dex_id: int) -> str:
    """PokeAPI official sprite URL."""
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_id}.png"


# Type colour palette (Pokémon type colours)
TYPE_COLORS = {
    "Fire": "#FF4422",
    "Water": "#3399FF",
    "Grass": "#77CC55",
    "Electric": "#FFCC33",
    "Ice": "#66CCFF",
    "Fighting": "#BB5544",
    "Poison": "#AA5599",
    "Ground": "#DDBB55",
    "Flying": "#8899FF",
    "Psychic": "#FF5599",
    "Bug": "#AABB22",
    "Rock": "#BBAA66",
    "Ghost": "#6666BB",
    "Dragon": "#7766EE",
    "Dark": "#775544",
    "Steel": "#AAAABB",
    "Fairy": "#EE99EE",
    "Normal": "#AAAA99",
}

TYPE_TEXT = {k: "white" for k in TYPE_COLORS}
TYPE_TEXT["Electric"] = "#333"
TYPE_TEXT["Ice"] = "#333"
TYPE_TEXT["Normal"] = "#333"
TYPE_TEXT["Steel"] = "#333"


def build_folium_map(filtered: pd.DataFrame):
    """Build a Folium map with watercolor background and click popups w/ sprite + stats."""
    import folium
    from folium.plugins import MarkerCluster

    center_lat = filtered["lat"].mean()
    center_lon = filtered["lon"].mean()

    # Watercolor tile background — painterly and memorable
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=3,
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="© Stadia Maps © Stamen Design © OpenMapTiles © OpenStreetMap contributors",
        prefer_canvas=True,
    )

    # # Faint label overlay so country/city names are still readable
    # folium.TileLayer(
    #     tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    #     attr="© OpenStreetMap contributors",
    #     name="Labels",
    #     overlay=True,
    #     control=False,
    #     opacity=0.45,
    # ).add_to(m)

    # Cluster for performance
    cluster = MarkerCluster(
        options={
            "maxClusterRadius": 40,
            "spiderfyOnMaxZoom": True,
            "showCoverageOnHover": False,
            "zoomToBoundsOnClick": True,
        }
    ).add_to(m)

    def stat_bar_html(val, max_val, color):
        pct = min(100, int(val / max_val * 100))
        return (
            f"<div style='background:#eee;border-radius:3px;height:6px;width:100%;margin:2px 0'>"
            f"<div style='background:{color};width:{pct}%;height:6px;border-radius:3px'></div>"
            f"</div>"
        )

    for _, row in filtered.iterrows():
        dex_id = get_pokemon_id(row)
        name = str(row["Name"])
        type1 = str(row.get("Type 1", "Normal"))
        type2 = str(row.get("Type 2", "")) if pd.notna(row.get("Type 2")) else ""
        total = int(row["Total"])
        hp = int(row["HP"])
        atk = int(row["Attack"])
        def_ = int(row["Defense"])
        sp_atk = int(row["Sp. Atk"])
        sp_def = int(row["Sp. Def"])
        speed = int(row["Speed"])
        gen = int(row["Generation"])
        legend = str(row["Legendary"]).upper() == "TRUE"
        sprite = sprite_url(dex_id)

        t1_col = TYPE_COLORS.get(type1, "#888888")
        t1_txt = TYPE_TEXT.get(type1, "white")

        # Type badge HTML
        type_badges = (
            f"<span style='background:{t1_col};color:{t1_txt};padding:2px 8px;"
            f"border-radius:999px;font-size:11px;font-weight:700'>{type1}</span>"
        )
        if type2:
            t2_col = TYPE_COLORS.get(type2, "#888888")
            t2_txt = TYPE_TEXT.get(type2, "white")
            type_badges += (
                f"&nbsp;<span style='background:{t2_col};color:{t2_txt};padding:2px 8px;"
                f"border-radius:999px;font-size:11px;font-weight:700'>{type2}</span>"
            )

        legendary_badge = ""
        if legend:
            legendary_badge = (
                "&nbsp;<span style='background:#FFD700;color:#333;padding:2px 7px;"
                "border-radius:999px;font-size:10px;font-weight:800'>★ LEGENDARY</span>"
            )

        popup_html = f"""
        <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap" rel="stylesheet"/>
        <div style="font-family:'Nunito',sans-serif;width:230px;border-radius:10px;
                    overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.2)">
          <!-- Header with sprite -->
          <div style="background:{t1_col};padding:12px;text-align:center">
            <img src="{sprite}" width="96" height="96"
                 style="image-rendering:pixelated;filter:drop-shadow(0 3px 8px rgba(0,0,0,.5))"
                 onerror="this.style.display='none'"/>
          </div>
          <!-- Body -->
          <div style="padding:10px 14px;background:white">
            <div style="font-size:16px;font-weight:800;color:#1a2475;margin-bottom:3px">
              #{dex_id:03d} {name}
            </div>
            <div style="margin-bottom:5px">{type_badges}{legendary_badge}</div>
            <div style="font-size:11px;color:#888;margin-bottom:6px">Generation {gen}</div>
            <hr style="margin:6px 0;border:none;border-top:1px solid #eee"/>
            <!-- Stat bars -->
            <table style="width:100%;font-size:11px;border-collapse:collapse">
              <tr>
                <td style="color:#888;width:50px;padding:1px 0">HP</td>
                <td style="font-weight:800;width:28px;text-align:right;color:#333">{hp}</td>
                <td style="padding-left:6px">{stat_bar_html(hp, 255, "#FF5959")}</td>
              </tr>
              <tr>
                <td style="color:#888;padding:1px 0">Attack</td>
                <td style="font-weight:800;text-align:right;color:#333">{atk}</td>
                <td style="padding-left:6px">{stat_bar_html(atk, 190, "#F5AC78")}</td>
              </tr>
              <tr>
                <td style="color:#888;padding:1px 0">Defense</td>
                <td style="font-weight:800;text-align:right;color:#333">{def_}</td>
                <td style="padding-left:6px">{stat_bar_html(def_, 230, "#FAE078")}</td>
              </tr>
              <tr>
                <td style="color:#888;padding:1px 0">Sp.Atk</td>
                <td style="font-weight:800;text-align:right;color:#333">{sp_atk}</td>
                <td style="padding-left:6px">{stat_bar_html(sp_atk, 194, "#9DB7F5")}</td>
              </tr>
              <tr>
                <td style="color:#888;padding:1px 0">Sp.Def</td>
                <td style="font-weight:800;text-align:right;color:#333">{sp_def}</td>
                <td style="padding-left:6px">{stat_bar_html(sp_def, 230, "#A7DB8D")}</td>
              </tr>
              <tr>
                <td style="color:#888;padding:1px 0">Speed</td>
                <td style="font-weight:800;text-align:right;color:#333">{speed}</td>
                <td style="padding-left:6px">{stat_bar_html(speed, 180, "#FA92B2")}</td>
              </tr>
            </table>
            <div style="margin-top:8px;text-align:right;font-size:12px;
                        color:#3B4CCA;font-weight:800">
              Total: {total}
            </div>
          </div>
        </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=7,
            color="white",
            weight=1.5,
            fill=True,
            fill_color=t1_col,
            fill_opacity=0.9,
            tooltip=folium.Tooltip(f"#{dex_id:03d} {name}", sticky=False),
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(cluster)

    return m


def run_assignment() -> None:
    """Run the Streamlit app for Assignment 2."""
    st.set_page_config(layout="wide", page_title="Pokémon World Map")

    st.markdown(
        """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;600;700;800&display=swap');

      html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

      h1 { font-family: 'Press Start 2P', monospace !important;
           font-size: 1.4rem !important; color: #FFCB05 !important;
           text-shadow: 3px 3px 0 #3B4CCA, -1px -1px 0 #3B4CCA; }

      .stTabs [data-baseweb="tab"] { font-family: 'Nunito', sans-serif;
           font-weight: 700; font-size: 1rem; }

      .metric-card { background: linear-gradient(135deg, #3B4CCA 0%, #1a2475 100%);
           border-radius: 12px; padding: 1rem 1.4rem; color: white; text-align: center;
           box-shadow: 0 4px 15px rgba(59,76,202,.35); }
      .metric-card .num { font-size: 2rem; font-weight: 800; color: #FFCB05; }
      .metric-card .lbl { font-size: .8rem; opacity: .85; text-transform: uppercase;
           letter-spacing: .05em; }

      .sidebar-header { font-family: 'Press Start 2P', monospace;
           font-size: .6rem; color: #3B4CCA; margin-bottom: .5rem; }

      .map-hint { background: rgba(59,76,202,.07); border-left: 3px solid #3B4CCA;
           padding: .45rem .8rem; border-radius: 0 6px 6px 0; font-size: .85rem;
           color: #3B4CCA; margin-bottom: .75rem; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("⚡ Pokémon World Map")
    st.caption("Explore where Pokémon have been spotted across the globe")

    pokemon_df = load_data()
    map_df = prepare_map_data(pokemon_df)

    # ── Sidebar Filters ──────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<p class="sidebar-header">🔍 Filters</p>', unsafe_allow_html=True)

        all_types = sorted(
            set(map_df["Type 1"].dropna().unique())
            | set(map_df["Type 2"].dropna().unique())
        )
        selected_types = st.multiselect(
            "Type",
            options=all_types,
            default=[],
            placeholder="All types",
        )

        generations = sorted(map_df["Generation"].dropna().unique().astype(int))
        selected_gens = st.multiselect(
            "Generation",
            options=generations,
            default=[],
            format_func=lambda g: f"Gen {g}",
            placeholder="All generations",
        )

        legendary_choice = st.radio(
            "Legendary status",
            options=["All", "Legendary only", "Non-legendary only"],
            index=0,
        )

        st.divider()

        stat_min, stat_max = int(map_df["Total"].min()), int(map_df["Total"].max())
        total_range = st.slider(
            "Base Stat Total",
            min_value=stat_min,
            max_value=stat_max,
            value=(stat_min, stat_max),
            step=5,
        )

    # ── Apply Filters ────────────────────────────────────────────────────────
    filtered = map_df.copy()

    if selected_types:
        mask = filtered["Type 1"].isin(selected_types) | filtered["Type 2"].isin(
            selected_types
        )
        filtered = filtered[mask]

    if selected_gens:
        filtered = filtered[filtered["Generation"].astype(int).isin(selected_gens)]

    if legendary_choice == "Legendary only":
        filtered = filtered[filtered["Legendary"].astype(str).str.upper() == "TRUE"]
    elif legendary_choice == "Non-legendary only":
        filtered = filtered[filtered["Legendary"].astype(str).str.upper() != "TRUE"]

    filtered = filtered[
        (filtered["Total"] >= total_range[0]) & (filtered["Total"] <= total_range[1])
    ]

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_overview, tab_charts, tab_table = st.tabs(["🗺️ Map", "📊 Charts", "📋 Table"])

    # ── MAP TAB ──────────────────────────────────────────────────────────────
    with tab_overview:
        c1, c2, c3, c4 = st.columns(4)
        for col, num, label in [
            (c1, len(filtered), "Pokémon shown"),
            (c2, filtered["Name"].nunique(), "Unique species"),
            (c3, filtered["Type 1"].nunique(), "Types represented"),
            (
                c4,
                (filtered["Legendary"].astype(str).str.upper() == "TRUE").sum(),
                "Legendaries",
            ),
        ]:
            col.markdown(
                f'<div class="metric-card"><div class="num">{num}</div>'
                f'<div class="lbl">{label}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(
            '<div class="map-hint">🖱️ <b>Click any dot</b> to reveal its sprite and full stats. '
            "Clusters expand on click — zoom in for individual Pokémon.</div>",
            unsafe_allow_html=True,
        )

        if filtered.empty:
            st.warning(
                "No Pokémon match the current filters. Try broadening your selection!"
            )
        else:
            try:
                from streamlit_folium import st_folium

                folium_map = build_folium_map(filtered)
                st_folium(
                    folium_map,
                    use_container_width=True,
                    height=560,
                    returned_objects=[],
                )
            except ImportError:
                st.error(
                    "📦 `folium` and `streamlit-folium` are required for the map.\n\n"
                    "```\npip install folium streamlit-folium\n```"
                )

            # Type legend
            present_types = filtered["Type 1"].dropna().unique()
            legend_html = (
                "<div style='display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.75rem;'>"
            )
            for t in sorted(present_types):
                c = TYPE_COLORS.get(t, "#888")
                txt = TYPE_TEXT.get(t, "white")
                legend_html += (
                    f"<span style='background:{c};color:{txt};padding:.2rem .6rem;"
                    f"border-radius:999px;font-size:.75rem;font-weight:700'>{t}</span>"
                )
            legend_html += "</div>"
            st.markdown("**Type legend:**")
            st.markdown(legend_html, unsafe_allow_html=True)

    # ── CHARTS TAB ──────────────────────────────────────────────────────────
    with tab_charts:
        if filtered.empty:
            st.info("No data to chart with current filters.")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Pokémon per Type")
                type_counts = (
                    filtered.groupby("Type 1")
                    .size()
                    .reset_index(name="Count")
                    .sort_values("Count", ascending=False)
                )
                st.bar_chart(type_counts.set_index("Type 1")["Count"])
            with col_b:
                st.subheader("Pokémon per Generation")
                gen_counts = (
                    filtered.groupby("Generation")
                    .size()
                    .reset_index(name="Count")
                    .sort_values("Generation")
                )
                gen_counts["Generation"] = gen_counts["Generation"].apply(
                    lambda g: f"Gen {int(g)}"
                )
                st.bar_chart(gen_counts.set_index("Generation")["Count"])

            st.subheader("Base Stat Total Distribution")
            hist_data = filtered["Total"].value_counts().sort_index().reset_index()
            hist_data.columns = ["Base Stat Total", "Count"]
            st.bar_chart(hist_data.set_index("Base Stat Total"))

    # ── TABLE TAB ────────────────────────────────────────────────────────────
    with tab_table:
        st.subheader(f"Filtered Pokémon — {len(filtered)} entries")
        display_cols = [
            "Name",
            "Type 1",
            "Type 2",
            "Total",
            "HP",
            "Attack",
            "Defense",
            "Sp. Atk",
            "Sp. Def",
            "Speed",
            "Generation",
            "Legendary",
        ]
        st.dataframe(
            filtered[display_cols].reset_index(drop=True),
            use_container_width=True,
            height=500,
        )


if __name__ == "__main__":
    run_assignment()
