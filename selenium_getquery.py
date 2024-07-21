from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open a webpage
driver.get("https://game.goldminer.app/")

# Wait for the page to load completely
time.sleep(5)

# Execute JavaScript to get session storage
session_storage = driver.execute_script("return window.sessionStorage;")

# Print the session storage
# print(session_storage)

# You can also get specific items from the session storage
item_key = "__telegram__initParams"  # replace with your actual session storage key
item_value = driver.execute_script(f"return window.sessionStorage.getItem('{item_key}');")

# Parse the JSON string
data = json.loads(item_value)

# Extract the tgWebAppData string
tg_web_app_data = data['tgWebAppData']

# Print the extracted data
print(tg_web_app_data)

# Close the browser
driver.quit()
