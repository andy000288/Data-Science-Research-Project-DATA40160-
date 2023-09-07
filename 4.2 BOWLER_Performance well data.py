import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Set up the Selenium driver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Dictionary of websites with their corresponding labels
websites = {
    "Durham Cricket": "https://durhamcb.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=255910&view_by=year&view_by=year&team_id=255910&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
}

# List to store URLs
all_page_urls = []

for label, website in websites.items():
    driver.get(website)
    wait = WebDriverWait(driver, 10)
    page_urls = []

    has_scorecards = False

    while True:
        scorecard_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                                          "//a[contains(@class, 'link-scorecard') and contains(@class, 'd-none d-md-inline-block rounded-circle')]")))

        if scorecard_icons:
            has_scorecards = True  
            for icon in scorecard_icons:
                try:
                    link_url = icon.get_attribute("href")
                    page_urls.append(link_url)
                except TimeoutException:
                    print(
                        "Timeout Exception: The SCORECARD tab might not be present or clickable within the given time frame.")

            try:
                next_button = driver.find_element(By.LINK_TEXT, "Next")
                next_button.click()
                wait.until(EC.staleness_of(scorecard_icons[0]))
                time.sleep(2)
            except NoSuchElementException:
                print("No more NEXT button. All match links extracted.")
                break
        else:
            break

    if not has_scorecards:
        print(f"{label} 没有符合要求的比赛。")

    # Store URLs along with label
    all_page_urls.append((label, page_urls))

# List to store generated filenames
generated_files = []

# Output the page URLs with labels to separate files
for label, urls in all_page_urls:
    filename = 'BATTER_' + label + '_Links.txt'
    generated_files.append(filename)  # Add the filename to the list

    with open(filename, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")

time.sleep(30)
driver.quit()

# Print the list of generated files
print(generated_files)


from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

# List to store all extracted bowler data
all_bowler_data_list = []

# Assuming 'BATTER_Durham Cricket_Links.txt' contains the URLs
with open('BATTER_Durham Cricket_Links.txt', 'r') as f:
    urls = [line.strip() for line in f]

# Loop through each URL to scrape data
for url in urls:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract club names and tab IDs
    club_tags = soup.select('ul.nav.nav-tabs.nav-justified.subnav-2 li a')

    # Loop through each club name and extract bowler data
    for club_tag in club_tags:
        club_name = club_tag.get_text(strip=True)
        section_id = club_tag['href'].replace('#', '')
        section_content = soup.find(id=section_id)

        if section_content:
            bowler_table = section_content.find('table', class_='bowler-detail')
            if bowler_table:
                tbody = bowler_table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) > 7:  # Assuming at least 8 cells for valid data
                            bowler_link = cells[0].find('a', href=True)
                            bowler_id = bowler_link['href'].split('/')[-1].split('?')[0] if bowler_link else 'N/A'
                            data = {
                                "ID": bowler_id,
                                "BOWLER": cells[0].get_text(strip=True),
                                "OVERS": cells[1].get_text(strip=True),
                                "MAIDENS": cells[2].get_text(strip=True),
                                "RUNS": cells[3].get_text(strip=True),
                                "WICKETS": cells[4].get_text(strip=True),
                                "WIDES": cells[5].get_text(strip=True),
                                "NO BALLS": cells[6].get_text(strip=True),
                                "ECON": cells[7].get_text(strip=True),
                                "CLUB": club_name  # Adding club_name as a new column
                            }
                            all_bowler_data_list.append(data)

# Quit the driver
driver.quit()

# Save data to Excel
df = pd.DataFrame(all_bowler_data_list)
df.to_excel('BOWLER_performance_well_Data1.xlsx', index=False)

import pandas as pd

# Read existing Excel file into DataFrame
try:
    existing_df = pd.read_excel("BOWLER_performance_well_Data1.xlsx")
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=['ID', 'BOWLER', 'OVERS', 'MAIDENS', 'RUNS', 'WICKETS', 'WIDES', 'NO BALLS', 'ECON', 'CLUB'])

# Define new data for Durham Cricket
durham_data = {
    'BOWLER': ['Joe Chapple', 'James Dunn', 'Corey Flintoff', 'Charlie Barnard', 'Haider Hussain', 'Adnan Miakhel', 'Leo Spilsbury'],
    'OVERS': [4, 2.3, 4, 4, 3, 1, 1],
    'MAIDENS': [0, 0, 0, 0, 0, 0, 0],
    'RUNS': [22, 15, 30, 38, 35, 9, 12],
    'WICKETS': [4, 0, 0, 1, 0, 0, 0],
    'WIDES': [2, 4, 1, 0, 1, 0, 0],
    'NO BALLS': [0, 0, 0, 0, 0, 0, 0],
    'ECON': [5.5, 6.0, 7.5, 9.5, 11.67, 9.0, 12.0],
    'CLUB': ['Durham Cricket'] * 7
}

# Define new data for Lancashire Cricket
lancashire_data = {
    'BOWLER': ['Brett Hutchinson', 'Daniel Hogg', 'Sebastian Hughes Pinan', 'Kenzie Peakman', 'Charlie Scorer', 'Callum Gaffney'],
    'OVERS': [3, 4, 4, 3, 4, 2],
    'MAIDENS': [0, 0, 1, 0, 0, 0],
    'RUNS': [40, 34, 15, 30, 29, 14],
    'WICKETS': [0, 2, 1, 0, 1, 1],
    'WIDES': [3, 1, 0, 2, 0, 0],
    'NO BALLS': [0, 0, 0, 0, 0, 1],
    'ECON': [13.33, 8.5, 3.75, 10.0, 7.25, 7.0],
    'CLUB': ['Lancashire Cricket'] * 6
}

# Create new DataFrames
df_durham = pd.DataFrame(durham_data)
df_lancashire = pd.DataFrame(lancashire_data)

# Concatenate the new DataFrames
new_data_df = pd.concat([df_durham, df_lancashire], ignore_index=True)

# Concatenate existing DataFrame with new DataFrame
combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)

# Update or add the 'ID' column
combined_df['ID'] = range(1, len(combined_df) + 1)

# Write combined DataFrame back to Excel file
combined_df.to_excel("BOWLER_performance_well_Data1.xlsx", index=False, engine='openpyxl')

print("Data successfully combined and written to BOWLER_performance_well_Data1.xlsx")

import pandas as pd

# Read the existing Excel file into a DataFrame
df = pd.read_excel("BOWLER_performance_well_Data1.xlsx")

# Remove rows where the CLUB column contains 'Durham Cricket'
df = df[~df['CLUB'].str.contains('Durham Cricket', na=False)]

# Change all CLUB entries to 'Durham Cricket'
df['CLUB'] = 'Durham Cricket'

df.drop('ID', axis=1, inplace=True)


# Write the modified DataFrame back to the Excel file
df.to_excel("BOWLER_performance_well_Data.xlsx", index=False, engine='openpyxl')

print("Data successfully modified and written to BOWLER_performance_well_Data.xlsx")

