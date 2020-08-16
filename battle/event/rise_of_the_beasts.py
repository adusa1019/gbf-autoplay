from battle.event.base import Event


class RiseOfTheBeasts(Event):

    def multi(self):
        self.driver.find_element_by_class_name("img-raid-boss").click()
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()
        self.driver.find_element_by_class_name("prt-icon-bonus").find_element_by_xpath(
            "..").click()

    def maniac(self):
        pass

    targets = {
        "multi": multi,
        "maniac": maniac,
    }

    def select_difficulty(self):
        self.targets[self.target](self)

    def pre_loop_actions(self):
        pass
