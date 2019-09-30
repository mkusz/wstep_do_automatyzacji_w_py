import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
from http import HTTPStatus


# Constants
URL = "http://0.0.0.0:5000/"
WAIT_FOR_ELEMENT = 3
USERNAME = 'admin'
PASSWORD = 'default'

# Initialize chrome webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=1024,768')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled" : False}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

# Open web page
driver.get(URL)
time.sleep(3)

# Send request to web server to mimic login page form submission
response = requests.post(url=f"{URL}login",
                         data={'username': USERNAME,
                               'password': PASSWORD},
                         allow_redirects=False
                         )

# Verify response status code
assert response.status_code == HTTPStatus.FOUND

# Add cookie with session token to web browser
driver.add_cookie({'domain': '0.0.0.0',
                   'httpOnly': True,
                   'name': 'session',
                   'path': '/',
                   'secure': False,
                   'value': response.cookies['session']})

# Open web page
driver.get(URL)
time.sleep(10)

# Check for new web page element to confirm that user has been logged in
login_text = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.text_to_be_present_in_element((By.XPATH, "//footer//li[2]/a"), "New Content")
)
assert login_text == True

# Close webdriver
driver.close()
