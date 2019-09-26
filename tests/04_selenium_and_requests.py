import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
from http import HTTPStatus


WAIT_FOR_ELEMENT = 3
USERNAME = 'admin'
PASSWORD = 'default'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=1024,768')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled" : False}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

driver.get("http://0.0.0.0:5000/")
time.sleep(1)

response = requests.post(url='http://0.0.0.0:5000/login',
                         data={'username': USERNAME,
                               'password': PASSWORD},
                         allow_redirects=False
                         )

assert response.status_code == HTTPStatus.FOUND

session_key = response.cookies['session']


driver.add_cookie({'domain': '0.0.0.0',
                   'httpOnly': True,
                   'name': 'session',
                   'path': '/',
                   'secure': False,
                   'value': session_key})

driver.get("http://0.0.0.0:5000/")
time.sleep(1)

login_text = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.text_to_be_present_in_element((By.XPATH, "//footer//li[2]/a"), "New Content")
)
assert login_text == True
driver.close()
