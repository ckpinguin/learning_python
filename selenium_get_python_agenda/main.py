from selenium import webdriver
from selenium.webdriver.common.by import By

url = "http://python.org"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--user-agent=Defined")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=url)


events = driver.find_element(By.CLASS_NAME, "event-widget")


times = events.find_elements(By.TAG_NAME, "time")
event_entries = events.find_elements(By.TAG_NAME, "li")
event_texts = [entry.find_element(By.TAG_NAME, "a") for entry in event_entries]
events_dict = {index: {"time": time.text, "name": event.text}
               for index, (time, event) in enumerate(zip(times, event_texts))}


print(events_dict)

# driver.close()
driver.quit()
