from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SimpleChromeDriver(webdriver.Chrome):

    def find(self, selector):
        return self.find_element_by_css_selector(selector)

    def fill_field(self, selector, value):
        field = self.find(selector)
        field.clear()
        field.send_keys(value)

    def wait_on_ec(self, ec):
        wait = WebDriverWait(self, 10)
        return wait.until(ec)

    def wait_till_clickable(self, selector):
        return self.wait_on_ec(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))

    def wait_till_visible(self, selector):
        return self.wait_on_ec(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
