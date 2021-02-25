import re
import time
import traceback
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait


def _supporter_info_to_int(x, effect):
    x = [t for t in x.text.replace("/", "\n").split("\n") if effect in t]
    return int(re.sub(r"\D", "", re.sub(r"最大\d+", "0", x[0])))


class Supporter:

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def _choose_element(self):
        pass

    def _choose_summon(self, effect):
        es = [
            e for e in self.driver.find_elements_by_class_name("btn-supporter") if effect in e.text
        ]
        if es:
            sorted(es, key=lambda x: _supporter_info_to_int(x, effect), reverse=True)[0].click()
            time.sleep(1)
            return True
        return False

    def choose(self, effect1, effect2=None):
        # TODO: temporary code for debuging
        if "supporter" not in self.driver.current_url:
            breakpoint()
        element = self.driver.find_element_by_class_name("selected").get_attribute("data-type")
        done = self._choose_summon(effect1)
        if effect2 and not done:
            done = self._choose_summon(effect2)
        if not done:
            es = [e for e in self.driver.find_elements_by_class_name("btn-supporter")]
            breakpoint()
        return element


class Party:

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def _choose_element(self, index):
        pass

    def _choose_party(self, index):
        pass

    def choose(self):
        pass

    def no_change(self):
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        time.sleep(1)


class Result:

    def __init__(self, driver, url):
        super().__init__()
        self.driver = driver
        self.url = url

    def skip(self):
        if self.driver.find_elements_by_class_name("btn-usual-ok"):
            self.driver.find_element_by_class_name("btn-usual-ok").click()
        self.driver.get(self.url)

    def run(self):
        self.skip()


class Battle:

    def __init__(self, driver):
        self.driver = driver
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

    def call_assist(self, check=(True, True, True)):
        wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-assist"))).click()
        wait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "pop-usual")))
        time.sleep(1)
        for e, c in zip(self.driver.find_elements_by_class_name("btn-check"), check):
            if int(e.get_attribute("active")) != int(c):
                e.click()
                time.sleep(1)
        wait(self.driver, 10).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-usual-text"))).click()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)

    def get_enemy_hp(self):
        hps = [
            int(e.text)
            for e in self.driver.find_elements_by_class_name("txt-gauge-value")[:3]
            if e.is_displayed()
        ]
        return sum(hps) / len(hps)

    def attack(self):
        wait(self.driver, 30).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "btn-attack-start"))).click()
        wait(self.driver,
             30).until(ec.invisibility_of_element_located((By.CLASS_NAME, "btn-attack-start")))
        wait(self.driver,
             30).until(ec.invisibility_of_element_located((By.CLASS_NAME, "btn-attack-cancel")))
        self.driver.refresh()

    def auto_battle(self, battle_time=120, reload=True):
        assisted = False
        while "#raid" in self.driver.current_url:
            try:
                if self.driver.find_elements_by_class_name("btn-cheer"):
                    self.driver.find_element_by_class_name("btn-cheer").click()
                    time.sleep(1)
                    self.driver.refresh()
                    time.sleep(1)
                    continue
                if self.driver.find_elements_by_class_name("prt-rematch-fail"):
                    self.driver.refresh()
                    time.sleep(1)
                    continue
                if self.driver.find_element_by_class_name(
                        "btn-revival").is_displayed() and not assisted:
                    self.call_assist()
                    assisted = True
                wait(self.driver, 10).until(ec.element_to_be_clickable(
                    (By.CLASS_NAME, "btn-auto"))).click()
                if self.get_enemy_hp() <= 50 and not assisted:
                    self.call_assist()
                    assisted = True
                wait(self.driver, battle_time).until(
                    ec.invisibility_of_element_located((By.CLASS_NAME, "btn-attack-start")))
                time.sleep(1)
                if reload:
                    self.driver.refresh()
                    self.wait_until_battle_start()
            except Exception:
                # traceback.print_exc()
                # breakpoint()
                pass

    def run(self, **kwargs):
        reload = kwargs.get("reload", True)
        self.wait_until_battle_start()
        self.auto_battle(reload=reload)
