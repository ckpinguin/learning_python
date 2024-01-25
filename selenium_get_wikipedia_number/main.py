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


url = "https://en.wikipedia.org/wiki/Main_Page"


driver.get(url=url)

number_of_articles = driver.find_element(
    By.CSS_SELECTOR, "#articlecount > a:nth-child(1)")
# number_of_articles.click()

print(number_of_articles.text)

search = driver.find_element(By.NAME, value="search")
search.send_keys("Python")
search.send_keys(Keys.ENTER)


# driver.close()
# driver.quit()
