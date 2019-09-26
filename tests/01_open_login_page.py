import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

URL = "http://0.0.0.0:5000/"
WAIT_FOR_ELEMENT = 3

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=1024,768')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(URL)
time.sleep(1)

driver.find_element_by_xpath("//footer//a[contains(text(), 'Login')]").click()

assert driver.current_url == f'{URL}login'

time.sleep(30)
driver.close()