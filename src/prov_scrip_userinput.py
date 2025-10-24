# --- USER INPUT AND DYNAMIC CONFIGURATION ---

# Ask for the job search term
job_search_term = input("Enter the job title you want to scrape (e.g., Data Scientist): ")

# Ask for the maximum number of jobs to scrape
while True:
    try:
        max_jobs_input = input("Enter the maximum number of jobs to scrape (e.g., 50): ")
        MAX_JOBS_TO_SCRAPE = int(max_jobs_input)
        if MAX_JOBS_TO_SCRAPE <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a whole number.")