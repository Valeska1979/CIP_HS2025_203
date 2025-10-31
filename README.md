<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIP Jobs Project README</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f9fc;
            color: #1f2937;
            padding: 2rem;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        }
        h1, h2, h3 {
            color: #10b981; /* Emerald 500 */
        }
        h1 {
            border-bottom: 3px solid #10b981;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        h2 {
            font-size: 1.75rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        h3 {
            font-size: 1.25rem;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: #374151;
        }
        .section-box {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            background-color: #f9fafb;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        th, td {
            border: 1px solid #e5e7eb;
            padding: 0.75rem;
            text-align: left;
        }
        th {
            background-color: #e0f2f1; /* Teal 50 */
            font-weight: 600;
        }
        code:not(pre code) {
            background-color: #f3f4f6;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: #b91c1c; /* Red 700 */
        }
        pre {
            background-color: #1f2937;
            color: #ffffff;
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
        }
        .list-unstyled {
            list-style: none;
            padding-left: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-3xl font-bold">CIP Jobs Project: Analysis of Required Skills in Data Science Job Advertisements</h1>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">🎯 Project Overview</h2>
            <p class="mb-4 text-gray-700">
                This project implements a complete data science workflow, focusing on extracting, processing, and analyzing job advertisement data for Data Science positions in **Switzerland**. The core goal is to generate insights into the current job market demand.
            </p>
            <p class="font-bold mb-2">The pipeline covers:</p>
            <ol class="list-unstyled space-y-2 pl-6 text-gray-700">
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">1.</span>
                    <span><strong>Data Acquisition:</strong> Web scraping job postings from <code>jobs.ch</code> using dynamic and static parsing techniques.</span>
                </li>
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">2.</span>
                    <span><strong>Data Transformation:</strong> Cleaning, standardizing, and categorizing unstructured, multilingual text data (skills, job titles).</span>
                </li>
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">3.</span>
                    <span><strong>Analysis & Visualization:</strong> Answering key research questions and visualizing findings using Python.</span>
                </li>
            </ol>

            <h3 class="font-semibold mt-6">Research Questions</h3>
            <p class="text-gray-700">The analysis is driven by the following questions:</p>
            <ul class="list-disc ml-6 space-y-2 text-gray-700">
                <li>Which **hard and soft skills** are most commonly required in current Data Science job advertisements in Switzerland?</li>
                <li>In which parts of Switzerland (geographic distribution) are the most Data Science positions currently advertised?</li>
                <li>Which programming languages, tools, or technologies are most frequently mentioned across all job postings?</li>
            </ul>
        </div>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">🚀 Getting Started</h2>

            <h3 class="font-semibold">1. Prerequisites</h3>
            <p class="text-gray-700">You need a working Python environment (preferably Python Python 3.11). The project uses a virtual environment (<code>.venv</code>), so ensure you have <code>pip</code> and <code>venv</code> installed.</p>

            <h3 class="font-semibold">2. Environment Setup</h3>
            <p class="text-gray-700">Clone the repository and install all required dependencies:</p>
            <pre><code class="language-bash"># Clone the repository
git clone [https://github.com/Valeska197/CIP_HS2025_203.git](https://github.com/Valeska197/CIP_HS2025_203.git)

cd CIP_HS2025_203

# Create and activate the virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies, including all necessary scraping and analysis libraries
pip install -r requirements.txt
</code></pre>

            <h3 class="font-semibold">3. Execution</h3>
            <p class="text-gray-700">The primary execution scripts are located in the <code>src/</code> directory and run the pipeline sequentially.</p>
            <p class="text-gray-700">To run the full pipeline (scraping, cleaning, analysis, and visualization), execute the main entry point script:</p>
            <pre><code class="language-bash"># Ensure your virtual environment is active
python src/main_jobs.py
</code></pre>
        </div>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">💾 Data Schema and Flow</h2>
            <p class="text-gray-700">The data pipeline processes the job data through three distinct stages, starting with the raw scrape and ending with the finalized dataset ready for analysis.</p>

            <h3 class="font-semibold">Schema (All Stages)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Column Name</th>
                        <th>Data Type</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>Job_Index</code></td>
                        <td><code>int</code></td>
                        <td>Unique, sequential ID for each job, continuous across all scraping sessions.</td>
                    </tr>
                    <tr>
                        <td><code>Job_Title</code></td>
                        <td><code>string</code></td>
                        <td>The title of the job advertisement (e.g., 'Data Scientist', 'ML Engineer').</td>
                    </tr>
                    <tr>
                        <td><code>Company_Name</code></td>
                        <td><code>string</code></td>
                        <td>The company offering the position.</td>
                    </tr>
                    <tr>
                        <td><code>Job_Location</code></td>
                        <td><code>string</code></td>
                        <td>The physical location of the job in Switzerland.</td>
                    </tr>
                    <tr>
                        <td><code>Tasks</code></td>
                        <td><code>string</code></td>
                        <td>A pipe-separated (<code>|</code>) string containing the key tasks and responsibilities listed in the job post.</td>
                    </tr>
                    <tr>
                        <td><code>Skills</code></td>
                        <td><code>string</code></td>
                        <td>A pipe-separated (<code>|</code>) string containing the required skills listed in the job post.</td>
                    </tr>
                    <tr>
                        <td><code>Job_Search_Term</code></td>
                        <td><code>string</code></td>
                        <td>The keyword used to find the job (e.g., 'Data Science').</td>
                    </tr>
                </tbody>
            </table>

            <h3 class="font-semibold">Data Flow Overview</h3>
            <p class="text-gray-700">The data transformation process is critical for ensuring only relevant, high-quality Data Science job postings are analyzed.</p>
            <ol class="list-unstyled space-y-2 pl-6 text-gray-700">
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">1.</span>
                    <span>**Raw Data (<code>jobs_ch_skills_all.csv</code>):** Collected data is merged into the master file.</span>
                </li>
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">2.</span>
                    <span>**Intermediate Cleansing (Script: <code>data_cleaning.py</code>):** Filters are applied to ensure data completeness and remove specific non-relevant job ads.</span>
                </li>
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">3.</span>
                    <span>**Final Cleansing (Script: <code>data_cleaning.py</code>):** A final regular expression-based filter is applied across job text fields to exclude roles clearly outside the Data Science scope (e.g., 'Chemie', 'Lager', 'Recht').</span>
                </li>
                <li class="flex items-start">
                    <span class="mr-2 text-green-500">4.</span>
                    <span>**Final Dataset (<code>jobs_ch_skills_all_cleaned_final_V1.csv</code>):** The final dataset ready for all subsequent analysis and visualization steps.</span>
                </li>
            </ol>
        </div>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">🛠️ Key Technologies & Libraries</h2>
            <p class="text-gray-700">This project applies various Python libraries to manage the data science workflow:</p>
            <table>
                <thead>
                    <tr>
                        <th>Stage</th>
                        <th>Key Libraries</th>
                        <th>Purpose</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Data Acquisition</strong></td>
                        <td><code>Selenium</code>, <code>BeautifulSoup</code>, <code>requests</code></td>
                        <td>Handling dynamic website elements, parsing HTML, and fetching static content from <code>jobs.ch</code>.</td>
                    </tr>
                    <tr>
                        <td><strong>Data Transformation</strong></td>
                        <td><code>pandas</code>, <code>nltk</code>, <code>spaCy</code>, <code>re</code>, <code>googletrans</code></td>
                        <td>Data cleaning, multilingual text processing (language detection/translation), and **regular expressions (<code>re</code>) for filtering**.</td>
                    </tr>
                    <tr>
                        <td><strong>Analysis & Viz</strong></td>
                        <td><code>geopandas</code>, <code>scikit-learn</code>, <code>umap-learn</code>, <code>sentence-transformers</code>, <code>matplotlib</code>, <code>seaborn</code>, <code>Plotly</code>, <code>wordcloud</code></td>
                        <td>Statistical analysis, advanced skill extraction/embedding, dimensionality reduction/clustering (e.g., for job categories), and **geospatial data processing and mapping**.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">📂 Repository Structure</h2>
            <p class="text-gray-700">The project follows a clean structure to separate source code, data artifacts, and reporting documents.</p>
            <table>
                <thead>
                    <tr>
                        <th>Folder/File</th>
                        <th>Purpose</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong><code>src/</code></strong></td>
                        <td>**All primary source code (<code>.py</code> files) for the data pipeline is located here.**</td>
                    </tr>
                    <tr>
                        <td><strong><code>data/</code></strong></td>
                        <td>Stores raw scraped data, intermediate files, and final cleaned datasets (e.g., CSV outputs).</td>
                    </tr>
                    <tr>
                        <td><strong><code>report/</code></strong></td>
                        <td>Contains final reports, figures and visualization images.</td>
                    </tr>
                    <tr>
                        <td><strong><code>.venv/</code></strong></td>
                        <td>Python virtual environment.</td>
                    </tr>
                    <tr>
                        <td><strong><code>.gitignore</code></strong></td>
                        <td>Specifies files and folders (like <code>.venv/</code> and <code>.idea/</code>) that Git should ignore.</td>
                    </tr>
                    <tr>
                        <td><strong><code>requirements.txt</code></strong></td>
                        <td>Lists all Python package dependencies (run <code>pip install -r requirements.txt</code>).</td>
                    </tr>
                    <tr>
                        <td><strong><code>repo_structure.txt</code></strong></td>
                        <td>Text file documenting the initial directory structure.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">👩‍💻 Team Contributions (Code Ownership)</h2>
            <p class="text-gray-700">This section outlines the specific, mandatory contribution areas and responsibilities of each team member.</p>
            <table>
                <thead>
                    <tr>
                        <th>Team Member</th>
                        <th>Area of Responsibility</th>
                        <th>Code/Artifact Contribution Focus</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Stefan Dreyfus</strong></td>
                        <td>**Data Acquisition & Cleansing**</td>
                        <td>Responsible for all code in the **scraping and cleaning stages**. Focuses on implementing **Selenium**, **BeautifulSoup**, data merging logic, data quality scripts, multilingual text handling, and all final regular expression-based data filtering.</td>
                    </tr>
                    <tr>
                        <td><strong>Valeska Blank</strong></td>
                        <td>**Core Analysis & Feature Engineering**</td>
                        <td>Responsible for all **analytical scripts** to answer **RQ1 (Hard/Soft Skills) and RQ3 (Programming Languages)**. Focuses on applying **NLTK/spaCy** and **sentence-transformers** for reliable skill extraction, grouping skills, and implementing core ML/clustering logic using **scikit-learn** and **umap-learn**.</td>
                    </tr>
                    <tr>
                        <td><strong>Julia Studer</strong></td>
                        <td>**Visualization & Geographic Analysis**</td>
                        <td>Responsible for all **visualization and reporting scripts**. Develops the geographic analysis for **RQ2** using **geopandas**. Focuses on creating all final output visualizations: **ranking plots**, **word clouds**, maps, and ensuring high-quality figures using **Plotly/matplotlib**.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section-box">
            <h2 class="text-2xl font-semibold mb-3">🤝 Contact</h2>
            <p class="text-gray-700">For any questions regarding the project setup or specific components, please reach out to the respective contributor listed above.</p>
        </div>
    </div>
</body>
</html>
