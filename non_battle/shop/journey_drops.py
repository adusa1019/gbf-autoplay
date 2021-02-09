import traceback
import time


class JourneyDrops:

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        url = "http://gbf.game.mbga.jp/#shop/exchange/trajectory"
        while self.driver.current_url != url:
            self.driver.get(url)

    def drop_rate(self):
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
                self.driver.find_element_by_class_name("btn-usual-ok").click()
                time.sleep(1)
                self.driver.find_element_by_class_name("btn-usual-ok").click()
                return
            except IndexError:
                continue
            except Exception:
                traceback.print_exc()
                breakpoint()
