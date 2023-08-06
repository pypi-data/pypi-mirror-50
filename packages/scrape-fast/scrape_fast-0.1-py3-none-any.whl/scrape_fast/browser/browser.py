import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    """ class for controling webdriver browser instance """

    def __init__(self, browser='chrome'):
        self.driver = self.open_browser(browser)

    @staticmethod
    def open_browser(browser):
        """
        Open webdriver and set options
        :param browser: string specifying browser type
        :return: webdriver object
        """
        browsers = {
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox
        }
        driver = browsers[browser]()
        return driver

    def endless_scroll(self):
        pass

    def scroll_to_bottom(self):
        """ Scrolls to the bottom of the page """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def wait_for_element_to_load(self, search_for: int, by='id', wait_for=10):
        """
        Waits for element to load
        :param search_for: string specifing element to look for
        :param by: string specifing what is previous string
        :param wait_for: amount of seconds to wait for element to load
        :return: True if element loaded False if not
        """
        find_by = {
            'id': By.ID,
            'xpath': By.XPATH,
            'class': By.CLASS_NAME,
            'css': By.CSS_SELECTOR,
            'name': By.NAME
        }
        try:
            element = WebDriverWait(self.driver, wait_for).until(
                EC.presence_of_element_located((find_by[by], search_for))
            )
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True
