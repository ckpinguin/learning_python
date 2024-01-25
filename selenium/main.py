from selenium import webdriver
from selenium.webdriver.common.by import By

product_name = "Ninja Foodi"
product_url = "https://www.amazon.de/dp/B09DGBJN2C"
price_threshold = 220

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--user-agent=Defined")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=product_url)

price_euro = driver.find_element(By.CLASS_NAME, value="a-price-whole").text
price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction").text
print(f"Price is EUR {price_euro}.{price_cents}")


# driver.close()
driver.quit()
