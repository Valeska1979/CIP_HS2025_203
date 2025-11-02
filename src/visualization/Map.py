import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load GeoJSON and reproject
# Load GeoJSON and reproject
geojson_url = "https://gist.githubusercontent.com/cmutel/a2e0f2e48278deeedf19846c39cee4da/raw/cantons.geojson"
gdf = gpd.read_file(geojson_url)

# Set CRS (the GeoJSON is in WGS84 latitude/longitude)
gdf.set_crs(epsg=4326, inplace=True)

# Reproject to Swiss coordinate system (CH1903+ / LV95)
gdf = gdf.to_crs(epsg=2056)

# Load job count CSV (semicolon-separated)
df_job_count = pd.read_csv("Job_count.csv", sep=";")
df_job_count.columns = df_job_count.columns.str.strip().str.lower()
df_job_count['canton'] = df_job_count['canton'].str.strip().str.upper()

# Merge
merged = gdf.merge(df_job_count, left_on='id', right_on='canton', how='left')

# Plot
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
