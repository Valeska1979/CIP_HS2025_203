import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read CSV
df = pd.read_csv("jobs_ch_tasks_overview1.csv", sep=';')

# Sort by Unique_Ads descending
df = df.sort_values(by="Unique_Ads", ascending=False)

# Custom color palette (distinct and vivid)
custom_colors = [
    "#d73027",  # red
    "#fc8d59",  # orange
    "#fee08b",  # yellow
    "#91cf60",  # green
    "#3288bd",  # blue
    "#984ea3",  # purple
    "#f781bf",  # pink
    "#999999"   # grey
]

# Repeat colors if needed
colors = (custom_colors * ((len(df) // len(custom_colors)) + 1))[:len(df)]

# Create figure
fig, ax = plt.subplots(figsize=(8, 5))

# Draw bars
bars = ax.barh(range(len(df)), df["Unique_Ads"], color=colors, edgecolor='black', height=0.4)

# Invert Y-axis (largest bar at top)
ax.invert_yaxis()

# Remove y-axis ticks
ax.set_yticks([])

# Axis labels and title
ax.set_xlabel("Unique Ads")
ax.set_title("Unique Ads per Skills")

# Compute vertical spacing adjustment
label_shift_y = 0.3  # distance above bars for skill names
xshift_label = 2      # minimum horizontal shift for skill text
xshift_value = 6      # x-shift for numeric labels at bar ends

# Add skill labels above each bar
for bar, skill in zip(bars, df["Topic"]):
    y_pos = bar.get_y() + bar.get_height() + label_shift_y
    x_pos = bar.get_x() + max(xshift_label, bar.get_width() * 0.02)
    ax.text(x_pos, y_pos, skill, ha='left', va='bottom', fontsize=9, fontweight='bold')

# Add numeric labels with horizontal offset
for bar in bars:
    width = bar.get_width()
    ax.text(width + xshift_value, bar.get_y() + bar.get_height() / 2,
            f'{int(width)}', va='center', fontsize=9)

# Adjust y-limits to make top/bottom spacing symmetric
top_bar_y = bars[0].get_y()
bottom_bar_y = bars[-1].get_y() + bars[-1].get_height()
extra_space = label_shift_y + 0.2  # same distance as top spacing
ax.set_ylim(bottom_bar_y + extra_space, top_bar_y - extra_space)

# Clean layout
plt.tight_layout()
plt.show()