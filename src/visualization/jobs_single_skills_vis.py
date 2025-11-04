import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import sys


CSV_DELIMITER = ';'

def create_single_skill_visualization(input_file_path: Path, output_file_path: Path, show_plot: bool = False):
    # Check if file exists

    if not os.path.exists(input_file_path):

        print(f"ERROR: Input file not found: {input_file_path}")

        return False

    try:

        # Read CSV
        df = pd.read_csv(input_file_path, sep=CSV_DELIMITER)

        # Sort by Unique_Ads descending
        df = df.sort_values(by="Unique_Ads", ascending=False)

        # Custom color palette (distinct colors)
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

        # Repeat colors if fewer than needed
        colors = (custom_colors * ((len(df) // len(custom_colors)) + 1))[:len(df)]

        # Create figure
        fig, ax = plt.subplots(figsize=(8, 5))

        # Draw horizontal bars
        bars = ax.barh(range(len(df)), df["Unique_Ads"], color=colors, edgecolor='black', height=0.4)

        # Invert Y-axis (largest bar on top)
        ax.invert_yaxis()

        # Remove y-axis ticks
        ax.set_yticks([])

        # Axis labels and title
        ax.set_xlabel("Unique Ads")
        ax.set_title("Unique Ads per Skills")

        # Layout parameters
        label_shift_y = -0.45     # vertical shift for skill labels
        xshift_label = 2         # min horizontal shift for skill labels
        xshift_value = 2         # shift for numeric labels
        right_margin = 10       # space between longest number and right frame (adjustable)

        # Add skill labels above each bar
        for bar, skill in zip(bars, df["Skill"]):
            y_pos = bar.get_y() + bar.get_height() + label_shift_y
            x_pos = bar.get_x() + max(xshift_label, bar.get_width() * 0.02)
            ax.text(x_pos, y_pos, skill, ha='left', va='bottom', fontsize=9, fontweight='bold')

        # Add numeric labels (shifted slightly right)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + xshift_value, bar.get_y() + bar.get_height() / 2,
                    f'{int(width)}', va='center', fontsize=9)

        # Adjust Y-limits for equal top/bottom spacing
        top_bar_y = bars[0].get_y()
        bottom_bar_y = bars[-1].get_y() + bars[-1].get_height()
        extra_space = label_shift_y + 1
        ax.set_ylim(bottom_bar_y + extra_space, top_bar_y - extra_space)

        # Adjust X-limits to add right margin (for label-to-frame distance)
        max_width = df["Unique_Ads"].max()
        ax.set_xlim(0, max_width + right_margin)

        # Clean layout
        plt.tight_layout()

        # Save Plot

        os.makedirs(output_file_path.parent, exist_ok=True)

        plt.savefig(output_file_path, bbox_inches='tight')

        if show_plot:
            plt.show()
        else:
            plt.close(fig)

        print(f"SUCCESS: Single skill visualization saved to: {output_file_path}")

        return True


    except Exception as e:

        print(f"ERROR creating single skill visualization: {e}")

        return False


# --- STANDALONE EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- RUNNING SINGLE SKILL VISUALIZATION SCRIPT IN STANDALONE TEST MODE ---")

    # Define paths relative to this script
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent.parent
    ANALYSIS_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "analysis"
    REPORT_DIR_TEST = PROJECT_ROOT_TEST / "report" / "figures"


    TEST_INPUT_PATH = ANALYSIS_DATA_DIR_TEST / "jobs_ch_single_skills_analysis.csv"
    TEST_OUTPUT_PATH = REPORT_DIR_TEST / "required_single_skills.png"

    # Check if the required input file exists for testing
    if not os.path.exists(TEST_INPUT_PATH):
        print(f"WARNING: Cannot run standalone test. Test input file not found at: {TEST_INPUT_PATH}")
        print("Please ensure your Skills Analysis script has generated this file first.")
        sys.exit(1)

    # Run the jobs_single_skills_vis script
    success = create_single_skill_visualization(TEST_INPUT_PATH, TEST_OUTPUT_PATH, show_plot=True)

    if success:
        print("Standalone visualization jobs single skill run complete.")
    else:
        print("Standalone visualization jobs single skill run failed.")
