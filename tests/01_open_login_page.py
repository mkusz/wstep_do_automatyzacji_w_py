import time
from selenium import webdriver


# Constants
URL = "http://0.0.0.0:5000/"
WAIT_FOR_ELEMENT = 3

# Initialize chrome webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=1024,768')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=chrome_options)

# Open web page
driver.get(URL)
time.sleep(1)

# Click on login link
driver.find_element_by_xpath("//footer//a[contains(text(), 'Login')]").click()

# Check for login page url
assert driver.current_url == f'{URL}login'

# Close webdriver
time.sleep(10)
driver.close()
