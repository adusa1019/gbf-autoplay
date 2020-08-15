from event import Event


class Showdowns(Event):

    def choose_ex(self):
        self.find_element_with_attribute_condition_by_class_name("btn-stage-detail", "data-key",
                                                                 "1").click()
        self.find_element_with_attribute_condition_by_class_name("btn-set-quest", "data-ap",
                                                                 "30").click()

    def choose_maniac(self):
        self.find_element_with_attribute_condition_by_class_name("btn-stage-detail", "data-key",
                                                                 "1").click()
        self.find_element_with_attribute_condition_by_class_name("btn-set-quest", "data-ap",
                                                                 "50").click()

    def choose_multi(self):
        self.utils.wait_and_click_element_by_class_name("btn-multi-detail")
        self.utils.wait_and_click_element_by_class_name("btn-offer")

    def select_difficulty(self):
        exec(f"self.choose_{self.target}()")
        time.sleep(1)

    def pre_loop_actions(self):
        self.utils.wait_and_click_element_by_class_name("btn-event-extra")
        time.sleep(1)
