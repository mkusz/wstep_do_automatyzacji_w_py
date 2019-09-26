import time
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("http://0.0.0.0:5000/")
time.sleep(30)
driver.close()