# ----------------------------------------------------------
# This script analyzes the 'Tasks' column from jobs.ch ads
# to identify key thematic areas
# describing what Data Scientists actually do.
# ==========================================================

import pandas as pd
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("stopwords")

# ----------------------------------------------------------
# Load cleaned dataset
# ----------------------------------------------------------
file_path = "data/processed/jobs_ch_skills_all_cleaned_final_V1.csv"
df = pd.read_csv(file_path)

print(f"Dataset loaded with {len(df)} rows")
print(df.columns.tolist())  # See column names

# ----------------------------------------------------------
# Use the 'Tasks' column for this analysis
# ----------------------------------------------------------
df["text"] = df["Tasks"].fillna("")
print("\nSample text from 'Tasks' column:\n", df["text"].head(2))

# ==========================================================
# Thematic Keyword Groups (multilingual)
# ==========================================================
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
        "present", "powerbi", "tableau",
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
# Count mentions per thematic group
# ----------------------------------------------------------
topic_stats = []

for topic, keywords in task_topics.items():
    pattern = r"|".join([r"\b" + re.escape(k.lower()) + r"\b" for k in keywords])
    total_mentions = df["text"].str.lower().str.count(pattern, flags=re.IGNORECASE).sum()
    unique_ads = df["text"].str.lower().str.contains(pattern, flags=re.IGNORECASE).sum()
    topic_stats.append((topic, int(total_mentions), int(unique_ads)))

df_topics = pd.DataFrame(topic_stats, columns=["Topic", "Total_Mentions", "Unique_Ads"])
df_topics = df_topics.sort_values("Unique_Ads", ascending=False)

# ----------------------------------------------------------
# Print summary for thematic analysis
# ----------------------------------------------------------
print("\nThematic Task Analysis (multilingual keyword groups):\n")
print(df_topics.to_string(index=False))

# ----------------------------------------------------------
# Export thematic results to CSV
# ----------------------------------------------------------
output_dir = "data/processed/"
tasks_out = output_dir + "jobs_ch_tasks.csv"
df_topics.to_csv(tasks_out, index=False, sep=";")
print(f"\nCSV file successfully saved: {tasks_out}")

