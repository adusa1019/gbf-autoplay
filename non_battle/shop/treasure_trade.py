import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait as wait


class TreasureTrade:

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        url = "http://gbf.game.mbga.jp/#shop/exchange/list"
        while self.driver.current_url != url:
            self.driver.get(url)


class Item(TreasureTrade):

    def go(self):
        super().go()
        wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-switch-item"))).click()

    def select_tab(self, category, item, name=None):
        wait(self.driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-pop-filter")))
        while self.driver.find_element_by_class_name("btn-pop-filter").text != name:
            self.driver.find_element_by_class_name("btn-pop-filter").click()
            time.sleep(1)
            self.driver.find_elements_by_class_name("btn-filter-category")[category].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name("btn-filter-item")[item].click()
            if name is None:
                time.sleep(1)
                self.driver.refresh()
                break

    # TODO: need tuning waiting time
    def half_elixirs(self, start=3):
        self.select_tab(1, 1, name="エリクシールハーフ")
        while len(self.driver.find_elements_by_class_name("lis-item-open")) > start:
            time.sleep(1)
            self.driver.find_elements_by_class_name("btn-exchange")[-1].click()
            time.sleep(1)
            if self.driver.find_element_by_class_name("num-set").is_displayed():
                ele = Select(self.driver.find_element_by_class_name("num-set"))
                ele.select_by_value(ele.options[-1].text)
                time.sleep(1)
            wait(self.driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "buy"))).click()
            time.sleep(1)
            wait(self.driver, 10).until(ec.element_to_be_clickable(
                (By.CLASS_NAME, "btn-usual-ok"))).click()
            time.sleep(1)

    def showdowns(self):
        pass


class Treasure(TreasureTrade):

    def go(self):
        super().go()
        wait(self.driver,
             10).until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-switch-treasure"))).click()

    def select_tab(self, value, name=None):
        ele = wait(self.driver, 10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "frm-list-select-treasure")))
        ele = Select(ele)
        while ele.all_selected_options[0].text != name:
            ele.select_by_value(value)
            if name is None:
                time.sleep(1)
                self.driver.refresh()
                break

    def prisms(self):
        self.select_tab("5", name='星晶')
        # TODO: impl


class DailyTrade:

    def __init__(self, driver):
        self.item = Item(driver)

    def run(self):
        self.item.go()
        self.item.half_elixirs()
