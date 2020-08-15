import time
import traceback

from battle.base import Battle


class Event(Battle):

    def __init__(self, driver, config):
        super().__init__(driver, supporter=config.get("supporter", None))
        self.target = config.get("target")
        self.use_debuff = config.get("use_debuff", False)
        self.use_treasure_hunt = config.get("use_treasure_hunt", False)

    def move_to_event(self):
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
        self.pre_loop_actions()
        while True:
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
        if self.use_debuff:
            self.debuff()
        self.auto_battle()
        self.battle_result()
