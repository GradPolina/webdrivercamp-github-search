from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def navigate_to(self, url):
        self.driver.get(url)

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def find_element(self, locator):
        return (WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, locator))))

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
