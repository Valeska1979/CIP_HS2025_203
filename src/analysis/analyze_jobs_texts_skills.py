# ----------------------------------------------------------
# This script analyzes 168 cleaned job ads from jobs.ch to
# identify the most frequent Data Science skills and concepts
# (Python, SQL, Machine Learning, BI, Cloud, etc.) across
# multiple languages (DE/EN/FR).
# Author: Valeska Blank
# ==========================================================

import pandas as pd
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import re
from collections import Counter
import os
from pathlib import Path

def run_skills_analysis(input_file_path: Path, output_dir_path: Path):

    # Load cleaned dataset
    try:
        df = pd.read_csv(input_file_path, sep=';')
    except FileNotFoundError:
        print(f"SKILLS ANALYSIS FAILED: Input file not found at {input_file_path}")
        return False
    except Exception as e:
        print(f"SKILLS ANALYSIS FAILED during load: {e}")
        return False

    print(f"Dataset loaded with {len(df)} rows")
    print(df.columns.tolist())

    # Combine text columns into one
    df["text"] = df["Tasks"].fillna("") + " " + df["Skills"].fillna("")
    print("\nSample combined text:\n", df["text"].head(2))

    # Prepare multilingual stopwords
    stops = set(
        stopwords.words("english")
        + stopwords.words("german")
        + stopwords.words("french")
    )

    # Clean and tokenize
    def clean_text_multilang(text):
        text = text.lower()
        # Keep accented letters to handle German/French words correctly
        words = re.findall(r"[a-zäöüéèàâçß]+", text)
        tokens = [w for w in words if w not in stops and len(w) > 2]
        return tokens

    df["tokens"] = df["text"].apply(clean_text_multilang)

    # Count raw word frequencies
    all_tokens = [t for tokens in df["tokens"] for t in tokens]
    freq = Counter(all_tokens)

    print("\nTop 20 most common words (all languages):\n")
    for word, count in freq.most_common(20):
        print(f"{word:20} {count}")

    # -----------------------------------------------------------
    # Above result was too general (many non-technical words).
    # Next: use enhanced multilingual phrase detection
    #
    # Goal:
    #   - Detect specific multi-word Data Science concepts
    #     (e.g., "machine learning", "data science", "business intelligence")
    #   - Include their translations and abbreviations in German (DE)
    #     and French (FR), since many job ads are multilingual.
    #   - Group synonyms and short forms (e.g., "ml" = "machine learning")
    #
    # Approach:
    #   - Define a dictionary 'phrase_groups' where:
    #       -keys are canonical English skill names (e.g. "machine learning")
    #       -values are lists of multilingual or synonymous variants
    # -----------------------------------------------------------

    phrase_groups = {
        "data science": ["data science", "science des données", "datenwissenschaft"],
        "machine learning": ["machine learning", "maschinelles lernen", "apprentissage automatique", "ml"],
        "deep learning": ["deep learning", "apprentissage profond"],
        "artificial intelligence": ["artificial intelligence", "intelligence artificielle", "ai"],
        "big data": ["big data", "grosse données"],
        "data analysis": ["data analysis", "data analytics", "analyse de données", "datenanalyse"],
        "business intelligence": ["business intelligence", "bi"],
        "data engineering": ["data engineering", "ingénierie des données", "datenengineering"],
        "data pipeline": ["data pipeline", "pipeline de données"],
        "data warehouse": ["data warehouse", "entrepôt de données", "datenlager"],
        "data lake": ["data lake", "lac de données"],
        "data visualization": ["data visualization", "visualisation de données", "datenvisualisierung"],
        "data governance": ["data governance", "gouvernance des données"],
        "power bi": ["power bi"],
        "tableau": ["tableau dashboard", "tableau", "tableaux de bord"],
        "cloud computing": ["cloud computing", "cloud", "azure cloud", "aws cloud", "google cloud"],
        "predictive modeling": ["predictive modeling", "modélisation prédictive", "vorhersagemodellierung"],
        "statistical modeling": ["statistical modeling", "modélisation statistique", "statistische modellierung"],
        "computer vision": ["computer vision", "vision par ordinateur"],
        "natural language processing": ["natural language processing", "traitement du langage naturel", "nlp"],
    }

    phrase_stats = []

    for canonical, variants in phrase_groups.items():
        # Build regex pattern combining all multilingual variants
        pattern = r"|".join([re.escape(v) for v in variants])

        # Count total mentions across all job texts
        total_mentions = df["text"].str.lower().str.count(pattern).sum()

        # Count unique job ads where phrase appears at least once
        unique_ads = df["text"].str.lower().str.contains(pattern).sum()

        # Store both values
        phrase_stats.append((canonical, int(total_mentions), int(unique_ads)))

    # Convert to DataFrame
    df_phrases = pd.DataFrame(phrase_stats, columns=["Phrase", "Total_Mentions", "Unique_Ads"])
    df_phrases = df_phrases.sort_values(by="Total_Mentions", ascending=False)

    print("\nData-Science Phrase Frequencies (multilingual):\n")
    print(df_phrases.to_string(index=False))

    # -----------------------------------------------------------
    # Next: Single-skill detection (programming languages & tools)
    #
    # Goal:
    #   - Identify individual technical skills and tools mentioned in job ads
    #     (e.g., "python", "sql", "excel", "r").
    #   - Count both:
    #       -total mentions across all ads
    #       -number of unique job ads mentioning each skill
    # -----------------------------------------------------------

    single_skills = [
        # Programming languages
        "python", "r", "sql", "scala", "java", "c++", "bash", "shell",

        # Data & analytics tools
        "excel", "tableau", "power bi", "powerbi", "qlik", "sas",

        # Python / data libraries
        "pandas", "numpy", "matplotlib", "seaborn", "plotly",
        "tensorflow", "pytorch", "keras", "scikit-learn",

        # Cloud & DevOps
        "aws", "azure", "gcp", "google cloud", "cloud",
        "docker", "kubernetes", "git", "github", "linux",

        # Big data & databases
        "spark", "hadoop", "mongodb", "sql server", "postgresql", "mysql", "oracle"
    ]

    skill_stats = []

    for skill in single_skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        # Total mentions
        total_mentions = df["text"].str.lower().str.count(pattern).sum()

        # Unique ads (how many job ads mention this skill at least once)
        unique_ads = df["text"].str.lower().str.contains(pattern).sum()

        skill_stats.append((skill, int(total_mentions), int(unique_ads)))

    # Convert to DataFrame and sort by total mentions
    df_skills = pd.DataFrame(skill_stats, columns=["Skill", "Total_Mentions", "Unique_Ads"])
    df_skills = df_skills.sort_values(by="Total_Mentions", ascending=False)

    print("\nProgramming / Tool Mentions:\n")
    print(df_skills.to_string(index=False))

    # -------------------------------------------------
    # Geographic distribution of Data Science job ads
    # -------------------------------------------------

    # Count number of job ads per location
    geo_counts = (
        df["Job_Location"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )
    geo_counts.columns = ["Location", "Job_Count"]

    print("\nTop 15 Locations for Data Science Jobs:\n")
    print(geo_counts.head(30).to_string(index=False))

    # -----------------------------------------------------------
    # Export results to CSV files
    # -----------------------------------------------------------

    # Define output directory and filenames
    os.makedirs(output_dir_path, exist_ok=True)

    phrases_out = output_dir_path / "jobs_ch_phrases_analysis.csv"
    skills_out = output_dir_path / "jobs_ch_single_skills_analysis.csv"
    locations_out = output_dir_path / "jobs_ch_location_counts.csv"

    # Save DataFrames to CSV (without index)
    try:
        df_phrases.to_csv(phrases_out, index=False, sep=";")
        df_skills.to_csv(skills_out, index=False, sep=";")
        geo_counts.to_csv(locations_out, index=False, sep=";")
    except Exception as e:
        print(f"SKILLS ANALYSIS FAILED during CSV export: {e}")
        return False

    print("\nCSV files successfully saved to ANALYSIS folder:")
    print(f"- Phrases:   {phrases_out}")
    print(f"- Skills:    {skills_out}")
    print(f"- Locations: {locations_out}")


    return True

# ----------------------------------------------------------
# STANDALONE EXECUTION BLOCK
# ----------------------------------------------------------
if __name__ == "__main__":
    print("--- RUNNING SKILLS ANALYSIS SCRIPT IN STANDALONE TEST MODE ---")

    # Define paths relative to this script
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent.parent

    ANALYSIS_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "analysis"

    # Define paths
    TEST_INPUT_PATH = ANALYSIS_DATA_DIR_TEST / "jobs_ch_semantic_clusters_labeled.csv"

    # Run the analysis, saving to the REPORT directory
    success = run_skills_analysis(
        input_file_path=TEST_INPUT_PATH,
        output_dir_path=ANALYSIS_DATA_DIR_TEST
    )

    if success:
        print("\nStandalone skills analysis run complete.")
    else:
        print("\nStandalone skills analysis run failed.")
        sys.exit(1)