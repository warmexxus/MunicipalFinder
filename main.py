#Selenium to read Javescript enabled websites to find information

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import sqlite3
import re


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
    # print(f"{item}")
    title = item.get_text(strip=True)
    link_tag = item.find("a")
    if link_tag and link_tag["href"]:
        link = link_tag["href"]
        results.append({"title": title, "link": link})
        print(f"{title} - {link}")

for result in results:
        link = result.get("link")
        if not link:
            print("Skipping result with no link", result)
            continue

        driver.get(link)

        time.sleep(3)

        detail_soup = BeautifulSoup(driver.page_source, "html.parser")
        for container in detail_soup.find_all("div",class_="fieldContainer"):
            label_div = container.find("div", class_="fieldLabel")
            value_div = container.find("div", class_="fieldBody")

            label = label_div.get_text(strip=True) if label_div else None
            value = value_div.get_text(strip=True) if value_div else None

            if label and value:
                results.append({label: value})

for result in results:
    print(item)

print(f"Found {len(results)} main results")

driver.quit()
