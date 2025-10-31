# CIP_HS2025_203 – Analysis of Required Skills in Data Science Job Advertisements

## Project Overview

This project was developed as part of the *Computational Intelligence in Practice (CIP)* course (HS2025).
Our goal is to analyze the skills demanded in **Data Science job postings in Switzerland**, using a full Python-based data pipeline — from web scraping to semantic text clustering and visualization.

The project explores trends in technical and soft skills required for data-oriented roles and their geographic distribution across Switzerland.

---

## Research Questions

1. Which **hard and soft skills** are most commonly required in current Data Science job advertisements in Switzerland?
2. In which **regions or cantons** are the most Data Science positions advertised?
3. Which **programming languages, tools, or technologies** appear most frequently across all job postings?

---

## Project Pipeline

The end-to-end data pipeline is implemented in `main_jobs.py` and follows six main stages:

1. **Scraping**
   Collect job advertisements from [jobs.ch](https://www.jobs.ch) using `requests`, `BeautifulSoup`, and `Selenium`.
   Dynamic elements such as cookie banners and filters are handled automatically.

2. **Merging**
   Session data are merged with a master dataset while avoiding duplicates.

3. **Cleaning**
   Unstructured job texts are cleaned, normalized, and filtered using `pandas`, `regex`, and basic NLP preprocessing.

4. **Analysis (Tasks)**
   Extract and quantify frequent terms related to job tasks.

5. **Analysis (Skills & Locations)**
   Identify common skills and geographic distribution of job offers.

6. **Semantic Clustering**
   Apply embeddings (`sentence-transformers`), dimensionality reduction (`UMAP`), and clustering (`scikit-learn`) to group similar skills.

---

## Project Structure


CIP_HS2025_203/
│
├── data/
│   ├── raw/               # Raw scraped data (per session & master file)
│   ├── processed/         # Cleaned and merged datasets
│   └── analysis/          # Clustered and analyzed datasets
│
├── report/
│   ├── figures/           # Plots, word clouds, heatmaps
│   └── CIP_HS2025_203_Report.pdf
│
├── src/
│   ├── scraping/          # Web scraping modules
│   ├── cleaning/          # Data cleaning & preprocessing
│   ├── analysis/          # Skill, task, and clustering analysis
│   ├── visualization/     # Plots & dashboards (in progress)
│   └── main_jobs.py       # Orchestrates the full data pipeline
│
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation (this file)
└── .gitignore


---

## Tools & Libraries

**Web Scraping:**
`requests`, `beautifulsoup4`, `selenium`, `mechanicalsoup`, `webdriver-manager`

**Data Analysis & Visualization:**
`pandas`, `matplotlib`

**Natural Language Processing:**
`nltk`, `sentence-transformers`

**Machine Learning & Clustering:**
`scikit-learn`, `umap-learn`, `geopandas`

---

## Example Outputs (Planned)

* Ranking of most frequent technical skills (bar chart)
* Word cloud of skill terms extracted from job ads
* Geographic heatmap of job locations
* 2D semantic skill cluster plot (UMAP visualization)

---

## Team & Contributions

**Group 203**

* **Stefan Dreyfus:** Web scraping, data merging, and cleaning
  *(scripts and outputs in `scraping/` and `cleaning/`)*
* **Valeska Blank:** Data analysis, clustering, and skill extraction
  *(scripts and outputs in `analysis/`)*
* **Julia Studer:** Visualization and presentation of results
  *(scripts and figures in `visualization/`, ongoing work)*

---

## How to Run

### Clone the repository

```bash
git clone https://github.com/<your-org>/CIP_HS2025_203.git
cd CIP_HS2025_203/src
```

### Install dependencies

pip install -r requirements.txt


### Run the main pipeline


python main_jobs.py

You will be prompted to enter:

* **Job title** (e.g. “Data Scientist”)
* **Maximum number of jobs** to scrape
* Whether to **delete session files** after merging

---

## Notes

* Data collection was performed respecting the [robots.txt](https://www.jobs.ch/robots.txt) of jobs.ch.
* The project is for **academic purposes only** and does not store or redistribute third-party content.
* The visualization component is currently under final development.

---

## Status

✔️ Data scraping and cleaning completed
✔️ Skill and clustering analyses completed
⏳ Visualization development in progress

---

**Authors:** Julia Studer, Valeska Blank,  Stefan Dreyfus
**Course:** Data Collection, Integration and Preprocessing HS2025

---
