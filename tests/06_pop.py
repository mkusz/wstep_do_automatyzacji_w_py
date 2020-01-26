import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
from http import HTTPStatus


class XPath(object):
    def __init__(self, value):
        self._value = value
        self._element = None

    def __repr__(self):
        return self._value

    def find_me(self, drv):
        self._element = drv.find_element_by_xpath(str(self))
        action = ActionChains(drv)
        action.move_to_element(self._element)
        action.perform()
        return self._element

    @property
    def locator(self):
        return By.XPATH, self._value


class AbstractPageObject(object):
    WAIT_FOR_ELEMENT = 5
    POOLING_WAIT = 1

    def __init__(self, drv):
        self._drv: webdriver.Chrome = drv
        self.url = None

    def _wait_for_element(self, condition):
        return WebDriverWait(driver=self._drv, timeout=self.WAIT_FOR_ELEMENT,
                             poll_frequency=self.POOLING_WAIT).until(condition)

    def find_element(self, element: XPath):
        return element.find_me(self._drv)

    def open_page(self):
        self._drv.get(self.url)

    @property
    def current_url(self):
        return self._drv.current_url

    def wait_to_be_clickable(self, element: XPath):
        condition = expected_conditions.element_to_be_clickable(element.locator)
        return self._wait_for_element(condition)

    def text_to_be_present_in_element(self, element: XPath, text: str):
        condition = expected_conditions.text_to_be_present_in_element(element.locator, text)
        return self._wait_for_element(condition)


class MainPageObject(AbstractPageObject):
    INPUT_USERNAME = XPath("//input[@name='username']")
    INPUT_PASSWORD = XPath("//input[@name='password']")
    MAIN_TITLE_TEXT = XPath("//main/h2")
    FOOTER_LINK_LOGIN = XPath("//footer//a[contains(text(), 'Login')]")
    FOOTER_LINK_NEW_CONTEXT = XPath("//footer//a[contains(text(), 'New Content')]")

    def __init__(self, drv):
        super().__init__(drv)
        self.url = "http://0.0.0.0:5000/"



class SimpleLogin(unittest.TestCase):
    # Constants
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
        self.main_page_obj = MainPageObject(self.driver)

    def tearDown(self) -> None:
        self.driver.close()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def check_is_logged_in(self):
        self.assertTrue(self.main_page_obj.wait_to_be_clickable(self.main_page_obj.FOOTER_LINK_NEW_CONTEXT))

    # =================================================================================================================
    # Tests (each function with name started with 'test_'
    # =================================================================================================================

    def test_open_page(self):
        self.main_page_obj.open_page()
        self.assertEqual(self.main_page_obj.url, self.main_page_obj.current_url)

    def test_open_login_page(self):
        self.test_open_page()
        login_link = self.main_page_obj.wait_to_be_clickable(self.main_page_obj.FOOTER_LINK_LOGIN)
        login_link.click()
        self.assertEqual(f'{self.main_page_obj.url}login', self.main_page_obj.current_url)

    def test_login_with_selenium(self):
        self.test_open_login_page()
        login_text = self.main_page_obj.text_to_be_present_in_element(self.main_page_obj.MAIN_TITLE_TEXT, "Login")
        self.assertTrue(login_text)

        login_user = self.main_page_obj.wait_to_be_clickable(self.main_page_obj.INPUT_USERNAME)
        login_user.send_keys(self.USERNAME)

        login_password = self.main_page_obj.wait_to_be_clickable(self.main_page_obj.INPUT_PASSWORD)
        login_password.send_keys(self.PASSWORD)

        login_password.submit()

        self.check_is_logged_in()

    def test_login_with_requests(self):
        self.test_open_page()

        response = requests.post(url=f'{self.main_page_obj.url}login',
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
