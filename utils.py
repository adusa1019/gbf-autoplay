from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait as wait


class Utils:

    def __init__(self, driver):
        self.driver = driver

    def wait_and_click_element(self, by, text, index, time):
        if index:
            wait(self.driver, time).until(ec.presence_of_all_elements_located(
                (by, text)))[index - 1].click()
        else:
            wait(self.driver, time).until(ec.element_to_be_clickable((by, text))).click()

    def wait_and_click_element_by_class_name(self, name, index=0, time=10):
        self.wait_and_click_element(By.CLASS_NAME, name, index, time)

    def wait_and_click_element_by_id(self, id_, index=0, time=10):
        self.wait_and_click_element(By.ID, id_, index, time)

    def wait_and_click_element_by_link_text(self, text, index=0, time=10):
        self.wait_and_click_element(By.LINK_TEXT, text, index, time)

    def wait_and_click_element_by_partial_link_text(self, text, index=0, time=10):
        self.wait_and_click_element(By.PARTIAL_LINK_TEXT, text, index, time)

    def wait_and_click_element_by_xpath(self, xpath, index=0, time=10):
        self.wait_and_click_element(By.XPATH, xpath, index, time)

    def wait_select_click_popup_element(self,
                                        select_by,
                                        select_text,
                                        click_by,
                                        click_text,
                                        index,
                                        time=10):
        wait(self.driver,
             10).until(ec.presence_of_element_located((By.CLASS_NAME, "prt-popup-header")))
        s = Select(self.driver.find_element(select_by, select_text))
        s.select_by_value(s.options[index].text)
        self.wait_and_click_element(click_by, click_text, 0, time)
