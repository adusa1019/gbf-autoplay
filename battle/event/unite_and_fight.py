from battle.event.base import Event


class UniteAndFight(Event):

    def vh(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[1].click()
        self.driver.find_elements_by_class_name("lis-multi")[0].click()

    def ex(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[1].click()
        self.driver.find_elements_by_class_name("lis-multi")[1].click()

    def exp(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[1].click()
        self.driver.find_elements_by_class_name("lis-multi")[2].click()

    def hell_1st_stage(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()

    targets = {
        "vh": vh,
        "ex": ex,
        "exp": exp,
    }

    def select_difficulty(self):
        self.targets[self.target](self)
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()

    def pre_loop_actions(self):
        pass

    def battle_routine(self):
        self.mechanic()
        self.summon(name="ゼノ・ウォフマナフ")
        self.attack()
        self.auto_battle()
