from event import Event


class RevivalEvent(Event):

    def choose_ex(self):
        self.utils.wait_and_click_element_by_class_name("btn-stage-detail")
        self.find_element_with_attribute_condition_by_class_name("btn-set-quest", "data-ap",
                                                                 "30").click()

    def choose_maniac(self):
        self.utils.wait_and_click_element_by_class_name("btn-stage-detail")
        self.find_element_with_attribute_condition_by_class_name("btn-set-quest", "data-ap",
                                                                 "50").click()

    def choose_multi(self):
        self.utils.wait_and_click_element_by_xpath('//div[@class="btn-stage-detail solo-multi"]')
        self.find_element_with_attribute_condition_by_class_name("btn-set-quest", "data-ap",
                                                                 "30").click()

    def select_difficulty(self):
        exec(f"self.choose_{self.target}()")
        time.sleep(1)

    def pre_loop_actions(self):
        self.utils.wait_and_click_element_by_id("tab-event-extra")
        time.sleep(1)
