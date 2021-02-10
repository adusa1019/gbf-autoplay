import time


class Gacha:

    def __init__(self, driver):
        self.driver = driver

    def go(self, is_normal=True):
        url = "http://gbf.game.mbga.jp/?#gacha"
        if is_normal:
            url += "/normal"
        while self.driver.current_url != url:
            self.driver.get(url)

    def lupi(self):
        self.go()
        while len(self.driver.find_elements_by_class_name("btn-lupi")):
            self.driver.find_element_by_class_name("btn-lupi").click()
            time.sleep(5)
            while len(self.driver.find_elements_by_id("cjs-gacha")):
                self.driver.find_element_by_id("cjs-gacha").click()
                time.sleep(5)
