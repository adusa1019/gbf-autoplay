import time
import traceback


class SkipHard:
    enemys = "ティアマト"

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.continue_ = True

    def run(self):
        self.move_to_quest()
        while self.continue_:
            try:
                is_pro = self.check_enemy()
                if is_pro:
                    self.skip_pro()
            except Exception:
                traceback.print_exc()
                breakpoint()

    def check_enemy(self):
        if not self.driver.find_elements_by_class_name("prt-list-contents"):
            return False
        ele = self.driver.find_elements_by_class_name("prt-list-contents")[1]
        quest_name = ele.get_attribute("data-quest-name").replace("討伐戦", "")
        if quest_name != self.enemys:
            self.continue_ = False
        return quest_name == self.enemys

    def skip_pro(self):
        self.driver.find_elements_by_class_name("prt-list-contents")[1].click()
        time.sleep(1)
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        time.sleep(1)
        if self.driver.find_elements_by_class_name("use-item-num"):
            self.use_elixir_half()
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        self.continue_ = False
        time.sleep(5)
        self.battle_result()

    def move_to_quest(self):
        url = "http://gbf.game.mbga.jp/#quest"
        while self.driver.current_url != url:
            self.driver.get(url)

    def use_elixir_half(self, full=False):
        self.driver.find_elements_by_class_name("btn-use-full")[-1].click()
        time.sleep(1)
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        time.sleep(1)
