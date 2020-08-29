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

    def hell_1st_stage_90(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()

    def hell_2nd_stage_90(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()
        self.driver.find_elements_by_class_name("btn-multi-battle")[0].click()

    def hell_2nd_stage_95(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()
        self.driver.find_elements_by_class_name("btn-multi-battle")[1].click()

    def hell_3rd_stage_90(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()
        self.driver.find_elements_by_class_name("btn-multi-battle")[0].click()

    def hell_3rd_stage_95(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()
        self.driver.find_elements_by_class_name("btn-multi-battle")[1].click()

    def hell_3rd_stage_100(self):
        self.driver.find_elements_by_class_name("img-btn-raid")[0].click()
        self.driver.find_elements_by_class_name("btn-multi-battle")[2].click()

    targets = {
        "vh": vh,
        "ex": ex,
        "exp": exp,
        "hell_1st_90": hell_1st_stage_90,
        "hell_2nd_90": hell_2nd_stage_90,
        "hell_2nd_95": hell_2nd_stage_95,
        "hell_3rd_90": hell_3rd_stage_90,
        "hell_3rd_95": hell_3rd_stage_95,
        "hell_3rd_100": hell_3rd_stage_100
    }

    def select_difficulty(self):
        self.targets[self.target](self)
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()

    def pre_loop_actions(self):
        if "hell" in self.target:
            self.battle_routine = self._battle_routine2
        else:
            self.battle_routine = self._battle_routine1
        pass

    def _battle_routine1(self):
        self.mechanic()
        self.summon(name="ゼノ・ウォフマナフ")
        self.attack()
        self.auto_battle()

    def _battle_routine2(self):
        self.summon(name="ゼノ・ウォフマナフ")
        self.auto_battle()
