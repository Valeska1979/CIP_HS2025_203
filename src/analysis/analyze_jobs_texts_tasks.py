# ----------------------------------------------------------
# This script analyzes the 'Tasks' column from jobs.ch ads
# to identify key thematic areas describing
# what Data Scientists actually do.
# Author: Valeska Blank
# ==========================================================

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import os
from pathlib import Path
import sys


nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("stopwords")

def run_task_analysis(input_file_path, output_dir_path):


    # ----------------------------------------------------------
    # Load cleaned dataset
    # ----------------------------------------------------------
    try:
        df = pd.read_csv(input_file_path, sep=';')
    except FileNotFoundError:
        print(f"TASK ANALYSIS FAILED: Input file not found at {input_file_path}")
        return False
    except Exception as e:
        print(f"TASK ANALYSIS FAILED during load: {e}")
        return False

    # ----------------------------------------------------------
    # Use the 'Tasks' column for this analysis
    # ----------------------------------------------------------
    df["text"] = df["Tasks"].fillna("")
    print("\nSample text from 'Tasks' column:\n", df["text"].head(2))

    # ----------------------------------------------------------
    # Thematic Keyword Groups (multilingual)
    # ----------------------------------------------------------
    task_topics = {
        "Data Preparation": [
            "clean", "preprocess", "transform", "wrangle", "prepare",
            "collect", "extract", "load", "ingest",
            "bereinigen", "vorbereiten", "aufbereiten", "transformieren",
            "sammeln", "extrahieren", "laden",
            "nettoyer", "préparer", "transformer", "collecter", "extraire", "charger"
        ],
        "Modeling": [
            "model", "train", "predict", "forecast", "regression",
            "classification", "cluster", "segmentation",
            "modellieren", "trainieren", "vorhersagen", "prognostizieren",
            "klassifizieren", "clustern", "segmentieren",
            "modéliser", "entraîner", "prédire", "prévoir", "classer", "segmenter"
        ],
        "Visualization": [
            "visualize", "dashboard", "report", "plot", "chart",
            "present", "powerbi", "power bi", "tableau",
            "visualisieren", "bericht", "darstellen", "präsentieren",
            "visualiser", "tableau", "rapport", "présenter"
        ],
        "Deployment / MLOps": [
            "deploy", "pipeline", "production", "api", "monitor",
            "ci", "cd", "automate", "container",
            "bereitstellen", "überwachen", "automatisieren", "produktion",
            "déployer", "surveiller", "automatiser", "production"
        ],
        "Collaboration": [
            "stakeholder", "business", "communicate", "presentation",
            "team", "collaborate", "support", "coordinate",
            "teamarbeit", "zusammenarbeit", "kommunizieren",
            "präsentation", "unterstützen", "koordinieren",
            "collaborer", "équipe", "communiquer", "soutenir", "coordonner"
        ],
        "Exploratory Analysis": [
            "analyze", "analyse", "explore", "insight", "understand",
            "interpret", "investigate",
            "analysieren", "untersuchen", "verstehen", "interpretieren",
            "erforschen", "einsicht",
            "analyser", "explorer", "comprendre", "interpréter", "étudier"
        ],
        "Data Engineering": [
            "pipeline", "etl", "dataflow", "warehouse", "integration",
            "database", "build",
            "datenpipeline", "etl", "datenfluss", "datenbank",
            "aufbauen", "integrieren", "datenlager",
            "pipeline", "entrepôt", "intégration", "base", "construire"
        ],
        "Statistics": [
            "statistical", "inference", "hypothesis", "test",
            "experiment", "metrics", "evaluate",
            "statistisch", "hypothese", "testen", "auswerten", "messen",
            "bewerten", "versuch",
            "statistique", "hypothèse", "tester", "évaluer", "mesurer", "expérience"
        ],
    }

    # ----------------------------------------------------------
    # Count mentions per thematic group (overview level)
    # ----------------------------------------------------------
    topic_stats = []

    for topic, keywords in task_topics.items():
        # Build regex that matches all keywords as whole words (\b = word boundary)
        # For multi-word phrases (e.g. "power bi"), replace spaces with \s+
        pattern = r"|".join([
            r"\b" + re.escape(k.lower()).replace("\\ ", r"\s+") + r"\b"
            for k in keywords
        ])

        # Count total mentions and number of unique ads containing any keyword
        total_mentions = df["text"].str.lower().str.count(pattern, flags=re.IGNORECASE).sum()
        unique_ads = df["text"].str.lower().str.contains(pattern, flags=re.IGNORECASE).sum()

        topic_stats.append((topic, int(total_mentions), int(unique_ads)))

    # Convert to DataFrame and sort by number of ads
    df_topics = pd.DataFrame(topic_stats, columns=["Topic", "Total_Mentions", "Unique_Ads"])
    df_topics = df_topics.sort_values("Unique_Ads", ascending=False)

    # ----------------------------------------------------------
    # Print summary for thematic analysis
    # ----------------------------------------------------------
    print("\nThematic Task Analysis (multilingual keyword groups)\n")
    print(df_topics.to_string(index=False))

    # ----------------------------------------------------------
    # Detailed breakdown: keyword-level statistics per topic
    # ----------------------------------------------------------
    keyword_details = []

    for topic, keywords in task_topics.items():
        for k in keywords:
            pattern = r"\b" + re.escape(k.lower()).replace("\\ ", r"\s+") + r"\b"

            total_mentions = df["text"].str.lower().str.count(pattern, flags=re.IGNORECASE).sum()
            unique_ads = df["text"].str.lower().str.contains(pattern, flags=re.IGNORECASE).sum()

            if total_mentions > 0:
                keyword_details.append((topic, k, int(total_mentions), int(unique_ads)))

    # Convert to DataFrame and sort
    df_keywords = pd.DataFrame(keyword_details, columns=["Topic", "Keyword", "Total_Mentions", "Unique_Ads"])
    df_keywords = df_keywords.sort_values(["Topic", "Total_Mentions"], ascending=[True, False])

    # ----------------------------------------------------------
    # Export results
    # ----------------------------------------------------------
    os.makedirs(output_dir_path, exist_ok=True)

    # Saving to output_dir_path
    tasks_overview_out = output_dir_path / "jobs_ch_tasks_overview.csv"
    tasks_keywords_out = output_dir_path / "jobs_ch_tasks_with_keywords.csv"

    try:
        df_topics.to_csv(tasks_overview_out, index=False, sep=";")
        print(f"\nOverview CSV successfully saved: {tasks_overview_out}")

        df_keywords.to_csv(tasks_keywords_out, index=False, sep=";")
        print(f"Detailed keyword-level CSV successfully saved: {tasks_keywords_out}")
    except Exception as e:
        print(f"TASK ANALYSIS FAILED during CSV export: {e}")
        return False

    # Show preview
    print("\nPreview of keyword-level summary\n")
    print(df_keywords.head(20).to_string(index=False))

    return True


# ----------------------------------------------------------
# STANDALONE EXECUTION BLOCK
# ----------------------------------------------------------
if __name__ == "__main__":
    print("--- RUNNING TASKS ANALYSIS SCRIPT IN STANDALONE TEST MODE ---")

    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent

    # Input is the final cleaned data
    PROCESSED_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "processed"
    TEST_INPUT_PATH = PROCESSED_DATA_DIR_TEST / "jobs_ch_skills_all_cleaned_final_V1.csv"

    # Output goes to the analysis directory
    ANALYSIS_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "analysis"

    # Run the analysis, saving to the ANALYSIS directory
    success = run_task_analysis(
        input_file_path=TEST_INPUT_PATH,
        output_dir_path=ANALYSIS_DATA_DIR_TEST
    )

    if success:
        print("\nStandalone task analysis run complete.")
    else:
        print("\nStandalone task analysis run failed.")
        sys.exit(1)