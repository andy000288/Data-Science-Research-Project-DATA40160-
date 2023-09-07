import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Set up the Selenium driver
chromedriver_path = "D:\path\dongling\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Dictionary of websites with their corresponding labels
websites = {
    "Durham City CC":"https://durhamcity.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=12256&view_by=year&view_by=year&team_id=12256&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Chester Le Street CC":"https://cles.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=23656&view_by=year&view_by=year&team_id=23656&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "South Shields CC":"https://southshields.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=182579&view_by=year&view_by=year&team_id=182579&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Sacriston CC":"https://sacriston.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=84228&view_by=year&view_by=year&team_id=84228&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    #"Lanchester CC":"https://lanchester.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=128155&view_by=year&view_by=year&team_id=128155&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Littletown CC":"https://littletowncc.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=277745&view_by=year&view_by=year&team_id=277745&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both",
    "Whitburn CC":"https://whitburn.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=78937&view_by=year&view_by=year&team_id=78937&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "hylton CCC":"https://hylton.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=306358&view_by=year&view_by=year&team_id=306358&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Seaham Harbour CC":"https://seaham.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=64810&view_by=year&view_by=year&team_id=64810&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Burnmoor CC":"https://burnmoor.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=7&season_id=256&season_id=256&team_id=103545&view_by=year&view_by=year&team_id=103545&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Boldon CC":"https://boldon.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=354&view_by=year&view_by=year&team_id=354&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Seaham Park CC":"https://seahampark.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=59210&view_by=year&view_by=year&team_id=59210&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Sunderland CC":"https://sunderland.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=68800&view_by=year&view_by=year&team_id=68800&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Castle Eden CC":"https://castleeden.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=95486&view_by=year&view_by=year&team_id=95486&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Dawdon Welfare CC":"https://dawdonwelfare.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=36086&view_by=year&view_by=year&team_id=36086&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Ryhope CC":"https://ryhope.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=212&view_by=year&view_by=year&team_id=212&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Washington CC, Durham":"https://washington.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=39303&view_by=year&view_by=year&team_id=39303&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    "Bishop Auckland CC":'https://bishopauckland.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=293436&view_by=year&view_by=year&team_id=293436&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply',
    "Willington CC":'https://willington.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=18784&view_by=year&view_by=year&team_id=18784&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply',
    "Crook CC":'https://crook.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=31686&view_by=year&view_by=year&team_id=31686&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply',
    "Evenwood CC":'https://evenwood.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=102808&view_by=year&view_by=year&team_id=102808&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply',
    'Brandon CC, Durham':'https://brandon.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=35252&view_by=year&view_by=year&team_id=35252&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply',
    'Tudhoe CC':"https://tudhoe.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=48711&view_by=year&view_by=year&team_id=48711&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply",
    'Ushaw Moor CC':"https://ushawmoor.play-cricket.com/Matches?utf8=%E2%9C%93&tab=Result&selected_season_id=256&seasonchange=f&fixture_month=8&season_id=256&season_id=256&team_id=211311&view_by=year&view_by=year&team_id=211311&search_in=Division&q%5Bcategory_id%5D=all&q%5Bgender_id%5D=all&home_or_away=both&commit=Apply"
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
        print(f"{label} There are no matching matches.")

    # Store URLs along with label
    all_page_urls.append((label, page_urls))


# List to store generated filenames
generated_files = []

# Output the page URLs with labels to separate files
for label, urls in all_page_urls:
    # Constructing the filename
    # e.g., 'BATTER_South Shields CC_Links.txt'
    filename = 'BATTER_' + label + '_Links.txt'
    generated_files.append(filename)  # Add the filename to the list

    with open(filename, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")

time.sleep(30)
driver.quit()

# Print the list of generated files
print(generated_files)

