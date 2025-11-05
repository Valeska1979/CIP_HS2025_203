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
import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
import sys
from matplotlib.patches import Patch

CSV_DELIMITER = ";"

def create_canton_map_visualization(job_counts_input_path: Path, report_output_path: Path, job_per_canton_output_path: Path):
    try:
        # ----------------------------------------------------------
        # Load GeoJSON
        # ----------------------------------------------------------
        # For an undistorted map first the GeoJSON has to be loaded. Then the coordinate reference system (CRS) is set to
        # the GCS WGS 84 with the EPSG code 4326. Then it is reprojected to the swiss coordinate system with the EPSG 2056,
        # Load GeoJSON and reproject
        # --- 1. Load canton geometry ---
        geojson_url = "https://gist.githubusercontent.com/cmutel/a2e0f2e48278deeedf19846c39cee4da/raw/cantons.geojson"
        gdf = gpd.read_file(geojson_url)

        # Set CRS (the GeoJSON is in WGS84 latitude/longitude)
        gdf.set_crs(epsg=4326, inplace=True)

        # Reproject to Swiss coordinate system (CH1903+ / LV95)
        gdf = gdf.to_crs(epsg=2056)
        gdf['id'] = gdf['id'].str.strip().str.upper()

        # ----------------------------------------------------------
        # Load and clean the job count csv
        # ----------------------------------------------------------

        # Load job count csv
        df_job_count = pd.read_csv(job_counts_input_path, sep=CSV_DELIMITER)
        df_job_count.columns = df_job_count.columns.str.strip().str.lower()

        print("Columns:", df_job_count.columns.tolist())
        print(df_job_count.head())

        # map the different location to cantons
        # Mapping was done by hand since there are too many special cases and not many cases, so it would take more time
        # to program.
        # special cases:
        # and/or Locations resulting in different locations: first named assumed more relevant
        # Regions instead of cantons: canton with the biggest population, since there are in total
        # only 3 cases.
        location_to_canton = {
        "Zürich": "ZH", "Bern": "BE", "Geneva": "GE", "Zurich": "ZH",
        "Solothurn": "SO", "Winterthur": "ZH", "Lausanne": "VD", "Basel": "BS",
        "Luzern": "LU", "Urdorf": "ZH", "Mägenwil": "AG", "Lenzburg": "AG",
        "Burgdorf": "BE", "Genève": "GE", "Schlieren": "ZH", "Bottighofen": "TG",
        "Martigny": "VS", "Zürich und/oder Mägenwil": "ZH", "St. Gallen": "SG",
        "Echandens": "VD", "Frauenfeld": "TG", "St.Gallen": "SG", "Deutschschweiz": "ZH",
        "Zürich-Seefeld": 'ZH', "Allschwil": "BL", "6036 Dierikon": "LU", "Wollerau": "SZ",
        "Neuchâtel (Hybrid)": "NE", "Uzwil": "SG", "Laufenburg": "AG", "Bussnang": "TG",
        "Ibach-Schwyz": "SZ", "St. Gallen und/oder Zürich-Flughafen (The Circle)": "SG",
        "Emmen": "LU", "Balerna": "TI", "Nänikon-Greifensee": "ZH", "Kaiseraugst": "AG",
        "CH - Zürich": "ZH", "Zentralschweiz": "LU", "Egerkingen": "SO", "Sierre": "VS",
        "Härkingen": "SO", "Thun, Berne, Schweiz": "BE", "Goldau / Schwyz / Uetendorf / Thun": "SZ",
        "2606 Corgémont": "BE", "Graubünden, Grono or remote": "GR", "Tägerwilen": "TG",
        "Liebefeld": "BE", "Büren an der Aare": " BE", "Berna": "BE", "Zollikofen": "BE",
        "Lausanne, Switzerland": "VD", "Chiasso": "TI", "Landquart": "GR", "Baden": "AG",
        "Regensdorf": "ZH", "Dübendorf": "ZH", "Raum Bern und teilweise im Homeoffice": "BE",
        "Boudevilliers": "NE", "Pully": "VD", "Stabio": "TI", "Switzerland &gt; Basel : H-127 A2": "BS",
        "Bleichemattstrasse 31": "AG", "Volkestwil": "ZH", "Oerlikon": "ZH", "Rolle": "VD",
        "Prilly": "VD", "Reinach BL": "BL", "Bonaduz": "GR", "Hergiswil": "NW", "1211 GENEVE 11": "GE",
        "Villars-sur-Glâne": "VD", "1008 Prilly": "VD", "Rheinfelden": "AG", "Buchs AG": "AG",
        "Münchenstein Spenglerpark und mobiles Arbeiten": "BL", "Basel Hauptsitz/Siège": "BS"
        }

        #  Assign canton abbreviations to a new column
        df_job_count["canton"] = df_job_count["location"].map(location_to_canton)

        # Check for missing mappings from the manual assignments, errors included, misspellings in job ad, misspelling in
        # assignment, missed entries, all were fixed.
        missing = df_job_count[df_job_count["canton"].isna()]
        if not missing.empty:
            print("Missing canton assignments for:")
            print(missing["location"].unique())

        #  Aggregate job counts per canton
        df_per_canton = (
            df_job_count.groupby("canton", as_index=False)["job_count"]
            .sum()
            .sort_values("job_count", ascending=False)
        )

        df_per_canton['canton'] = df_per_canton['canton'].str.strip().str.upper()
        merged = gdf.merge(df_per_canton, left_on='id', right_on='canton', how='left')

        merged['job_count'] = merged['job_count'].fillna(0).astype(int)
        print(f"Merged cantons: {merged['job_count'].gt(0).sum()} with data out of {len(merged)} total.")

        # Save to new csv
        # Ensure the directory exists before saving
        os.makedirs(job_per_canton_output_path.parent, exist_ok=True)
        df_per_canton.to_csv(job_per_canton_output_path, index=False, encoding="utf-8")

        print(f"Saved as {job_per_canton_output_path}")

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
        bins = [-1, 0, 2, 4, 9, 15, 29, 59, float('inf')]
        labels = ['0', '1–2', '3–4', '5–9', '10–15', '16–29', '30–59', '60+']
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
        # --- SETTINGS ---
        x_offset = 0.05  # general horizontal offset for labels
        y_offset = 0.03  # general vertical offset for labels
        legend_x_offset = 0.9  # horizontal position of legend (0 = left, 1 = right)
        legend_y_offset = 0.8  # vertical position of legend (0 = bottom, 1 = top)

        # Plot
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
            print("Dissolve failed, fallback to unique geometries:", e)
            centroids = merged.drop_duplicates(subset=["id"])[["id", "geometry"]]

        centroids["centroid"] = centroids["geometry"].centroid

        # --- 7. Manual fine-tuning for small or overlapping cantons ---
        label_offsets = {
            "BS": (3000, 6000),
            "BL": (10000, -2000),
            "GE": (3800, 1200),
            "ZG": (7000, 8000),
            "SH": (-1000, 1000),
            "TI": (0, -5000),
            "VD": (-6000, 1000),  # Example: move Bern slightly left
            "LU": (4000, 2000),
            "SO": (5000, 1000),
            "AI": (-1000, 0),
            "AR": (-3000, 7000),
            "SG": (-8000, -3000),
            "OW": (-2000, 0),
            "NW": (2500, 2000),
            "ZG": (-1000, -1000)
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
        ax.set_xlim(merged.total_bounds[0] + 10000, merged.total_bounds[2] + 10000)
        ax.set_ylim(merged.total_bounds[1] - 10000, merged.total_bounds[3] + 10000)
        plt.tight_layout()
        plt.show()

        # saving the plot
        os.makedirs(report_output_path.parent, exist_ok=True)
        plt.savefig(report_output_path)  #

        plt.show()
        print(f"\nMap plot saved to: {report_output_path}")
        return True

    except Exception as e:
        print(f"ERROR during plot save: {e}")
        return False

# --- STANDALONE EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- RUNNING MAP VISUALIZATION SCRIPT IN STANDALONE TEST MODE ---")

    # Relative path definition for this script
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent.parent
    DATA_VIS_DIR_TEST = PROJECT_ROOT_TEST / "data" / "visualization"
    REPORT_DIR_TEST = PROJECT_ROOT_TEST / "report" / "figures"
    TEST_INPUT_PATH = DATA_VIS_DIR_TEST / "jobs_ch_location_counts_1.csv"
    TEST_job_per_canton_output_path = DATA_VIS_DIR_TEST / "Job_per_canton.csv"
    TEST_OUTPUT_PATH = REPORT_DIR_TEST / "jobs_maps_switzerland.png"

    if not TEST_INPUT_PATH.exists():
        print(f"ERROR: Input file not found at {TEST_INPUT_PATH}. Please ensure it exists.")
        sys.exit(1)

    # Call the main function
    if create_canton_map_visualization(TEST_INPUT_PATH, TEST_OUTPUT_PATH, TEST_job_per_canton_output_path):
        print("Standalone map visualization run complete.")
    else:
        print("Standalone map visualization run failed.")