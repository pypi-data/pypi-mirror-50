from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

timeout = 30


class Helper:
    def __init__(self, driver):
        self.driver = driver

    def find_by_class_name_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.CLASS_NAME, locator)))

    def find_by_class_name_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.CLASS_NAME, locator)))

    def find_by_tag_name_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.TAG_NAME, locator)))

    def find_by_tag_name_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.TAG_NAME, locator)))

    def find_by_link_text_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.LINK_TEXT, locator)))

    def find_by_link_text_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.LINK_TEXT, locator)))

    def find_by_xpath_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.XPATH, locator)))

    def find_by_xpath_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.XPATH, locator)))

    def find_by_name_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.NAME, locator)))

    def find_by_name_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.NAME, locator)))

    def find_by_id_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.ID, locator)))

    def find_by_id_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.ID, locator)))

    def find_by_css_of_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_element_located((By.CSS_SELECTOR, locator)))

    def find_by_css_of_all_wait(self, locator):
        return WebDriverWait(self.driver, timeout).until\
            (EC.presence_of_all_elements_located((By.CSS_SELECTOR, locator)))
