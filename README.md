# 🎮 Streamlit Workshop — Pokémon Edition

Welkom bij de Streamlit Workshop! In 4 uur leer je hoe je interactieve data-apps bouwt met Python en Streamlit — aan de hand van een echte Pokédex dataset.

---

## 🗓️ Programma

| # | Onderdeel | Tijd |
|---|-----------|------|
| 🎤 | Presentatie 1: Introductie Streamlit | ~20 min |
| 💻 | **Opdracht 1: Pokémon Data Explorer** | ~35 min |
| 🎤 | Presentatie 2: Session State & Filters | ~20 min |
| 💻 | **Opdracht 2: Advanced Filters & Shareable Links** | ~35 min |
| 🎤 | Presentatie 3: Multipage Apps & Battle Mechanics | ~20 min |
| 🏆 | **Opdracht 3: De Grote Competitie** | ~50 min |

---

## ⚙️ Setup

```bash
# Installeer dependencies
uv sync

# Start je app
uv run streamlit run <path_to_app.py>
```

Je browser opent automatisch op `http://localhost:8501` 🎉

---

## 📊 Dataset

**`data/Pokemon_Stats.csv`** — 700+ Pokémon met de volgende kolommen:

| Kolom | Beschrijving |
|-------|-------------|
| `#` | Pokédex ID |
| `Name` | Naam |
| `Type 1` | Primair type |
| `Type 2` | Secundair type (kan leeg zijn) |
| `Total` | Totale stats |
| `HP` | Hit Points |
| `Attack` | Aanvalskracht |
| `Defense` | Verdediging |
| `Sp. Atk` | Speciale aanval |
| `Sp. Def` | Speciale verdediging |
| `Speed` | Snelheid |
| `Generation` | Generatie (1–7) |
| `Legendary` | Is het een legendarische Pokémon? |
| `location` | POINT object met lat lon gegevens |
| `Area (km)` | Oppervlak binnen POINT waarin pokemon te vinden is |

---

---

# 📗 Opdracht 1: Pokémon Data Explorer ⚡

> **Doel:** Bouw een interactieve Pokédex-verkenner om de dataset te verkennen en te visualiseren.

## Wat ga je bouwen?

Een app waarmee je voor een gegeven Pokémon dataset kunt een overzicht kan krijgen en de data kunt visualiseren via grafieken.

---

## ✅ Stap 1 — Dataset inladen

- 💾 Laad de CSV in data/Pokemon_Stats.csv in een **Pandas DataFrame**

---

## ✅ Stap 2 — Dataset overzicht

Toon de volgende **4 metrics** bovenaan je app (tip: gebruik `st.columns` en `st.metric`):

- 🔢 Totaal aantal Pokémon
- ⭐ Aantal legendarische Pokémon
- 🌍 Aantal generaties
- 🎨 Aantal unieke types (tel Type 1 én Type 2 mee!)

---

## ✅ Stap 3 — Visualisaties via tabs

Gebruik **`st.tabs`** om vijf tab bladen te scheiden:

### 🔢 Tab 1: Metrics
- Verplaats de metrics uit stap 2 naar zijn eigen tab

### 📊 Tab 2: Type distributie
- Bar chart van hoeveel Pokémon per type (`Type 1`)
- Gebruik `st.bar_chart` of Plotly

### 💥 Tab 3: Attack vs Defense scatter plot
- Scatter plot van `Attack` vs `Defense`
- Filter op **één type** naar keuze (bijv. Water, Fire, Grass...)
- Gebruik `st.scatter_chart` of Plotly

### 🏅 Tab 4: Top 10 Pokémon
- Laat de gebruiker kiezen welke stat ze willen ranken: `HP`, `Attack`, `Defense`, `Sp. Atk`, `Sp. Def`, `Speed`
- Toon de top 10 Pokémon op basis van de gekozen stat
- Gebruik een bar chart

### 🛡️⚡🔥💧🌿❄️ Tab 5: Random team creator
- Maak een knop die de DataFrame index van een random pokemon kiest.
- Voeg deze index toe aan een lijst (waarom is hier session state nodig?)
- Laat met behulp van `st.dataframe` het gegenereerde team zien.

---

# 📘 Opdracht 2: Advanced Filters & Shareable Links 🎯

> **Doel:** Bouw een geavanceerde filter-tool met cascading filters, session state en deelbare URLs.

## Wat ga je bouwen?

Een app met meerdere filters die elkaar beïnvloeden, waarbij de filterstand wordt opgeslagen in de URL zodat je hem kunt delen.

---

## ✅ Part A — Cascading Filters 🧩

### Stap 1: Laad de data en toon de tabel

- Laad de CSV in data/Pokemon_Stats.csv in een **Pandas DataFrame**
- Toon de Pokémon in een **interactieve tabel** met `st.dataframe`
- Toon hoeveel Pokémon er na het filteren overblijven: `"X Pokémon gevonden"`

---

### Stap 2: Bouw 4 filters die elkaar beïnvloeden

De filters moeten **in volgorde** werken: elke filter beperkt de opties van de volgende.

| Filter | Widget | Werking |
|--------|--------|---------|
| 🌍 Generatie | `st.multiselect` | Selecteer 1 of meer generaties → beïnvloedt beschikbare types |
| 🎨 Type | `st.selectbox` | Kies een type (alleen types uit geselecteerde generaties) → beïnvloedt de Pokémon lijst |
| ⭐ Legendary | `st.radio` | Kies: Alle / Alleen Legendary / Geen Legendary |
| 💪 Minimum stat | `st.slider` | Stel een minimum in voor een gekozen stat (bijv. HP ≥ 50) |

- Toon hoeveel Pokémon er na het filteren overblijven: `"X Pokémon gevonden"`

---

## ✅ Part B — Shareable Filter Links 🔗

### Stap 1: Sla filters op in de URL

- Voeg `key=` toe aan de widgets zodat elke filterwijziging opgeslagen wordt in de URL query parameters
- Voeg `bind=` toe zodat de widget waardes uit de URL worden geladen


### Stap 2: Share knop

- Voeg een **"🔗 Kopieer link"** button toe  <--- DONT KNOW HOW YET
- Toon een `st.success` melding na het klikken

### Stap 3: Reset knop

- Voeg een **"🔄 Reset filters"** button toe die:
  - Alle filters terugzet naar een beginstand  
  - De pagina herlaadt met `st.rerun()`

---

### 🧪 Test je implementatie

1. Stel filters in
2. Kopieer de URL
3. Open de URL in een nieuw tabblad
4. ✅ Filters moeten identiek zijn!

---

## 🎁 Bonus: Team Builder

- Voeg een **multiselect** toe waarmee de gebruiker 6 Pokémon kan kiezen voor hun team
- Toon gecombineerde teamstatistieken (totale HP, Attack, Defense, enz.)
- Visualiseer de **type coverage**: welke types heeft je team gedekt?
- Sla het team op in `st.session_state` zodat het bewaard blijft

---

# 🏆 Opdracht 3: De Grote Competitie — Bouw je eigen Pokédex App!

> **Doel:** Bouw een complete multipage Pokémon-app met een turn-based battle game, Pokémon management en een leaderboard.

## Wat ga je bouwen?

Een volledige app met meerdere pagina's, een battle game, en zoveel mogelijk Streamlit-features. Dit is de **competitie-opdracht** — de beste app wint! 🥇

---

## 🗺️ App structuur (multipage)

Gebruik Streamlit's multipage-functionaliteit (`pages/` map of `st.navigation`):

```
📁 pages/
   🏠 1_Home.py          → Overzicht & statistieken
   ⚔️  2_Battle.py        → Turn-based battle game
   📋 3_Pokemon.py       → Pokémon management & team builder
   🏆 4_Leaderboard.py   → Scores & ranglijst
```

---

## ✅ Pagina 1 — Home

- Overzicht van de volledige Pokédex (gebruik wat je al hebt van Opdracht 1)
- Zoekfunctie op naam
- Statistieken (totaal, types, generaties)

---

## ✅ Pagina 2 — Battle Game ⚔️

Bouw een **turn-based Pokémon battle** tegen een willekeurige tegenstander:

### Battle mechanica (basis):
- 🎮 Kies je Pokémon (uit je team of vrij)
- 🤖 De tegenstander kiest een willekeurige Pokémon
- 🔁 Beurten: jij kiest een move → tegenstander doet een move
- ❤️ HP daalt op basis van `Attack` vs `Defense` berekening
- 🏁 Battle eindigt als HP van één van de twee op 0 staat

### Basis aanvalsformule:
```python
schade = max(1, aanvaller_attack - verdediger_defense // 2)
```

### UI vereisten:
- Toon HP van beide Pokémon (gebruik `st.progress` voor health bars)
- Toon de battle log (wat er elke beurt gebeurde)
- Toon het resultaat: gewonnen of verloren
- Sla de score op in `st.session_state`

---

## ✅ Pagina 3 — Pokémon Management 📋

- Zoek en bekijk Pokémon (met afbeeldingen via PokeAPI  https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png)
- Stel je team samen (max 6 Pokémon)
- Toon teamstatistieken en type coverage
- Sla je team op in `st.session_state`

---

## ✅ Pagina 4 — Leaderboard 🏆

- Toon de battle-resultaten van de huidige sessie
- Ranglijst: meeste overwinningen, hoogste score
- Reset-knop om de scores te wissen

---

## 🥇 Beoordelingscriteria

| Criterium | Beschrijving |
|-----------|-------------|
| 🥇 **Beste battle game** | Meeste features, mooiste mechanics |
| 🎨 **Mooiste UI/styling** | Custom CSS, mooie layout, Pokédex-gevoel |
| 🏃 **Snelste completion** | Alle opdrachten (1+2+3) afgerond |
| 🎚️ **Meeste widgets** | `file_uploader`, `slider`, `tabs`, `columns`, `metric`, `image`, `download_button`, etc. |
| 🧪 **Beste app tests** | Pytest / Streamlit testing |

---

## 🎁 Extra ideeën

- 🌟 **Type-voordelen** in de battle (Water sterk tegen Fire, enz.)
- 💊 **Items** gebruiken tijdens battle (Potion, etc.)
- 🎵 **Geluidseffecten** via `st.audio`
- 📱 **Responsive layout** via `st.columns`
- 🌈 **Custom theming** via `.streamlit/config.toml`
- 📸 **Animaties** via Lottie of GIF-weergave

---

## 💡 Handige Streamlit cheatsheet

```python
# Layout
st.columns([1, 2, 1])       # Kolommen met verhoudingen
st.tabs(["Tab 1", "Tab 2"]) # Tabs
st.expander("Meer info")    # Uitklapbaar blok
st.sidebar                  # Zijbalk

# Data
st.dataframe(df)            # Interactieve tabel
st.metric("Label", waarde)  # KPI-kaartje
st.image(url)               # Afbeelding

# Widgets
st.selectbox(...)           # Dropdown
st.multiselect(...)         # Meerdere opties
st.slider(...)              # Schuifregelaar
st.radio(...)               # Keuzerondje
st.checkbox(...)            # Vinkje
st.button(...)              # Knop
st.download_button(...)     # Download

# State & navigatie
st.session_state            # Bewaar data tussen reruns
st.query_params             # Lees/schrijf URL parameters
st.rerun()                  # Herlaad de app
st.cache_data               # Cache zware berekeningen
```

---

Veel succes — en moge de beste trainer winnen! 🏆⚡
