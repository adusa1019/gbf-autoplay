import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait as wait


class Cage:

    def __init__(self, driver):
        self.driver = driver

    def go(self, is_exchange=True):
        url = "http://gbf.game.mbga.jp/#casino"
        if is_exchange:
            url += "/exchange"
        while self.driver.current_url != url:
            self.driver.get(url)

    def move_page(self, index):
        while self.driver.find_elements_by_class_name("prt-page-number")[index].get_attribute(
                "disable") == "false":
            self.driver.find_elements_by_class_name("prt-page-number")[index].click()
            time.sleep(1)

    def daily(self, start):
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

    def buy_medal(self):
        self.go(False)
        while True:
            time.sleep(1)
            self.driver.find_element_by_class_name("btn-plus").click()
            time.sleep(1)
            ele = self.driver.find_elements_by_class_name("btn-medal")[-1]
            if ele.get_attribute("state") == "3":
                break
            ele.click()
            time.sleep(1)
            self.driver.find_element_by_class_name("btn-usual-ok").click()
            time.sleep(1)
            self.driver.refresh()

    def run(self, start=7):
        self.go()
        self.move_page(1)
        self.daily(start)
        self.buy_medal()
