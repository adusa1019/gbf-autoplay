import re
import time
import traceback
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait as wait
from utils import Utils


def _supporter_info_to_int(x, supporter):
    x = [t for t in x.text.replace("/", "\n").split("\n") if supporter in t]
    return int(re.sub(r"\D", "", re.sub(r"最大\d+", "0", x[0])))


class Battle:

    def __init__(self, driver, supporter=None, supporter2=None):
        self.driver = driver
        self.supporter = supporter
        self.supporter2 = supporter2
        self.utils = Utils(driver)
        self.continue_ = True

    def wait_until_battle_start(self):
        wait(self.driver,
             30).until(ec.visibility_of_element_located((By.CLASS_NAME, "prt-black-bg")))
        wait(self.driver,
             30).until(ec.invisibility_of_element_located((By.CLASS_NAME, "prt-black-bg")))
        try:
            wait(self.driver,
                 30).until(ec.visibility_of_element_located((By.CLASS_NAME, "active-mask")))
            wait(self.driver,
                 30).until(ec.invisibility_of_element_located((By.CLASS_NAME, "active-mask")))
        except TimeoutException:
            pass
        except Exception:
            traceback.print_exc()
            breakpoint()

    def use_elixir_half(self, full=False):
        if full:
            # TODO
            pass
        wait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "pop-usual")))
        wait(self.driver, 10).until(
            ec.element_to_be_clickable(
                (By.XPATH, '//div[@class="btn-use-full index-1"]'))).click()
        self.utils.wait_and_click_element_by_class_name("btn-usual-ok")

    def select_supporter_stone(self, loop_count=10):
        if "supporter" not in self.driver.current_url:
            return
        for _ in range(loop_count):
            try:
                base = [
                    e for e in self.driver.find_elements_by_class_name("btn-supporter") if e.text
                ]
                if self.supporter:
                    *es, = filter(lambda x: self.supporter in x.text, base)
                    es.sort(key=lambda x: _supporter_info_to_int(x, self.supporter), reverse=True)
                if not es and self.supporter2:
                    *es, = filter(lambda x: self.supporter2 in x.text, base)
                    es.sort(key=lambda x: _supporter_info_to_int(x, self.supporter2), reverse=True)
                if es:
                    es[0].click()
                    return
            except Exception:
                traceback.print_exc()
                breakpoint()
        else:
            *es, = filter(lambda x: x.text,
                          self.driver.find_elements_by_class_name("btn-supporter"))
            breakpoint()

    def call_assist(self):
        wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-assist"))).click()
        wait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "pop-usual")))
        time.sleep(1)
        wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-usual-text"))).click()
        time.sleep(1)
        wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-usual-ok"))).click()

    def attack(self):
        wait(self.driver, 30).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-attack-start"))).click()
        wait(self.driver,
             30).until(ec.invisibility_of_element_located((By.CLASS_NAME, "btn-attack-start")))
        wait(self.driver,
             30).until(ec.invisibility_of_element_located((By.CLASS_NAME, "btn-attack-cancel")))
        self.driver.refresh()

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

    def treasure_hunt(self):
        skills = None
        while not skills:
            try:
                self.utils.wait_and_click_element_by_xpath(
                    '//div[@class="lis-character0 btn-command-character"]')
                skills = self.driver.find_elements_by_class_name("lis-ability")
            except Exception:
                pass
        wait(self.driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "lis-ability")))
        skills[3].click()
        self.driver.find_element_by_class_name("btn-command-back").click()

    def mechanic(self):
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

    # TODO: ElementNotInteractable に対応する
    def summon(self, index=-1, name=None, loop_count=10):
        self.driver.find_element_by_class_name("summon-on").click()
        for _ in range(loop_count):
            try:
                es = self.driver.find_elements_by_class_name("lis-summon")
                if name:
                    # NOTE: アニメーションが終わるまで待機
                    time.sleep(1)
                    es = [e for e in es if e.get_attribute("summon-name") == name][0]
                else:
                    es = es[index]
                if es:
                    break
            except Exception:
                traceback.print_exc()
                breakpoint()
        else:
            *es, = filter(lambda x: x.text, self.driver.find_elements_by_class_name("lis-summon"))
            breakpoint()
        es.click()
        self.driver.find_element_by_class_name("btn-summon-use").click()
        try:
            self.driver.find_element_by_class_name("btn-command-back").click()
        except ElementNotInteractableException:
            pass
            # traceback.print_exc()
            # breakpoint()

    def auto_battle(self, battle_time=60):
        while len(self.driver.find_elements_by_class_name("btn-usual-ok")) != 1:
            if self.driver.current_url == self.base_url:
                break
            try:
                self.utils.wait_and_click_element_by_class_name("btn-auto", time=60)
                wait(self.driver, battle_time).until(
                    ec.invisibility_of_element_located((By.CLASS_NAME, "btn-attack-start")))
                time.sleep(1)
                self.driver.refresh()
            except Exception:
                pass

    def battle_result(self):
        if self.driver.current_url == self.base_url:
            return
        self.driver.find_element_by_class_name("btn-usual-ok")
        self.driver.get(self.base_url)
