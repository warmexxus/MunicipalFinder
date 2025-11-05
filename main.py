#Selenium to read Javescript enabled websites to find information

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

#step 1 - Configure Chrome
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

print("\n--- HTML ---")
print(html[:1000])  #print first 1000 characters for inspection

print("\n--- TEXT ---")
print(driver.find_element("tag name", "body").text[:1000])  #readable text of page

driver.quit()
