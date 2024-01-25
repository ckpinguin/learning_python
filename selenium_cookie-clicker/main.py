from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--user-agent=Defined")

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=chrome_options)


url = "https://orteil.dashnet.org/cookieclicker/"
duration = 300  # 5 mins
buy_interval = 10  # secs

driver.get(url=url)

driver.implicitly_wait(10)
driver.find_element(By.ID, "langSelect-EN").click()

bigCookie = driver.find_element(By.ID, value="bigCookie")


def buy_most_expensive_item(sorted_products):
    cash = get_number_of_cookies()
    for product in sorted_products:
        if get_price(product) <= cash:
            name = product.find_element(By.CLASS_NAME, "productName").text
            print(f"Buying {name}")
            driver.execute_script("arguments[0].click();", product)
            break


def buy_upgrade():
    upgrade = driver.find_element(By.ID, value="upgrade0")
    if upgrade:
        print("Buying upgrade")
        upgrade.click()
    else:
        print("No upgrades available")


def get_price(product):
    price_text = product.find_element(
        By.CLASS_NAME, "price").text
    try:
        return int(price_text.replace(',', ''))
    except ValueError:
        return 0


def get_number_of_cookies():
    cookies_stats = driver.find_element(By.ID, value="cookies")
    no_of_cookies = int(cookies_stats.text.split()[0].replace(',', ''))
    return no_of_cookies


# Get the current time
end_runtime = time.time() + duration

start_time = time.time()
item_start_time = start_time

while time.time() < end_runtime:
    buy_timer = time.time() + buy_interval
    while time.time() < buy_timer:
        bigCookie.click()

    print(f"Cookies: {get_number_of_cookies()}")
    products = driver.find_elements(By.CLASS_NAME, value="product")
    sorted_products = sorted(products, key=get_price, reverse=True)
    buy_upgrade()
    buy_most_expensive_item(sorted_products)

""" first_name_input.send_keys("John")
last_name_input.send_keys("Johnson")
email_input.send_keys("john@johnson.com")
submit_button.click() """


# driver.close()
# driver.quit()
