# Define the keywords for exclusion. Keywords will be searched in 'Title', 'Tasks', and 'Skills' columns.
EXCLUSION_KEYWORDS = [
    # ACADEMIC / HIGHLY SPECIALIZED SCIENCE
    'PH\.D',
    'Doktor',
    'Dozent',
    'Chemie',
    'Biologie',
    'Laborant',
    'Food process',
    'Food engineering',
    # SOCIAL SCIENCES / HUMANITIES / LEGAL
    r'\bRecht\b',
    'Psychologie',
    'Sozialwissenschaften',
    'Geisteswissenschaften',
    # MEDICAL / HEALTHCARE / PHARMACEUTICAL
    r'\bMedizin\b',
    'Infirmières',
    'Infirmier',
    'Pflegeexpert',
    # TRADES / MANUAL / ENGINEERING / LOGISTICS
    'Montage',
    'Monteur',
    'Servicetechniker',
    'Technicien',
    'Mechanical',
    'Manufacturing',
    'Bauingenieur',
    'Lager',
    # BUSINESS SUPPORT / ADMIN / FINANCE
    'HR-Manager',
    'Treuhand',
    'Buchhaltung',

    # Add more keywords here as needed, e.g., 'Engineering', 'Biotech'
]

# Columns to check for the exclusion keywords
columns_to_check = ['Job_Title', 'Tasks', 'Skills']

# Build the case-insensitive regex pattern. Escape special characters in keywords (like '.' in 'PH.D') and join them with an OR operator '|'
regex_pattern = '|'.join([re.escape(k) for k in EXCLUSION_KEYWORDS])

# Flag for case-insensitivity:
regex_pattern_with_flags = f'(?i){regex_pattern}'

# Create a combined boolean exclusion mask
# Initializing the mask to all False
exclusion_mask_keywords = pd.Series([False] * len(df_cleaned), index=df_cleaned.index)

# Iterate over the columns and update the exclusion mask using the logical OR operator
for col in columns_to_check:
    # Calculate the mask for the current column
    col_mask = df_cleaned[col].astype(str).str.contains(
        regex_pattern_with_flags,
        na=False,
        regex=True
    )
    # The job is excluded if it matches the pattern in ANY of the columns
    exclusion_mask_keywords = exclusion_mask_keywords | col_mask

# Apply the filter. Keep only the rows where the mask is False
df_cleaned_final = df_cleaned[~exclusion_mask_keywords].copy()

# Validation output
rows_excluded_by_keyword = len(df_cleaned) - len(df_cleaned_final)

print("-" * 30)
print(f"Keywords used for exclusion: {', '.join(EXCLUSION_KEYWORDS)}")
print(f"Total rows before keyword filter: {len(df_cleaned)}")
print(f"Rows excluded by keyword filter: {rows_excluded_by_keyword}")
print(f"Total rows in cleaned data: {len(df_cleaned_final)}")
print("-" * 30)
