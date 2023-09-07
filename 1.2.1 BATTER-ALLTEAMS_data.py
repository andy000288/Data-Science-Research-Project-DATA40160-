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

# Initialize Selenium WebDriver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# List of files to process
files =['BATTER_Durham City CC_Links.txt', 'BATTER_Chester Le Street CC_Links.txt', 'BATTER_South Shields CC_Links.txt', 'BATTER_Sacriston CC_Links.txt', 'BATTER_Littletown CC_Links.txt', 'BATTER_Whitburn CC_Links.txt', 'BATTER_hylton CCC_Links.txt', 'BATTER_Seaham Harbour CC_Links.txt', 'BATTER_Burnmoor CC_Links.txt', 'BATTER_Boldon CC_Links.txt', 'BATTER_Seaham Park CC_Links.txt', 'BATTER_Sunderland CC_Links.txt', 'BATTER_Castle Eden CC_Links.txt', 'BATTER_Dawdon Welfare CC_Links.txt', 'BATTER_Ryhope CC_Links.txt', 'BATTER_Washington CC, Durham_Links.txt', 'BATTER_Bishop Auckland CC_Links.txt', 'BATTER_Willington CC_Links.txt', 'BATTER_Crook CC_Links.txt', 'BATTER_Evenwood CC_Links.txt', 'BATTER_Brandon CC, Durham_Links.txt', 'BATTER_Tudhoe CC_Links.txt', 'BATTER_Ushaw Moor CC_Links.txt']

# Initialize list to store all batter data across all files
all_batter_data_list = []

for file in files:
    # Read page URLs from the file
    with open(file, 'r') as f:
        urls = [line.strip() for line in f]

    # Extract team name from the filename
    team_name = ' '.join(file.split('_')[1:-1])

    for url in urls:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the tab containing the team name
        team_tab = soup.find('a', string=re.compile(rf'{team_name}', re.IGNORECASE))

        if team_tab:
            tab_id = team_tab['href'].replace('#', '')
            tab_content = soup.find(id=tab_id)

            if tab_content:
                # Find the batting table for the team
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
                                    "CLUB": team_name
                                }
                                all_batter_data_list.append(data)
                            except IndexError:
                                print(f"Insufficient batter data in a row of {url}")

# Close Selenium WebDriver
driver.quit()

# Save all the extracted batter data to an Excel file
all_batter_df = pd.DataFrame(all_batter_data_list)
all_batter_df.to_excel('BATTER_All_Teams_Data.xlsx', index=False)
