from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you've set up ChromeDriver correctly

# List of filenames
filenames = [
    'BATTER_Durham City CC_Links.txt',
    'BATTER_Chester Le Street CC_Links.txt',

]

# Lists to store extracted data
bowler_data_list = []
extracted_data_urls = []

# Loop through each filename to read URLs
for filename in filenames:
    club_name_from_file = filename.split('_')[1]  # Extract the club name from the filename

    # Read page URLs from the file
    with open(filename, 'r') as f:
        urls = [line.strip() for line in f]

    # Loop through each URL to extract data
    for url in urls:
        driver.get(url)  # Open the URL with Selenium
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse the page content

        # Extract club names from tabs
        club_tags = soup.select('ul.nav.nav-tabs.nav-justified.subnav-2 li a')
        for club_tag in club_tags:
            club_name = club_tag.get_text(strip=True)
            if club_name != club_name_from_file:  # Extract data from the opposite tab
                section_id = club_tag['href'].replace('#', '')
                section_content = soup.find(id=section_id)

                # Extract bowler data
                bowler_table = section_content.find_next_sibling('table', class_='bowler-detail')
                if bowler_table:
                    tbody = bowler_table.find('tbody')
                    if tbody:
                        rows = tbody.find_all('tr')
                        for row in rows:
                            cells = row.find_all('td')
                            try:
                                bowler_name = cells[0].get_text(strip=True) if cells else "N/A"
                                data = {
                                    "BOWLER": bowler_name,
                                    "OVERS": cells[1].get_text(strip=True) if len(cells) > 1 else "N/A",
                                    "MAIDENS": cells[2].get_text(strip=True) if len(cells) > 2 else "N/A",
                                    "RUNS": cells[3].get_text(strip=True) if len(cells) > 3 else "N/A",
                                    "WICKETS": cells[4].get_text(strip=True) if len(cells) > 4 else "N/A",
                                    "WIDES": cells[5].get_text(strip=True) if len(cells) > 5 else "N/A",
                                    "NO BALLS": cells[6].get_text(strip=True) if len(cells) > 6 else "N/A",
                                    "ECON": cells[7].get_text(strip=True) if len(cells) > 7 else "N/A",
                                    "CLUB": club_name  # Add the club name here
                                }
                                bowler_data_list.append(data)
                            except IndexError:
                                print(f"Insufficient bowler data in a row of {url}")

                extracted_data_urls.append(url)

# Close Selenium WebDriver
driver.quit()

# Save the extracted bowler data to an Excel file
bowler_df = pd.DataFrame(bowler_data_list)
bowler_df.to_excel('BOWLER_All_Clubs_data.xlsx', index=False)
