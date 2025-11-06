# Data Collection, Integration and Preprocessing HS2025 – Analysis of Required Skills in Data Science Job Advertisements

## Project Overview

This project was developed as part of the module  Data Collection, Integration and Preprocessing HS2025.
The goal is to analyze the skills demanded in Data Science job postings in Switzerland, using a full Python-based data pipeline — from web scraping to semantic text clustering and visualization.

The project explores trends in technical and soft skills required for data-oriented roles and their geographic distribution across Switzerland.

---

## Research Questions

1. What are the most frequently required skills, tools and tasks across current Data Science job advertisements in Switzerland? 
2. How can the thematic patterns in job descriptions be grouped into distinct clusters, and what do these clusters reveal about the main types of Data Science roles on the Swiss job market?
3. In which parts of Switzerland are the most Data Science positions currently advertised?

---

## Project Pipeline

The end-to-end data pipeline is implemented in `main_jobs.py` and follows six main stages:

1. **Scraping**
   Collect job advertisements from [jobs.ch](https://www.jobs.ch) using `requests`, `BeautifulSoup`, and `Selenium`.

2. **Merging**
   Session data are merged with a master dataset while avoiding duplicates.

3. **Cleaning**
   Unstructured job texts are cleaned and filtered using `pandas` and `regex`.

4. **Analysis (Tasks)**
   Extract and quantify frequent terms related to job tasks.

5. **Analysis (Skills & Locations)**
   Identify common skills and geographic distribution of job offers.

6. **Semantic Clustering**
   Apply embeddings (`sentence-transformers`), dimensionality reduction (`UMAP`), and clustering (`scikit-learn`) to group similar skills.

7. **Canton Map Visualization**
   Display the spatial distribution of Data Science job offers across Swiss cantons using geospatial plotting with `geopandas` and `matplotlib`.

8. **Single Skill Visualization**
   Present the most frequently mentioned technical skills as comparative horizontal bar charts.

9. **Tasks Overview Visualization**
   Visualize the most frequently mentioned soft skills using comparative horizontal bar charts.



---

## Project Structure

CIP_HS2025_203/
├── data/
│ ├── raw/            # Raw CSV data from jobs.ch
│ ├── processed/      # Cleaned data
│ └── visualization/  # Data for visualizations
├── report/
│   └── figures/        # Plots, figures
├── src/
│   ├── archive/        # Archive folder
│   ├── scraping/       # Web scraping modules
│   ├── cleaning/       # Data cleaning & preprocessing
│   ├── analysis/       # Skill, task, and clustering analysis
│   ├── visualization/  # Map and bar chart visualizations
│   └── main_jobs.py    # Orchestrates the full data pipeline
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore

---

## Tools & Libraries

**Web Scraping:**
`requests`, `beautifulsoup4`, `selenium`, `mechanicalsoup`, `webdriver-manager`

**Data Analysis & Visualization:**
`pandas`, `matplotlib`, `geopandas`

**Natural Language Processing:**
`nltk`, `sentence-transformers`

**Machine Learning & Clustering:**
`scikit-learn`, `umap-learn`

---

## How to Run

### Clone the repository


git clone https://github.com/Valeska197/CIP_HS2025_203.git

cd CIP_HS2025_203


### Install dependencies

pip install -r requirements.txt


### Run the main pipeline


python main_jobs.py

You will be prompted to enter:

* Job title (e.g. “Data Scientist”)
* Maximum number of jobs to scrape
* Whether to delete session files after merging

---

## Team & Contributions

**Group 203**

* **Stefan Dreyfus:** Web scraping, data merging, and cleaning
  *(scripts in scraping/ and cleaning/)*
* **Valeska Blank:** Data analysis, clustering, and skill extraction
  *(scripts in analysis/)*
* **Julia Studer:** Visualization and presentation of results
  *(scripts in visualization/)*

---


## How Generative AI Was Used

Generative AI tools, such as ChatGPT or Gemini, were employed in a supportive capacity during the project. 

These tools assisted in debugging code, clarifying programming questions, and suggesting approaches for scraping, data cleaning, analysis, and visualization.

AI was also used to refine text for the report, improving clarity and phrasing in English. 

All core tasks — including web scraping, data cleaning, analysis, clustering, and interpretation of results — were conducted and validated independently by the project team. 

While AI provided guidance, suggestions, and inspiration, methodological choices and final conclusions were determined without reliance on AI outputs. 

The use of AI contributed to workflow efficiency and facilitated problem-solving without substituting critical reasoning or domain expertise.

---
