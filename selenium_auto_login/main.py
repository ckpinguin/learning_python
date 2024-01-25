from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--user-agent=Defined")

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=chrome_options)


url = "https://secure-retreat-92358.herokuapp.com"


driver.get(url=url)


first_name_input = driver.find_element(By.NAME, value="fName")
last_name_input = driver.find_element(By.NAME, value="lName")
email_input = driver.find_element(By.NAME, value="email")
submit_button = driver.find_element(By.CSS_SELECTOR, "form button")
first_name_input.send_keys("John")
last_name_input.send_keys("Johnson")
email_input.send_keys("john@johnson.com")
submit_button.click()


# driver.close()
# driver.quit()
