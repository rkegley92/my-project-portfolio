import pandas as pd
import plotly.express as px
from preswald import connect, get_df, text, table, plotly

connect()
df = get_df("worldcities")
df["population"] = pd.to_numeric(df["population"], errors="coerce")   # strings → numbers

# ───────────────────── 0. Overview blurb ──────────────────────────
total_cities    = len(df)
total_countries = df["country"].nunique()

text(f"""
# 🌍 World Cities Dashboard  

**Dataset summary**  
* {total_cities:,} rows, representing **{total_countries}** countries  
* Population field converted to numeric so charts and tables sort correctly  
* Bubble sizes on the map are proportional to population  
""")

# ───────────────────── 1. Top-20 table ────────────────────────────
top20_df = (
    df.nlargest(20, "population")
      [["city", "country", "population", "lat", "lng"]]
)

text("## 🌆  Top 20 Most-Populous Cities")
table(top20_df, filters=False)

text("""
The table is sorted by *population* (descending).  
Hover any city to see latitude/longitude; use the header filters (▲▼) to
narrow by country if you’re curious about a specific region.
""")

# ───────────────────── 2. Country drill-down table ────────────────
country_name = "India"                       # 👈 change to any country
country_df = (
    df[df["country"] == country_name]
      .sort_values("population", ascending=False)
      .head(15)
)

text(f"## 🏳️  Major Cities in {country_name}")
table(
    country_df,
    title=f"Top 15 Cities in {country_name}",
    filters=True,
)

text(f"""
This slice shows the **{country_name}** cities with the largest reported
populations.  
*Use the column filters to look for particular states or population bands.*
""")

# ───────────────────── 3. World bubble map ────────────────────────
fig_world = px.scatter_geo(
    df.dropna(subset=["population"]),
    lat="lat",
    lon="lng",
    hover_name="city",
    hover_data={"country": True, "population": ":,"},
    size="population",
    size_max=20,
    title="World Cities by Population",
    projection="natural earth",
)
plotly(fig_world)

text("""
### How to use the map  
* **Zoom & pan** to explore regions.  
* **Hover** a bubble to view city name, country and population.  
* Bubble **size** ≈ population (√-scaled for readability).  
""")

