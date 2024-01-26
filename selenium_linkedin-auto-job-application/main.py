from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import json

try:
    with open(".secret.json", "r") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)

LOGIN = config_data["LOGIN"]
PASSWORD = config_data["PASSWORD"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--user-agent=Defined")

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=chrome_options)


url = ("https://www.linkedin.com/jobs/search/?currentJobId=3586148395&f_LF=f_AL&geoId=101356765&"
       "keywords=python&location=London%2C%20England%2C%20United%20Kingdom&refresh=true")

driver.get(url=url)

# Click Reject Cookies Button
time.sleep(2)
reject_button = driver.find_element(
    by=By.CSS_SELECTOR, value='button[action-type="DENY"]')
reject_button.click()

# Login
sign_in_button = driver.find_element(by=By.LINK_TEXT, value="Sign in")
sign_in_button.click()
time.sleep(1)
usernameField = driver.find_element(By.ID, "username")
passwordField = driver.find_element(By.ID, "password")

usernameField.send_keys(LOGIN)
passwordField.send_keys(PASSWORD)
passwordField.send_keys(Keys.ENTER)
# driver.implicitly_wait(10)

""" first_name_input.send_keys("John")
last_name_input.send_keys("Johnson")
email_input.send_keys("john@johnson.com")
submit_button.click() """


# driver.close()
# driver.quit()
