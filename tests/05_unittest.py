import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
from http import HTTPStatus


class SimpleLogin(unittest.TestCase):
    URL = "http://0.0.0.0:5000/"
    WAIT_FOR_ELEMENT = 3
    USERNAME = 'admin'
    PASSWORD = 'default'

    # =================================================================================================================
    # Framework methods
    # =================================================================================================================

    @classmethod
    def setUpClass(cls) -> None:
        cls.chrome_options = webdriver.ChromeOptions()
        cls.chrome_options.add_argument('--window-size=1024,768')
        cls.chrome_options.add_argument('--disable-default-apps')
        cls.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        cls.chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        cls.chrome_options.add_experimental_option("prefs", prefs)

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def tearDown(self) -> None:
        self.driver.close()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    # =================================================================================================================
    # Helper functions
    # =================================================================================================================

    def wait_to_be_clickable(self, xpath):
        return WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT).until(
            expected_conditions.element_to_be_clickable((By.XPATH, xpath))
        )

    def check_is_logged_in(self):
        self.assertTrue(self.wait_to_be_clickable("//footer//a[contains(text(), 'New Content')]"))

    # =================================================================================================================
    # Tests
    # =================================================================================================================

    def test_open_page(self):
        self.driver.get(self.URL)
        self.assertEqual(self.URL, self.driver.current_url)


    def test_open_login_page(self):
        self.test_open_page()

        login_link = self.wait_to_be_clickable("//footer//a[contains(text(), 'Login')]")
        login_link.click()
        self.assertEqual(f'{self.URL}login', self.driver.current_url)

    def test_login_with_selenium(self):
        self.test_open_login_page()

        login_text = WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT).until(
            expected_conditions.text_to_be_present_in_element(
                (By.XPATH, "//main/h2"), "Login")
        )
        self.assertTrue(login_text)

        login_user = self.wait_to_be_clickable("//input[@name='username']")
        login_user.send_keys(self.USERNAME)

        login_password = self.wait_to_be_clickable("//input[@name='password']")
        login_password.send_keys(self.PASSWORD)

        login_password.submit()

        self.check_is_logged_in()

    def test_login_with_requests(self):
        self.test_open_page()

        response = requests.post(url=f'{self.URL}login',
                                 data={'username': self.USERNAME,
                                       'password': self.PASSWORD},
                                 allow_redirects=False
                                 )
        self.assertEqual(HTTPStatus.FOUND, response.status_code)

        session_key = response.cookies['session']
        self.driver.add_cookie({'domain': '0.0.0.0',
                                'httpOnly': True,
                                'name': 'session',
                                'path': '/',
                                'secure': False,
                                'value': session_key})

        self.test_open_page()
        self.check_is_logged_in()
