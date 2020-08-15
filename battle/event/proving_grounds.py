import time

from battle.event.base import Event


class ProvingGrounds(Event):

    def choose_exp(self):
        self.utils.wait_and_click_element_by_class_name("btn-set-sequence", 3)
        self.utils.wait_and_click_element_by_class_name("btn-usual-ok")

    def select_difficulty(self):
        self.utils.wait_and_click_element_by_class_name("btn-sequence-banner")
        exec(f"self.choose_{self.target}()")
        time.sleep(1)

    def pre_loop_actions(self):
        pass

    def process_event(self):
        self.select_difficulty()
        self.select_supporter_stone()
        time.sleep(1)
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()
            time.sleep(1)
        self.utils.wait_and_click_element_by_class_name("btn-usual-ok")
        for _ in range(2):
            self.utils.wait_and_click_element_by_class_name("btn-start-quest")
            self.wait_until_battle_start()
            if self.use_debuff:
                self.debuff()
            self.auto_battle(600)
            self.battle_result()
        self.utils.wait_and_click_element_by_id("canv-sequence-reward")
        self.utils.wait_and_click_element_by_class_name("btn-location-top")
