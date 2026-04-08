---
title: Streamlit Workshop - Deel 3
theme: advanced
---

<h1 style="font-size: 1.3em;">Streamlit: Advanced stuff...</h1>

<h3 style="font-size: 0.8em;">Deel 3: Let the games begin!</h3>

---

### 🌍 Publishing

<div style="font-size: 0.55em; margin: 30px 0px;">

### ☁️ **Streamlit Community Cloud** — gratis hosting voor je apps

1. Push je code naar **GitHub**
2. Ga naar [share.streamlit.io](https://share.streamlit.io)
3. Verbind je repo → kies `app.py` → klik **Deploy**

```
https://jouw-naam-jouw-repo-app-xyz123.streamlit.app  🎉
```

<br>

### 🔒 **Secrets beheren**
```python
# secrets.toml (lokaal, NIET in git!)
# [database]
# password = "super_secret"

# In je app:
import streamlit as st

db_password = st.secrets["database"]["password"]
api_key = st.secrets["API_KEY"]
```

Secrets stel je in via de Community Cloud UI — nooit in je code!

</div>

---

### 🌍 Publishing — Vereisten

<div style="font-size: 0.55em; margin: 30px 0px;">

### 📦 **Wat heb je nodig?**

| Bestand | Doel |
|---|---|
| `app.py` | Je Streamlit app |
| `requirements.txt` of `pyproject.toml` | Dependencies |
| (optioneel) `.streamlit/secrets.toml` | Lokale secrets |

<br>

### ✅ **Checklist voor deployment**
```
☐ requirements.txt bevat alle imports
☐ Geen hardcoded secrets in je code
☐ Data bestanden staan in de repo of via URL
☐ App draait lokaal zonder fouten
☐ GitHub repo is public (geen harde eis)
```

<br>

💡 **Alternatief:** Deploy ook op **Azure**, **GCP**, **AWS** of **Docker**s

</div>

---

### 🔐 OAuth out of the box

<div style="font-size: 0.55em; margin: 30px 0px;">

### 🆕 **Ingebouwde authenticatie**

Streamlit heeft native ondersteuning voor OAuth — geen extra libraries nodig!

```toml
# .streamlit/secrets.toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "een-willekeurig-geheim"

[auth.google]
client_id = "jouw-google-client-id"
client_secret = "jouw-google-client-secret"
```

```python
import streamlit as st

# Login knop
st.login()  # Toont login popup

# Check of gebruiker is ingelogd
if not st.user.is_logged_in:
    st.stop()  # Stop de app voor niet-ingelogde gebruikers

# Gebruik gebruikersinfo
st.write(f"Welkom, {st.user.name}! 👋")
st.write(f"Email: {st.user.email}")

# Logout knop
if st.button("Uitloggen"):
    st.logout()
```

</div>

---

### 🔐 OAuth — Ondersteunde Providers

<div style="font-size: 0.5em; margin: 30px 0px;">

### 🌐 **Werkt out of the box met:**

<div style="text-align: left; margin-left: 40px;">

🔵 **Google** — `[auth.google]`  
🟣 **Microsoft / Entra ID** — `[auth.microsoft]`  
⚫ **GitHub** — `[auth.github]`  
🟠 **Okta** — `[auth.okta]`  
🔧 **Elke OpenID Connect provider** — `[auth.oidc]`

</div>

<br>

### 🛡️ **Toegang beperken per gebruiker**
```python
import streamlit as st

ALLOWED_EMAILS = ["alice@bedrijf.nl", "bob@bedrijf.nl"]

st.login("google")

if not st.user.is_logged_in:
    st.stop()

if st.user.email not in ALLOWED_EMAILS:
    st.error("❌ Geen toegang. Neem contact op met de beheerder.")
    st.stop()

st.success(f"✅ Welkom {st.user.name}!")
```

</div>

---

### 📄 Multiple Pages

<div style="font-size: 0.65em; margin: 30px 0px;">

### 🗂️ **Methode 1: `pages/` map** — eenvoudigst

```
mijn_app/
├── app.py          ← Hoofdpagina
├── pages/
│   ├── 1_📊_Dashboard.py
│   ├── 2_🔍_Zoeken.py
│   └── 3_⚙️_Instellingen.py
└── requirements.txt
```

Streamlit detecteert automatisch de `pages/` map en voegt een **sidebar navigatie** toe — geen extra code nodig!

<br>

### 💡 **Naamgeving truc:**
```
1_Pagina_Naam.py  →  "Pagina Naam"   (cijfer = volgorde)
🔥_Fire_Types.py  →  "Fire Types"    (emoji werkt ook!)
```

</div>

---

### 📄 Multiple Pages — `st.navigation`

<div style="font-size: 0.55em; margin: 30px 0px;">

### 🚀 **Methode 2: `st.navigation()`** — meer controle

```python
# app.py
import streamlit as st

# Definieer pagina's als objecten
dashboard = st.Page("pages/dashboard.py", title="📊 Dashboard", icon="📊")
zoeken    = st.Page("pages/zoeken.py",    title="🔍 Zoeken",    icon="🔍")
instellingen = st.Page(
    "pages/instellingen.py",
    title="⚙️ Instellingen",
    icon="⚙️",
    default=True  # Standaard pagina
)

# Groepeer pagina's
pg = st.navigation({
    "Overzicht": [dashboard],
    "Tools": [zoeken, instellingen],
})

pg.run()  # Voer de actieve pagina uit
```

<br>

✅ **Voordelen:** Dynamische navigatie, pagina's verbergen, eigen sidebar layout

</div>

---

### 📄 Multiple Pages — Gedeelde State

<div style="font-size: 0.55em; margin: 30px 0px;">

### 🔗 **Data delen tussen pagina's**

`st.session_state` werkt over alle pagina's heen!

```python
# pages/zoeken.py
import streamlit as st

st.title("🔍 Zoeken")

pokemon_naam = st.text_input("Zoek een Pokemon")

if st.button("Zoek"):
    st.session_state.geselecteerde_pokemon = pokemon_naam
    st.switch_page("pages/dashboard.py")  # Navigeer naar andere pagina
```

```python
# pages/dashboard.py
import streamlit as st

st.title("📊 Dashboard")

# Lees data van de andere pagina
if "geselecteerde_pokemon" in st.session_state:
    pokemon = st.session_state.geselecteerde_pokemon
    st.write(f"Stats voor: **{pokemon}**")
else:
    st.info("Ga naar 'Zoeken' om een Pokemon te selecteren.")
```

<br>

💡 `st.switch_page()` laat je navigeren tussen pagina's

</div>

---

#### 🏆 Deel 3: Bouw de beste Pokémon app!

<div style="font-size: 0.65em; margin: 30px 0px 30px 0px; line-height: 1.6; text-align: left;">

Jullie bouwen **in groepen** de ultieme Pokémon Streamlit app. Aan het einde kiezen we een winnaar! 🥇

</div>

<div style="font-size: 0.45em; margin: 10px 0px; line-height: 1.6; text-align: left;">

### 💡 Ideeën om mee te starten (of te combineren!)

| Idee | Wat je nodig hebt |
|---|---|
| 📖 **Pokédex** | Zoek op naam, toon sprite + alle stats, type badge |
| ⚔️ **Battle Arena** | Vergelijk 2 Pokémon, simuleer een gevecht op basis van stats |
| 📊 **Stats Dashboard** | Radar chart, histogrammen |
| 🦁 **Leaderboard** | top-10 lijsten per stat of combinatie van stats |
| 🌍 **Interactieve Kaart** | Geo-data van Pokémon → `px.scatter_geo` of `st.map` |
| 🔢 **Type Calculator** | Welke types zijn sterk/zwak tegen elkaar? |

</div>

<div style="font-size: 0.5em; margin: 20px 0px 10px 0px; line-height: 1.6; text-align: left;">

### 🗂️ Beschikbare data

- `Pokemon_Stats.csv` — stats, type, generatie, legendary, etc.
- **Geo-data** — locaties waar Pokémon voorkomen *(tip: `location` kolom!)*
- Sprites (zie URL in readme)

</div>

---

<div style="text-align: center; padding: 2em 0;">

## Einde Deel 3

<div style="margin-top: 2em; display: flex; gap: 1.5em; justify-content: center; flex-wrap: wrap;">
  <a href="index.html" style="padding: 0.7em 1.4em; background: #0f3460; color: #c0d0e0; border-radius: 8px; text-decoration: none; font-size: 1em; font-weight: 600;">🏠 Terug naar index</a>
</div>

</div>
