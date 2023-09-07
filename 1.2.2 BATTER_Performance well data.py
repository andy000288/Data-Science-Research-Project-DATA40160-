import time
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Set up the Selenium driver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Target website and label
website = "https://durhamcb.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=255910&view_by=year&view_by=year&team_id=255910&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply"
label = "Durham Cricket"

# Extract match links from the target website
driver.get(website)
wait = WebDriverWait(driver, 10)
page_urls = []

while True:
    try:
        scorecard_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'link-scorecard') and contains(@class, 'd-none d-md-inline-block rounded-circle')]")))
        for icon in scorecard_icons:
            link_url = icon.get_attribute("href")
            page_urls.append(link_url)
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
        wait.until(EC.staleness_of(scorecard_icons[0]))
        time.sleep(2)
    except (NoSuchElementException, TimeoutException):
        break

# Store URLs to a file
filename = 'BATTER_' + label + '_Links.txt'
with open(filename, 'w') as f:
    for url in page_urls:
        f.write(f"{url}\n")

# Store URLs to a file
filename = 'BATTER_' + label + '_Links.txt'
print(f"Saving links to file: {filename}")  # 打印文件名
with open(filename, 'w') as f:
    for url in page_urls:
        f.write(f"{url}\n")

# Extract batter data from the match links
all_batter_data_list = []

for url in page_urls:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the tab containing "Durham Cricket"
    durham_tab = soup.find('a', string=re.compile(r'Durham Cricket', re.IGNORECASE))

    if durham_tab:
        tab_id = durham_tab['href'].replace('#', '')
        tab_content = soup.find(id=tab_id)

        if tab_content:
            # Find the batting table for "Durham Cricket"
            batter_table = tab_content.find('table')

            if batter_table:
                tbody = batter_table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    for row in rows:
                        cells = row.find_all('td')
                        try:
                            batter_link = cells[0].find('a')
                            batter_name = batter_link.get_text(strip=True) if batter_link else "N/A"
                            batter_id_match = re.search(r'/player_stats/batting/(\d+)\?', str(batter_link))
                            batter_id = batter_id_match.group(1) if batter_id_match else "N/A"
                            # Define team_name within this loop
                            team_name = '_'.join(filename.split('_')[1:-1]).replace('_', ' ')
                            data = {
                                "ID": batter_id,
                                "BATTER": batter_name,
                                "RUNS": cells[3].get_text(strip=True) if len(cells) > 3 else "N/A",
                                "BALLS": cells[4].get_text(strip=True) if len(cells) > 4 else "N/A",
                                "4s": cells[5].get_text(strip=True) if len(cells) > 5 else "N/A",
                                "6s": cells[6].get_text(strip=True) if len(cells) > 6 else "N/A",
                                "SR": cells[7].get_text(strip=True) if len(cells) > 7 else "N/A",
                                "CLUB": team_name
                            }
                            all_batter_data_list.append(data)
                        except IndexError:
                            print(f"Insufficient batter data in a row of {url}")

# ... (rest of the code)

# Close Selenium WebDriver
driver.quit()

# Save the extracted batter data to an Excel file
all_batter_df = pd.DataFrame(all_batter_data_list)
all_batter_df.to_excel('BATTER_Performance well_Data1.xlsx', index=False)


import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def extract_batter_data(soup, tab_id_str, club_name):
    batter_data_list = []
    durham_tab = soup.find('a', id=tab_id_str)
    if durham_tab:
        tab_id = durham_tab['href'].replace('#', '')
        tab_content = soup.find(id=tab_id)

        if tab_content:
            batter_table = tab_content.find('table')

            if batter_table:
                tbody = batter_table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    for row in rows:
                        cells = row.find_all('td')
                        try:
                            batter_link = cells[0].find('a')
                            batter_name = batter_link.get_text(strip=True) if batter_link else "N/A"
                            batter_id_match = re.search(r'/player_stats/batting/(\d+)\?', str(batter_link))
                            batter_id = batter_id_match.group(1) if batter_id_match else "N/A"
                            data = {
                                "ID": batter_id,
                                "BATTER": batter_name,
                                "RUNS": cells[3].get_text(strip=True) if len(cells) > 3 else "N/A",
                                "BALLS": cells[4].get_text(strip=True) if len(cells) > 4 else "N/A",
                                "4s": cells[5].get_text(strip=True) if len(cells) > 5 else "N/A",
                                "6s": cells[6].get_text(strip=True) if len(cells) > 6 else "N/A",
                                "SR": cells[7].get_text(strip=True) if len(cells) > 7 else "N/A",
                                "CLUB": club_name
                            }
                            batter_data_list.append(data)
                        except IndexError:
                            print(f"Insufficient batter data in a row")
    return batter_data_list

# Set up the Selenium driver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Target website
website = "https://durhamcb.play-cricket.com/website/results/5527676"
driver.get(website)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the table data for the two innings
all_batter_data_list = []
all_batter_data_list += extract_batter_data(soup, "innings6975607-tab", "Durham Cricket 1st Innings")
all_batter_data_list += extract_batter_data(soup, "innings6978690-tab", "Durham Cricket 2nd Innings")

# Close Selenium WebDriver
driver.quit()

# Save the extracted batter data to an Excel file
all_batter_df = pd.DataFrame(all_batter_data_list)
all_batter_df.to_excel('BATTER_Performance_Data_From_Specified_Link.xlsx', index=False)

import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def extract_batter_data(soup, tab_id, innings_name):
    batter_data_list = []
    tab_content = soup.find(id=tab_id)
    if tab_content:
        batter_table = tab_content.find('table')
        if batter_table:
            tbody = batter_table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    try:
                        batter_link = cells[0].find('a')
                        batter_name = batter_link.get_text(strip=True) if batter_link else "N/A"
                        batter_id_match = re.search(r'/player_stats/batting/(\d+)\?', str(batter_link))
                        batter_id = batter_id_match.group(1) if batter_id_match else "N/A"
                        data = {
                            "ID": batter_id,
                            "BATTER": batter_name,
                            "RUNS": cells[3].get_text(strip=True) if len(cells) > 3 else "N/A",
                            "BALLS": cells[4].get_text(strip=True) if len(cells) > 4 else "N/A",
                            "4s": cells[5].get_text(strip=True) if len(cells) > 5 else "N/A",
                            "6s": cells[6].get_text(strip=True) if len(cells) > 6 else "N/A",
                            "SR": cells[7].get_text(strip=True) if len(cells) > 7 else "N/A",
                            "CLUB": "Durham Cricket",
                            "INNINGS": innings_name
                        }
                        batter_data_list.append(data)
                    except IndexError:
                        print(f"Insufficient batter data in a row for {innings_name}")
    return batter_data_list

# Set up the Selenium driver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Target website
website = "https://durhamcb.play-cricket.com/website/results/5527673"
driver.get(website)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the table data for the two innings
all_batter_data_list = []
all_batter_data_list += extract_batter_data(soup, "innings6957405", "Durham Cricket 1st Innings")
all_batter_data_list += extract_batter_data(soup, "innings6958163", "Durham Cricket 2nd Innings")

# Close Selenium WebDriver
driver.quit()

# Save the extracted batter data to an Excel file
all_batter_df = pd.DataFrame(all_batter_data_list)
all_batter_df.to_excel('BATTER_Performance_Data_From_Specified_Link2.xlsx', index=False)

import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def extract_batter_data(soup, tab_id, innings_name):
    batter_data_list = []
    tab_content = soup.find(id=tab_id)
    if tab_content:
        batter_table = tab_content.find('table')
        if batter_table:
            tbody = batter_table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    try:
                        batter_link = cells[0].find('a')
                        batter_name = batter_link.get_text(strip=True) if batter_link else "N/A"
                        batter_id_match = re.search(r'/player_stats/batting/(\d+)\?', str(batter_link))
                        batter_id = batter_id_match.group(1) if batter_id_match else "N/A"
                        data = {
                            "ID": batter_id,
                            "BATTER": batter_name,
                            "RUNS": cells[3].get_text(strip=True) if len(cells) > 3 else "N/A",
                            "BALLS": cells[4].get_text(strip=True) if len(cells) > 4 else "N/A",
                            "4s": cells[5].get_text(strip=True) if len(cells) > 5 else "N/A",
                            "6s": cells[6].get_text(strip=True) if len(cells) > 6 else "N/A",
                            "SR": cells[7].get_text(strip=True) if len(cells) > 7 else "N/A",
                            "CLUB": "Durham Cricket",
                            "INNINGS": innings_name
                        }
                        batter_data_list.append(data)
                    except IndexError:
                        print(f"Insufficient batter data in a row for {innings_name}")
    return batter_data_list

# Set up the Selenium driver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Target website (you can change this link as needed)
website = "https://durhamcb.play-cricket.com/website/results/5527679"
driver.get(website)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the table data for the two innings (change the IDs as needed)
all_batter_data_list = []
all_batter_data_list += extract_batter_data(soup, "innings6933223", "Durham Cricket 1st Innings")
all_batter_data_list += extract_batter_data(soup, "innings6936020", "Durham Cricket 2nd Innings")

# Close Selenium WebDriver
driver.quit()

# Save the extracted batter data to an Excel file
all_batter_df = pd.DataFrame(all_batter_data_list)
all_batter_df.to_excel('BATTER_Performance_Data_From_Specified_Link3.xlsx', index=False)

import pandas as pd
import numpy as np

data_list = [
    {"BATTERS": "Charlie Coulthard", "RUNS": 2, "BALLS": 5, "MINS": 12, "4s": 0, "6s": 0, "SR": 40.00},
    {"BATTERS": "Daniel Hogg", "RUNS": 17, "BALLS": 18, "MINS": 22, "4s": 1, "6s": 0, "SR": 94.44},
    {"BATTERS": "Callum Gaffney", "RUNS": 7, "BALLS": 17, "MINS": 21, "4s": 0, "6s": 0, "SR": 41.18},
    {"BATTERS": "Hayden Mustard", "RUNS": 89, "BALLS": 47, "MINS": 60, "4s": 8, "6s": 5, "SR": 189.36},
    {"BATTERS": "Luke symington", "RUNS": 35, "BALLS": 25, "MINS": 37, "4s": 3, "6s": 1, "SR": 140.00},
    {"BATTERS": "Sebastian Hughes Pinan", "RUNS": 0, "BALLS": 2, "MINS": 2, "4s": 0, "6s": 0, "SR": 0.00},
    {"BATTERS": "Robbie Bowman", "RUNS": 3, "BALLS": 3, "MINS": 8, "4s": 0, "6s": 0, "SR": 100.00},
    {"BATTERS": "Kenzie Peakman", "RUNS": None, "BALLS": None, "MINS": None, "4s": None, "6s": None, "SR": None},
    {"BATTERS": "Jack Brassell", "RUNS": np.nan, "BALLS": np.nan, "MINS": np.nan, "4s": np.nan, "6s": np.nan, "SR": np.nan},
    {"BATTERS": "Brett Hutchinson", "RUNS": np.nan, "BALLS": np.nan, "MINS": np.nan, "4s": np.nan, "6s": np.nan, "SR": np.nan},
    {"BATTERS": "Charlie Scorer", "RUNS": np.nan, "BALLS": np.nan, "MINS": np.nan, "4s": np.nan, "6s": np.nan, "SR": np.nan},
]

df_new_data = pd.DataFrame(data_list)

# Try to read the existing Excel file. If not found, create an empty DataFrame.
try:
    df_existing = pd.read_excel('BATTER_Performance_Data_From_Specified_Link3.xlsx')
except FileNotFoundError:
    df_existing = pd.DataFrame()

# Combine the existing data and the new data
df_combined = pd.concat([df_existing, df_new_data], ignore_index=True)

# Save the combined data to an Excel file
df_combined.to_excel('BATTER_Performance_Data_From_Specified_Link3.xlsx', index=False)

# Read four Excel files
df1 = pd.read_excel('BATTER_Performance_Data_From_Specified_Link.xlsx')
df2 = pd.read_excel('BATTER_Performance_Data_From_Specified_Link2.xlsx')
df3 = pd.read_excel('BATTER_Performance well_Data1.xlsx')
df4 = pd.read_excel('BATTER_Performance_Data_From_Specified_Link3.xlsx')

# Merge these four DataFrames
merged_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Merge 'BATTERS' and 'BATTER' columns if they exist
if 'BATTERS' in merged_df.columns:
    merged_df['BATTER'] = merged_df.apply(lambda row: row['BATTERS'] if pd.notna(row['BATTERS']) else row['BATTER'],
                                          axis=1)
    # Delete the 'BATTERS' column
    del merged_df['BATTERS']

# Delete 'INNINGS' and 'MINS' columns if they exist
for col in ['INNINGS', 'MINS']:
    if col in merged_df.columns:
        del merged_df[col]

# Change all the content of 'CLUB' column to 'Durham Cricket'
merged_df['CLUB'] = 'Durham Cricket'

# Save the merged DataFrame to a new Excel file
merged_df.to_excel('BATTER_Performance well_Data.xlsx', index=False)
