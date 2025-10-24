## 1. Here we display the jobcount per canton in a map
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# load the shape file of the cantons

geojson_url = "https://gist.githubusercontent.com/cmutel/a2e0f2e48278deeedf19846c39cee4da/raw/cantons.geojson"

gdf = gpd.read_file(geojson_url)

#check names
print(gdf.columns)
print(gdf.head())


# load the job count data
df_job_count = pd.read_csv("jobcount.csv")

# inspect
df_job_count = pd.read_csv("jobcount.csv")
print(df_job_count.columns)


#merge the data with shape of cantons
merged = gdf.merge(df_job_count,
                   left_on ='id',
                   right_on ='canton',
                   how='left'
)

print(merged[['id', 'canton', 'job_count']])
print(merged['job_count'].isna().sum(), "cantons missing data")

#  Plot map
fig, ax = plt.subplots(figsize=(8, 8))
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

# 5. Show (or save)
plt.show()
# plt.savefig("swiss_job_count_map.png", dpi=300, bbox_inches="tight")
