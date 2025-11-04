import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --- SETTINGS ---
x_offset = 0.05      # general horizontal offset for labels
y_offset = 0.03      # general vertical offset for labels
legend_x_offset = 0.8  # horizontal position of legend (0 = left, 1 = right)
legend_y_offset = 0.15  # vertical position of legend (0 = bottom, 1 = top)

# --- 1. Load canton geometry ---
geojson_url = "https://gist.githubusercontent.com/cmutel/a2e0f2e48278deeedf19846c39cee4da/raw/cantons.geojson"
gdf = gpd.read_file(geojson_url)
gdf['id'] = gdf['id'].str.strip().str.upper()

# --- 2. Load your CSV job counts ---
df_job_count = pd.read_csv("Job_per_canton.csv")
df_job_count.columns = df_job_count.columns.str.strip()
df_job_count['canton'] = df_job_count['canton'].str.strip().str.upper()
df_job_count['job_count'] = pd.to_numeric(df_job_count['job_count'], errors='coerce')

# --- 3. Merge to keep all cantons ---
merged = gdf.merge(df_job_count, left_on='id', right_on='canton', how='left')

# Replace NaN (no data) with 0
merged['job_count'] = merged['job_count'].fillna(0).astype(int)

# --- 4. Define classification bins ---
bins = [-1, 0, 2, 4, 9, 15, 30, 60, float('inf')]
labels = ['0', '1–2', '3–4', '5–9', '10–15', '16–30', '31–60', '61+']
colors = [
    '#f7fbff',
    '#deebf7',
    '#c6dbef',
    '#9ecae1',
    '#6baed6',
    '#4292c6',
    '#2171b5',
    '#08519c'
]

merged['job_class'] = pd.cut(merged['job_count'], bins=bins, labels=labels, include_lowest=True)
color_map = dict(zip(labels, colors))
merged['color'] = merged['job_class'].map(color_map).astype('object')

# --- 5. Plot ---
fig, ax = plt.subplots(figsize=(9, 9))
merged.plot(color=merged['color'], edgecolor='black', linewidth=0.5, ax=ax)

ax.set_title("Job Count by Canton (Switzerland)", fontsize=15)
ax.axis('off')
ax.set_aspect('equal')

# --- 6. Fix invalid geometries before computing centroids ---
merged["geometry"] = merged["geometry"].buffer(0)

# Try dissolving to get one geometry per canton
try:
    centroids = merged.dissolve(by="id", as_index=False)[["id", "geometry"]]
except Exception as e:
    print("⚠️ Dissolve failed, fallback to unique geometries:", e)
    centroids = merged.drop_duplicates(subset=["id"])[["id", "geometry"]]

centroids["centroid"] = centroids["geometry"].centroid

# --- 7. Manual fine-tuning for small or overlapping cantons ---
label_offsets = {
    "BS": (0.05, 0.05),
    "BL": (0.05, -0.02),
    "GE": (0.05, -0.05),
    "ZG": (0.03, 0.02),
    "SH": (0.05, 0.05),
    "TI": (0.00, -0.05)
}

# --- 8. Add canton labels + job counts ---
for _, row in centroids.iterrows():
    job_value = int(merged.loc[merged["id"] == row["id"], "job_count"].iloc[0])
    label = f"{row['id']} {job_value}"

    dx, dy = label_offsets.get(row["id"], (x_offset, y_offset))
    plt.text(
        row["centroid"].x + dx,
        row["centroid"].y + dy,
        label,
        ha='center', va='center', fontsize=8, color='black'
    )

# --- 9. Custom legend ---
legend_elements = [Patch(facecolor=c, edgecolor='black', label=l)
                   for l, c in zip(labels, colors)]

ax.legend(
    handles=legend_elements,
    title='Job Count',
    loc='center',
    bbox_to_anchor=(legend_x_offset, legend_y_offset),
    fontsize=8,
    title_fontsize=9,
    frameon=True
)

plt.tight_layout()
plt.show()