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
driver.get("https://game.goldminer.app/#tgWebAppData=query_id%3DAAGerGA8AwAAAJ6sYDyre0JR%26user%3D%257B%2522id%2522%253A7455419550%252C%2522first_name%2522%253A%2522xnijazhy%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522xnizjazy%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1721480222%26hash%3D9ff70a651b7fc742056d400e40e55d25a284d7079425ab2b585eec8975c638d5&tgWebAppVersion=7.4&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22")

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
