from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from jobs_ch_base import get_driver, accept_cookies_and_close_banner
import time
import pandas as pd

#Getting the URL and accepting cookies and close banner
driver = get_driver()
driver.get("https://www.jobs.ch/de/")

accept_cookies_and_close_banner(driver)

#Search for Data Science in Search bar
wait = WebDriverWait(driver, 3)
search_bar = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[@id='synonym-typeahead-text-field']")))

search_bar.clear() #clear search par if needed
search_bar.send_keys("Data Science")
search_bar.send_keys(Keys.RETURN) #pressing Enter / Search for the job

time.sleep(5)

# 1. Target the specific <p> element class that serves as the heading for the skills section.
# We'll search for ALL <p> elements with this specific class combination, as one of them
# should be the skills heading. We'll then look for an <ul> immediately following it.
# This assumes the skills section is one of the *last* major sections in the ad structure.

# XPath to find a <p> element with the specific set of classes used for the heading:
HEADING_XPATH = (
    "//p[contains(@class, 'mb_s12') and contains(@class, 'lastOfType:mb_s0') and contains(@class, 'textStyle_p1')]"
)

# 2. Find all potential <ul> lists that immediately follow one of those <p> headings.
# The actual skills list (<ul>) also has a unique class combination that we can check for
# to ensure we grab the right list.

REQUIRED_SKILLS_CLASSES = "li-t_disc pl_s16 mb_s40 mt_s16"

try:
    # A more advanced XPath: Find a <p> with the heading classes, and then get the
    # <ul> following it that also has the unique skills list classes.
    # This combines both selectors for maximum accuracy.
    skills_list_xpath = (
        f"({HEADING_XPATH})/following-sibling::ul[contains(@class, 'li-t_disc')]"
    )

    # Locate the element (we'll rely on the structure and hope the skills list is the first or second such structure)
    # Since we can't guarantee *which* <p> is the skills heading without text, we'll try to find the *first*
    # <ul> that matches the structural requirement (following a matching <p> and having the required <ul> classes).

    # We will simply look for the first <ul> that contains the specific classes, as it is highly
    # likely to be the skill/task section. Then we can check the heading.

    # Let's revert to a slightly simpler, yet robust path: Find ALL <ul>s matching the class
    # and then confirm which one is preceded by the correct <p> heading.

    # The most reliable simple path: Find the <p> that *precedes* a list with the unique list classes.
    # The structure suggests the desired <ul> is the one you want. Let's stick to using the list classes:

    # Finding ALL <ul> elements with the unique list classes (tasks AND skills)
    all_content_lists = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH,
             f"//ul[contains(@class, 'li-t_disc') and contains(@class, 'pl_s16') and contains(@class, 'mb_s40') and contains(@class, 'mt_s16')]")
        )
    )

    # Now, iterate through the lists and try to determine which one is the skills section.
    # The skills list is usually the SECOND (index 1) or later list on the page, after "Tasks" (index 0).
    # Based on your data, let's assume the required skills are in the second matching <ul> (index 1)
    # OR, if we only have one, it's the first. This is a heuristic, but often works.

    # Heuristic: Take the last list matching the pattern. The 'Required Skills' is usually one of the final sections.
    if len(all_content_lists) >= 2:
        # Take the last one, which is most likely the skills section
        skills_list_ul = all_content_lists[-1]
    elif len(all_content_lists) == 1:
        # If there's only one list, it must be the one we need (either tasks or skills, but we'll extract it)
        skills_list_ul = all_content_lists[0]
    else:
        raise Exception("Found no content lists matching the class pattern.")

    # 3. Find all child <li> elements within the selected <ul>.
    skill_items = skills_list_ul.find_elements(By.TAG_NAME, "li")

    # 4. Extract the text from each <li>.
    required_skills = []
    for skill_item in skill_items:
        skill_text = skill_item.text.strip()
        if skill_text:
            required_skills.append(skill_text)

    # Output the results
    print("\n--- Extracted Required Skills (Heuristic: Last Matching List) ---")
    for skill in required_skills:
        print({skill})
    print("-----------------------------------------------------------------")

except Exception as e:
    print(f"An error occurred during skill extraction: {e}")
    print("Could not reliably find the expected skills list.")