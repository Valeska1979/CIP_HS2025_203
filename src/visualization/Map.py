# ==========================================================
# Map with job counts per canton
# ==========================================================
# Goal:
#   Show the number of jobs in each canton on a map.
#   Define groups referring the locations to the cantons.
#   Import the geo data frame, reference and reproject for undistorted map.
#   Join the datasets and create the graph
# Author: Julia Studer
# ==========================================================

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# For an undistorted map first the GeoJSON has to be loaded. Then the coordinate reference system (CRS) is set to
# the GCS WGS 84 with the EPSG code 4326. Then it is reprojected to the swiss coordinate system with the EPSG 2056,
# Load GeoJSON and reproject
geojson_url = "https://gist.githubusercontent.com/cmutel/a2e0f2e48278deeedf19846c39cee4da/raw/cantons.geojson"
gdf = gpd.read_file(geojson_url)

# Set CRS (the GeoJSON is in WGS84 latitude/longitude)
gdf.set_crs(epsg=4326, inplace=True)

# Reproject to Swiss coordinate system (CH1903+ / LV95)
gdf = gdf.to_crs(epsg=2056)

# Load and clean the job count csv
# Load job count csv (semicolon-separated)
df_job_count = pd.read_csv("data/analysis/jobs_ch_location_counts.csv", sep=";")
df_job_count.columns = df_job_count.columns.str.strip().str.lower()

# map the different location to cantons
# special cases:
# and/or Locations resulting in different locations: first named assumed more relevant
# Regions instead of cantons: canton with the biggest population, since there are in total
# only 3 cases.
location_to_canton = {
    "Zürich": "ZH",
    "Bern": "BE",
    "Geneva": "GE",
    "Zurich": "ZH",
    "Solothurn": "SO",
    "Winterthur": "ZH",
    "Lausanne": "VD",
    "Basel": "BS",
    "Luzern": "LU",
    "Urdorf": "ZH",
    "Mägenwil": "AG",
    "Lenzburg": "AG",
    "Burgdorf": "BE",
    "Genève": "GE",
    "Schlieren": "ZH",
    "Bottighofen": "TG",
    "Martigny": "VS",
    "Zürich und/oder Mägenwil": "ZH",
    "St. Gallen": "SG",
    "Echandens": "VD",
    "Frauenfeld": "TG",
    "St. Gallen": "SG",
    "Deutschschweiz": "ZH"
    "Zürich-Seefeld": "ZH",
    "Allschwil": "BL",
    "6036 Dierikon": "LU",
    "Wollerau": "SZ",
    "Neuchâtel (Hybrid)": "NE",
    "St.Gallen": "SG",
    "Uzwil": "SG",
    "Laufenburg": "AG",
    "Bussnang": "TG",
    "Ibach-Schwyz": "SZ",
    "St. Gallen und/oder Zürich-Flughafen": "SG"
    "Emmen": "LU",
    "Balerna": "TI",
    "Mänikon-Greifensee": "ZH",
    "Kaiseraugst": "AG",
    "CH - Zürich": "ZH",
    "Zentralschweiz": "LU",
    "Egerkingen": "SO",
    "Sierre": "VS",
    "Härkingen": "SO",
    "Thun, Berne, Schweiz": "BE",
    "Goldau / Schwyz / Uetendorf / Thun": "SZ",
    "2606 Corgémont": "BE",
    "Graubünden, Grono or remote": "GR",
    "Tägerwilen":"TG",
    "Liebefeld": "BE",
    "Büren an der Aare":
    "Berna": "BE"
    "Zollikofen": "BE"
    "Lausanne, Switzerland": "VD",
    "Chiasso": "TI",
    "Landquart: "GR",
    "Baden": "AG",
    "Regensdorf": "ZH",
    "Dübendorf": "ZH",
    "Raum Bern und teilweise im Homeoffice": "BE",
    "Boudevilliers": "NE",
    "Pully": "VD",
    "Stabio": "TI",
    "Switzerland &gt; Basel: H-127 A2": "BS",
    "Bleichemattstrasse 31": "AG",
    "Volketswil": "ZH",
    "Oerlikon": "ZH",
    "Rolle": "VD",
    "Prilly": "VD",
    "Reinach BL": "BL"
}

# Merge the job count df with the gdf
merged = gdf.merge(df_job_count, left_on='id', right_on='canton', how='left')

# Plot a map with an annotated cantons and colors for the different numbers of jobs, with tight boundaries
fig, ax = plt.subplots(figsize=(10, 7))
merged.plot(
    column='job_count',
    cmap='YlOrRd',
    legend=True,
    edgecolor='black',
    linewidth=0.5,
    ax=ax
)

ax.set_title("Job Count by Canton (Switzerland)", fontsize=14)
ax.axis('off')
ax.set_aspect('equal')

# Fit bounds
minx, miny, maxx, maxy = merged.total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

# Annotate canton codes
for idx, row in merged.iterrows():
    plt.annotate(
        text=row['id'],
        xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
        ha='center', fontsize=8, color='black'
    )

plt.tight_layout()
plt.show()
