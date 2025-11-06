# ==========================================================
# Bar diagram showing single skills and tools in unique ads
# ==========================================================
# Goal:
#   Show the number of unique ads per single skill and tool.
#   In the case of same amount of adds for different skills/tools, they are shown on the same bar.
#   Legend of the skills/tools above the bar, number of unique ads next to bar.
#   Use of distinguishable colours for each bar, similar to the map graph.
# Author: Julia Studer
# ==========================================================

import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt



CSV_DELIMITER = ';'

def create_single_skill_visualization(input_file_path: Path, output_file_path: Path, show_plot: bool = False):
    """Creates a horizontal bar chart showing Unique Ads per grouped skill count, using blue color grading."""
    # Check if file exists
    if not os.path.exists(input_file_path):
        print(f"ERROR: Input file not found: {input_file_path}")
        return False

    try:
        # ----------------------------------------------------------
        # Data preparation
        # ----------------------------------------------------------

        # Read csv
        df = pd.read_csv(input_file_path, sep=CSV_DELIMITER)

        # Sort by Unique_Ads descending and keep top 15
        df = df.sort_values(by="Unique_Ads", ascending=False).head(15)

        # Check if df is empty
        if df.empty:
            print(f"ERROR: No skills data available to plot. Check input CSV: {input_file_path}")
            return False

        # Ensure required columns exist
        for col in ["Skill", "Unique_Ads"]:
            if col not in df.columns:
                print(f"ERROR: Required column '{col}' not found in CSV.")
                return False

        # Group skills with same Unique_Ads count
        grouped = (
            df.groupby("Unique_Ads")["Skill"]
            .apply(lambda skills: " / ".join(skills))  # join with slash separator
            .reset_index()
            .sort_values(by="Unique_Ads", ascending=False)
        )

        # ----------------------------------------------------------
        # Create and assign colors
        # ----------------------------------------------------------

        # Define color palette blue with 10 steps
        blues_10 = [
            '#ffffff',
            '#fff7fb',
            '#deebf7',
            '#c6dbef',
            '#9ecae1',
            '#6baed6',
            '#4292c6',
            '#2171b5',
            '#08519c',
            '#08306b'
        ]
        # Assign colors
        num_bars = len(grouped)
        # Darkest blue for top value, lightest for lowest
        colors = [blues_10[-(i + 1)] for i in range(num_bars)]
        # If more bars than colors, repeat palette
        if num_bars > len(colors):
            colors = (colors * ((num_bars // len(colors)) + 1))[:num_bars]

        # ----------------------------------------------------------
        # Create figure
        # ----------------------------------------------------------
        if not grouped.empty:
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 5))

            # Axis labels and title
            ax.set_xlabel("Unique Ads")
            ax.set_title("Unique Ads per Technical Skill and Tool (Grouped by Count)")

            # Layout parameters
            label_shift_y = -0.45  # vertical shift for skill labels
            xshift_label = 1.5  # horizontal shift for skill labels
            xshift_value = 1  # numeric label shift
            right_margin = 5  # space between the longest number and right frame

            # Draw horizontal bars
            bars = ax.barh(range(len(grouped)), grouped["Unique_Ads"], color=colors, edgecolor='black', height=0.4)

            # Invert Y-axis (largest bar on top)
            ax.invert_yaxis()
            ax.set_yticks([])

            # Add skill names above bars
            for bar, skill_text in zip(bars, grouped["Skill"]):
                y_pos = bar.get_y() + bar.get_height() + label_shift_y
                x_pos = bar.get_x() + max(xshift_label, bar.get_width() * 0.02)
                ax.text(x_pos, y_pos, skill_text, ha='left', va='bottom', fontsize=9, fontweight='bold')

            # Add numeric values next to bars
            for bar in bars:
                width = bar.get_width()
                ax.text(width + xshift_value, bar.get_y() + bar.get_height() / 2,
                        f'{int(width)}', va='center', fontsize=9)

            # Adjust axis limits safely
            top_bar_y = bars[0].get_y()
            bottom_bar_y = bars[-1].get_y() + bars[-1].get_height()
            extra_space = label_shift_y + 1.3
            ax.set_ylim(bottom_bar_y + extra_space, top_bar_y - extra_space)

            max_width = grouped["Unique_Ads"].max()
            ax.set_xlim(0, max_width + right_margin)

        # Adjust layout
        plt.tight_layout()
    else:
        print(f"ERROR: No data to plot. Check 'Unique_Ads' values in {input_file_path}")
        return False


        # Clean layout
        plt.tight_layout()

        # ----------------------------------------------------------
        # Save plot
        # ----------------------------------------------------------
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