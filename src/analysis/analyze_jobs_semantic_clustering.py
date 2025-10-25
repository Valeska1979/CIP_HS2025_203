# ==========================================================
# Semantic Clustering of Job Ads (multilingual)
# ==========================================================
# Goal:
#   Group similar job ads based on semantic content
#   (Tasks + Skills) using sentence embeddings.
#   Identify top keywords per cluster and assign labels.
# Author: Valeska Blank
# ==========================================================

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from umap import UMAP
import matplotlib.pyplot as plt
from pathlib import Path
import os
import sys

def run_semantic_clustering(input_file_path: Path, output_csv_path: Path, output_plot_path: Path):

    # ----------------------------------------------------------
    # Setup & Stopwords
    # ----------------------------------------------------------
    nltk.download("stopwords")

    # Combine English, German, and French stopwords
    multi_stopwords = set(
        stopwords.words("english")
        + stopwords.words("german")
        + stopwords.words("french")
    )

    # Add extra common filler words
    custom_stops = {
        "sowie", "kenntnisse", "erfahrung", "bereich",
        "team", "kunden", "arbeit", "anforderungen",
        "vorteil", "umfeld", "projekt", "mitarbeit",
        "etc", "data", "und", "oder", "gute"
    }
    multi_stopwords = multi_stopwords.union(custom_stops)

    # ----------------------------------------------------------
    # Load dataset
    # ----------------------------------------------------------
    try:
        df = pd.read_csv(input_file_path, sep=';')
    except FileNotFoundError:
        print(f"CLUSTERING FAILED: Input file not found at {input_file_path}")
        return False
    except Exception as e:
        print(f"CLUSTERING FAILED during load: {e}")
        return False

    # Combine relevant text fields
    df["text"] = df["Tasks"].fillna("") + " " + df["Skills"].fillna("")

    print(f"Dataset loaded: {len(df)} job ads")
    print("Example text:\n", df["text"].iloc[0][:250], "...\n")

    # ----------------------------------------------------------
    # Generate sentence embeddings (multilingual model)
    # ----------------------------------------------------------
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    model = SentenceTransformer(model_name)

    print(f"Encoding texts with model: {model_name}")
    embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

    # ----------------------------------------------------------
    # Cluster embeddings with KMeans
    # ----------------------------------------------------------
    n_clusters = 4  # you can adjust (try 3–6)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(embeddings)

    # ----------------------------------------------------------
    # Inspect cluster summaries
    # ----------------------------------------------------------
    print("\nCluster distribution:")
    print(df["Cluster"].value_counts().sort_index())

    # Show a few sample ads per cluster
    for c in range(n_clusters):
        print(f"\n--- Cluster {c} ---")
        sample = df[df["Cluster"] == c]["text"].head(2).tolist()
        for i, t in enumerate(sample, start=1):
            clean_text = t[:200].replace("\n", " ")
            print(f"[{i}] {clean_text}...")

    # ----------------------------------------------------------
    # Identify Top Keywords per Cluster (multilingual)
    # ----------------------------------------------------------
    cluster_texts = df.groupby("Cluster")["text"].apply(lambda x: " ".join(x)).to_dict()

    # Convert multilingual stopword set to list (required by sklearn)
    vectorizer = TfidfVectorizer(
        max_features=2000,
        stop_words=list(multi_stopwords),
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(cluster_texts.values())
    feature_names = vectorizer.get_feature_names_out()

    # Get top terms per cluster
    top_keywords = {}
    for i, cluster in enumerate(cluster_texts.keys()):
        row = tfidf_matrix[i].toarray().flatten()
        top_indices = row.argsort()[-8:][::-1]
        keywords = [feature_names[idx] for idx in top_indices]
        top_keywords[cluster] = keywords
        print(f"\nCluster {cluster} top keywords:")
        print(", ".join(keywords))

    # ----------------------------------------------------------
    # Create quick human-readable labels
    # ----------------------------------------------------------
    def suggest_label(keywords):
        text = " ".join(keywords).lower()
        if "machine" in text or "learning" in text or "ai" in text:
            return "Machine Learning / AI"
        elif "bi" in text or "dashboard" in text or "report" in text:
            return "Business Intelligence / Reporting"
        elif "pipeline" in text or "fabric" in text or "data platform" in text:
            return "Data Engineering / Architecture"
        elif "stakeholder" in text or "marketing" in text or "crm" in text:
            return "Business / Communication"
        else:
            return "General Data Science"

    cluster_labels = {cluster: suggest_label(words) for cluster, words in top_keywords.items()}

    # Assign labels back to the dataframe
    df["Cluster_Label"] = df["Cluster"].map(cluster_labels)

    print("\nAssigned cluster labels:")
    for c, label in cluster_labels.items():
        print(f"Cluster {c}: {label}")

    # ----------------------------------------------------------
    # Save results
    # ----------------------------------------------------------
    try:
        os.makedirs(output_csv_path.parent, exist_ok=True)
        df.to_csv(output_csv_path, index=False, sep=";")
        print(f"\nLabeled cluster file saved to: {output_csv_path}")
    except Exception as e:
        print(f"CLUSTERING FAILED during CSV save: {e}")
        return False

    # ----------------------------------------------------------
    # Visualize Semantic Clusters with UMAP
    # ----------------------------------------------------------

    # --- Reduce embeddings to 2D with UMAP ---
    umap_model = UMAP(
        n_neighbors=10,     # how many neighbors influence local structure
        min_dist=0.3,       # smaller = tighter clusters
        n_components=2,     # 2D output
        random_state=42
    )
    umap_results = umap_model.fit_transform(embeddings)

    # --- Create scatterplot ---
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        umap_results[:, 0],
        umap_results[:, 1],
        c=df["Cluster"],
        cmap="tab10",
        alpha=0.8,
        edgecolors="w",
        linewidths=0.4
    )

    plt.title("Semantic Clustering of Data Science Job Ads (UMAP Projection)", fontsize=12)
    plt.xlabel("UMAP Dimension 1")
    plt.ylabel("UMAP Dimension 2")

    # --- Legend with cluster labels ---
    handles, _ = scatter.legend_elements()
    labels = [cluster_labels[i] for i in sorted(cluster_labels.keys())]
    plt.legend(handles, labels, title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()

    return True


# ----------------------------------------------------------
# STANDALONE EXECUTION BLOCK
# ----------------------------------------------------------
if __name__ == "__main__":
    print("--- RUNNING SEMANTIC CLUSTERING SCRIPT IN STANDALONE TEST MODE ---")

    # Define paths relative to this script
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent.parent
    PROCESSED_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "processed"
    ANALYSIS_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "analysis"
    REPORT_DIR_TEST = PROJECT_ROOT_TEST / "report"

    # Define paths
    TEST_INPUT_PATH = PROCESSED_DATA_DIR_TEST / "jobs_ch_skills_all_cleaned_final_V1.csv"
    TEST_OUTPUT_CSV_PATH = ANALYSIS_DATA_DIR_TEST / "jobs_ch_semantic_clusters_labeled.csv"
    TEST_OUTPUT_PLOT_PATH = REPORT_DIR_TEST / "semantic_clusters_umap.png"

    # Run the analysis
    success = run_semantic_clustering(
        input_file_path=TEST_INPUT_PATH,
        output_csv_path=TEST_OUTPUT_CSV_PATH,
        output_plot_path=TEST_OUTPUT_PLOT_PATH
    )

    if success:
        print("\nStandalone clustering run complete.")
    else:
        print("\nStandalone clustering run failed.")
        sys.exit(1)