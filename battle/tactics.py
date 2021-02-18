def mechanic_1t_ca():
    """
    skills = None
    while not skills:
        try:
            self.utils.wait_and_click_element_by_xpath(
                '//div[@class="lis-character0 btn-command-character"]', time=30)
            skills = self.driver.find_elements_by_class_name("lis-ability")
        except ElementClickInterceptedException:
            pass
        except Exception:
            traceback.print_exc()
            breakpoint()
    # TODO: 時々発生する例外に対処する
    for i in range(4):
        for _ in range(10):
            try:
                wait(self.driver,
                     10).until(ec.element_to_be_clickable((By.CLASS_NAME, "lis-ability")))
                skills[i].click()
            except Exception:
                print(f"in click {i}")
            else:
                break
    self.driver.find_element_by_class_name("btn-command-back").click()
    """
    pass


def chrysaor_1t_ca():
    pass


def qilin_1t_ca():
    pass


"""
    def debuff(self):
        skills = None
        while not skills:
            try:
                self.utils.wait_and_click_element_by_xpath(
                    '//div[@class="lis-character0 btn-command-character"]', time=30)
                skills = self.driver.find_elements_by_class_name("lis-ability")
            except ElementClickInterceptedException:
                pass
            except Exception:
                traceback.print_exc()
                breakpoint()
        # TODO: 時々発生する例外に対処する
        for _ in range(10):
            try:
                wait(self.driver,
                     10).until(ec.element_to_be_clickable((By.CLASS_NAME, "lis-ability")))
                skills[1].click()
            except Exception:
                print("in click 1")
            else:
                break
        for _ in range(10):
            try:
                wait(self.driver,
                     10).until(ec.element_to_be_clickable((By.CLASS_NAME, "lis-ability")))
                skills[2].click()
            except Exception:
                print("in click 2")
            else:
                break
        self.driver.find_element_by_class_name("btn-command-back").click()
"""
