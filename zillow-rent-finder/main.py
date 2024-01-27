import requests
from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time

zillow_url = "https://appbrewery.github.io/Zillow-Clone/"

try:
    with open(".secret.json", "r") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)


# Get 3 lists for the rental objects
response = requests.get(zillow_url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

all_anchors = soup.find_all(name="a", class_="property-card-link")

href_list = [anchor.get('href') for anchor in all_anchors]

all_prices = soup.find_all(
    name="span", class_="PropertyCardWrapper__StyledPriceLine")

price_list = [re.sub(r'[^0-9,$]', '', price.get_text())
              for price in all_prices]

all_addresses = soup.find_all(name="address")
address_list = [re.sub(r'[|\^]', '', address.get_text(strip=True))
                for address in all_addresses]


# Fill out the form
GOOGLE_FORM_URL = config_data.get('GOOGLE_FORM_URL')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--user-agent=Defined")
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=chrome_options)
driver.get(url=GOOGLE_FORM_URL)
driver.implicitly_wait(3)
# address_input = WebDriverWait(driver, 2).until(
# EC.presence_of_element_located((By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")))
# mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input


time.sleep(2)


for i in range(0, len(all_prices)):
    address_input = driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(
        By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input"
    )
    link_input = driver.find_element(
        By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input"
    )
    send_button = driver.find_element(
        By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div")

    print(f"Filling in address: {address_list[i]}")
    address_input.send_keys(address_list[i])
    price_input.send_keys(price_list[i])
    link_input.send_keys(href_list[i])
    send_button.click()
    time.sleep(1)
    more_answers_anchor = driver.find_element(
        By.CSS_SELECTOR, "body > div.Uc2NEf > div:nth-child(2) > div.RH5hzf.RLS9Fe > div > div.c2gzEf > a")
    more_answers_anchor.click()
    time.sleep(1)
