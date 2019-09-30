import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


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
time.sleep(1)

# Wait for page title to be sure that web page is opened
blog_name_text = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.text_to_be_present_in_element((By.XPATH, "//nav//h1"), "Blog for testing")
)
assert blog_name_text == True

# Wait for login link to be clickable and then wait
login_link = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.element_to_be_clickable((By.XPATH, "//footer//a[contains(text(), 'Login')]")))
login_link.click()
time.sleep(1)

# Wait for login page title to be sure that web page is opened
login_text = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.text_to_be_present_in_element((By.XPATH, "//main/h2"), "Login")
)
assert login_text == True

# Wait for user name form field to be clickable and then enter user name
login_user = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.element_to_be_clickable((By.NAME, "username")))
login_user.send_keys(USERNAME)
time.sleep(1)

# Wait for password form field to be clickable and then enter user password
login_password = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
login_password.send_keys(PASSWORD)
time.sleep(1)

# Submit form without clicking submit button
login_password.submit()

# Check for new web page element to confirm that user has been logged in
login_text = WebDriverWait(driver, WAIT_FOR_ELEMENT).until(
    expected_conditions.text_to_be_present_in_element((By.XPATH, "//footer//li[2]/a"), "New Content")
)
assert login_text == True

# Print page cookies (we are looking for session token)
pprint(driver.get_cookies())

# Close webdriver
time.sleep(10)
driver.close()
