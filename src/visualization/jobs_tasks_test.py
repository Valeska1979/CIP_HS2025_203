import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read CSV
df = pd.read_csv("jobs_ch_tasks_overview1.csv", sep=';')

# Sort by Unique_Ads descending
df = df.sort_values(by="Unique_Ads", ascending=False)

# Create a color gradient (dark red → orange → yellow)
cmap = plt.cm.autumn
colors = cmap(np.linspace(0, 1, len(df)))

# Create horizontal bars (thinner)
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(range(len(df)), df["Unique_Ads"], color=colors, edgecolor='black', height=0.45)

# Invert Y-axis so largest value on top
ax.invert_yaxis()

# Add title and axis labels
ax.set_xlabel("Unique Ads")
ax.set_title("Unique Ads per Skills")

# Remove y-axis tick labels (we’ll place names above bars instead)
ax.set_yticks([])

# Add skill labels above bars
for i, (bar, skill) in enumerate(zip(bars, df["Topic"])):
    ax.text(bar.get_x(), bar.get_y() + bar.get_height() + 0.1,
            skill, ha='left', va='bottom', fontsize=9, fontweight='bold')

# Add numeric values at the end of each bar
for bar in bars:
    width = bar.get_width()
    ax.text(width + 2, bar.get_y() + bar.get_height() / 2,
            f'{int(width)}', va='center')

# Tidy layout
plt.tight_layout()
plt.show()
