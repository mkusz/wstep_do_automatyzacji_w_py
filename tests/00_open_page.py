import time
from selenium import webdriver


# Initialize chrome webdriver
driver = webdriver.Chrome()

# Open web page
driver.get("http://0.0.0.0:5000/")

# Close webdriver
time.sleep(10)
driver.close()
