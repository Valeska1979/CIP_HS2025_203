# CIP_HS2025_203

## Project Overview
This is the repository for our group project in the course *Collect, Integrate & Prepare (CIP)* at HSLU.  
Goal: We scrape data from a website and then perform an analysis using Python.

## Team
- Member 1: Julia Studer
- Member 2: Stefan Dreyfus
- Member 3: Valeska Blank

## Setup

### Requirements
- **Python 3.11**  
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Valeska197/CIP_HS2025_203.git
   cd CIP_HS2025_203


2. Create a virtual environment:

- macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

- Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

### Project Structure

CIP_HS2025_203/
│   README.md
│   .gitignore
│   requirements.txt
│
├── data/
│   ├── raw/           # Raw data from scraping
│   └── processed/     # Cleaned / transformed data
│
└── src/
    ├── scraping/      # Scraping scripts
    └── analysis/      # Data analysis & visualization

### Workflow

1. Always create a new branch for code changes.

2. Use Pull Requests to merge into main.

3. Keep dependencies up to date by refreshing requirements.txt:
pip freeze > requirements.txt

4. Run all scripts from the project root to ensure relative paths work correctly.

