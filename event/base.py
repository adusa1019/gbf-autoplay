import time
import traceback

from battle.base import Battle


class Event(Battle):

    def __init__(self, driver, config):
        super().__init__(driver,
                         supporter=config.get("supporter", None),
                         supporter2=config.get("supporter2", None))
        self.target = config.get("target")
        self.use_debuff = config.get("use_debuff", False)
        self.use_treasure_hunt = config.get("use_treasure_hunt", False)
        self.url = config.get("url", None)

    def move_to_event(self):
        if self.url:
            self.base_url = "http://gbf.game.mbga.jp/#event/" + self.url
            self.driver.get(self.base_url)
        else:
            self.utils.wait_and_click_element_by_class_name("btn-head-pop")
            self.utils.wait_and_click_element_by_class_name("img-global-banner")
            self.base_url = self.driver.current_url
        self.driver.refresh()

    def skip_hell(self):
        self.driver.find_element_by_class_name("type-treasureraid-hell").click()
        self.utils.wait_and_click_element_by_class_name("btn-usual-text")
        time.sleep(2)
        self.battle_result()

    def run(self):
        self.move_to_event()
        if self.target == "box":
            self.run_treasure()
        else:
            self.run_battle()

    def run_treasure(self):
        self.pre_loop_actions()
        while self.continue_:
            try:
                self.open_treasurebox()
            except Exception:
                traceback.print_exc()
                breakpoint()

    def run_battle(self):
        self.pre_loop_actions()
        while self.continue_:
            try:
                if len(self.driver.find_elements_by_class_name("type-treasureraid-hell")):
                    self.skip_hell()
                self.process_event()
            except Exception:
                traceback.print_exc()
                breakpoint()

    def select_difficulty(self):
        raise NotImplementedError

    def pre_loop_actions(self):
        raise NotImplementedError

    # TODO: 適切な名前をつける
    def process_event(self):
        self.select_difficulty()
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()
        self.select_supporter_stone()
        self.utils.wait_and_click_element_by_class_name("btn-usual-ok")
        self.wait_until_battle_start()
        self.battle_routine()
        self.battle_result()

    def battle_routine(self):
        if self.use_debuff:
            self.debuff()
        self.auto_battle()

    def open_treasurebox(self):
        if len(self.driver.find_elements_by_class_name("btn-bulk-play")):
            self.driver.find_element_by_class_name("btn-bulk-play").click()
            time.sleep(5)
            self.driver.find_element_by_id("cjs-gacha").click()
            time.sleep(10)
            self.driver.find_element_by_id("cjs-gacha").click()
        elif len(self.driver.find_elements_by_class_name("btn-medal")) > 1:
            self.driver.find_element_by_class_name("btn-medal").click()
            time.sleep(1)
            if len(self.driver.find_elements_by_id("cjs-gacha")):
                time.sleep(4)
                self.driver.find_element_by_id("cjs-gacha").click()
                time.sleep(10)
                self.driver.find_element_by_id("cjs-gacha").click()
        else:
            if not len(self.driver.find_elements_by_class_name("btn-reset")):
                self.continue_ = False
                return
            self.driver.find_element_by_class_name("btn-reset").click()
            self.driver.find_element_by_class_name("btn-usual-ok").click()
            time.sleep(2)
            self.driver.get(self.base_url)
            self.select_difficulty()
