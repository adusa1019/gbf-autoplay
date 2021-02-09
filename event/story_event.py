from event.base import Event


class StoryEvent(Event):

    def choose_vh(self):
        self.driver.find_element_by_class_name("btn-quest-start").click()

    def choose_ex(self):
        self.driver.find_elements_by_class_name("btn-quest-start")[1].click()

    def choose_hl(self):
        self.driver.find_elements_by_class_name("btn-quest-start")[1].click()

    def choose_box(self):
        if self.base_url.endswith("end"):
            pass

    def select_difficulty(self):
        if self.target != "box":
            self.utils.wait_and_click_element_by_class_name("img-raid-boss")
        exec(f"self.choose_{self.target}()")
        # self.driver.find_elements_by_class_name("btn-quest-start")[1].click()

    def pre_loop_actions(self):
        pass
