import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait as wait


class Cage:

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        url = "http://gbf.game.mbga.jp/#casino/exchange"
        while self.driver.current_url != url:
            self.driver.get(url)

    def run(self, start=7):
        self.go()
        while self.driver.find_elements_by_class_name("prt-page-number")[1].get_attribute(
                "disable") == "false":
            self.driver.find_elements_by_class_name("prt-page-number")[1].click()
            time.sleep(1)
        while len(self.driver.find_elements_by_class_name("btn-exchange")) > start:
            self.driver.find_elements_by_class_name("btn-exchange")[-1].click()
            time.sleep(1)
            if len(self.driver.find_elements_by_class_name("num-set")):
                ele = Select(self.driver.find_element_by_class_name("num-set"))
                ele.select_by_value(ele.options[-1].text)
                time.sleep(1)
            self.driver.find_element_by_class_name("exchange").click()
            time.sleep(1)
            self.driver.find_element_by_class_name("btn-usual-ok").click()
            time.sleep(1)
