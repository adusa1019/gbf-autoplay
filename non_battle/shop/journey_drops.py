import traceback
import time
from selenium.webdriver.support.ui import Select


class JourneyDrops:

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        url = "http://gbf.game.mbga.jp/#shop/exchange/trajectory"
        while self.driver.current_url != url:
            self.driver.get(url)

    def drop_rate(self, index=0):
        self.go()
        while True:
            try:
                es = self.driver.find_elements_by_class_name("btn-use-support")
                if es[-1].find_element_by_xpath("..").text.split()[0] != 'アイテムドロップ率UP':
                    return
                es[-1].click()
                time.sleep(1)
                self.driver.find_elements_by_class_name("btn-level")[-1].click()
                time.sleep(1)
                ele = Select(self.driver.find_element_by_class_name("num-time"))
                ele.select_by_value(ele.options[index].text)
                time.sleep(1)
                self.driver.find_element_by_class_name("btn-usual-ok").click()
                time.sleep(1)
                self.driver.find_element_by_class_name("btn-usual-ok").click()
                return
            except IndexError:
                continue
            except Exception:
                traceback.print_exc()
                breakpoint()
