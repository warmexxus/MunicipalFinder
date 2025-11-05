#Selenium to read Javescript enabled websites to find information

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import sqlite3


#step 1 - Configure Chrome / Setup Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

#step 2 - Create folder
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#step 3 - Open a Javascript-heavy webpage
url = "https://massarbor.org/directory"
print(f"Opening {url}")
driver.get(url)

#Step 4 - Wait for JS to load (simple fixed wait for now)
time.sleep(3)

#Step 5 - Grab the full rendered HTML and text
html = driver.page_source

#Step 6 - Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

#Example: find all result blocks and their links
results = []

for item in soup.select("h5"): #<-- Replace .result with the real class/tag
    print(f"{item}")
    title = item.get_text(strip=True)
    link_tag = item.find("a")
    if link_tag and link_tag["href"]:
        link = link_tag["href"]
        results.append({"title": title, "link": link})
        # print(f"{title} - {link}")

for result in results:
    driver.get(result["link"])
    time.sleep(2)
    detail_soup = BeautifulSoup(driver.page_source, "html.parser")

    #Example: extract some info
    field_label = detail_soup.select_one("fieldLabel").get_text(strip=True) if detail_soup.select_one("fieldLabel") else None
    field_body = detail_soup.select_one("fieldBody").get_text(strip=True) if detail_soup.select_one("fieldBody") else None

    result["field label"] = field_label
    result["field_body"] = field_body
    print(f"{field_label} and {field_body}")

print(f"Found {len(results)} main results")

driver.quit()
