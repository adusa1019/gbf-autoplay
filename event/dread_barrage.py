from event.base import Event


class DreadBarrage(Event):

    def battle_routine(self):
        self.call_assist()
        self.auto_battle()

    def select_difficulty(self):
        for e in self.driver.find_elements_by_class_name("btn-start-quest")[::-1]:
            if e.is_displayed():
                e.click()
                return

    def pre_loop_actions(self):
        pass
