import argparse
import time
import traceback

import yaml
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait

from permanent import MagnaI
from proving_grounds import ProvingGrounds
from revival_event import RevivalEvent
from rise_of_the_beasts import RiseOfTheBeasts
from showdowns import Showdowns
from quest import Quest
from story_event import StoryEvent
from unite_and_fight import UniteAndFight
from utils import Utils


def load_config(file="config.yaml"):
    with open(file) as f:
        return yaml.safe_load(f)


def initialize(config):
    mobile = {"deviceName": "iPad Pro"}
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir=./data/{config['account']}")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("--window-size=1800,1800")
    options.add_argument("--force-device-scale-factor=0.7")
    options.add_argument("--high-dpi-support=0.5")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    options.add_experimental_option("mobileEmulation", mobile)
    driver = webdriver.Chrome("./chromedriver.exe", desired_capabilities=options.to_capabilities())
    driver.implicitly_wait(10)
    return driver


class GBF:
    tasks = {
        "daily": MagnaI,
        "quest": Quest,
        "ストイベ": StoryEvent,
        "復刻": RevivalEvent,
        "撃滅戦": Showdowns,
        "四象降臨": RiseOfTheBeasts,
        "ブレグラ": ProvingGrounds,
        "古戦場": UniteAndFight
    }

    def __init__(self, driver, config):
        self.driver = driver
        self.task = self.tasks[config["task_name"]](driver, config)
        self.utils = Utils(driver)

    def move_to_game(self):
        self.driver.get("http://gbf.game.mbga.jp/#mypage")
        self.get_login_bonus()
        self.driver.refresh()

    def get_login_bonus(self):
        driver.implicitly_wait(2)
        while len(self.driver.find_elements_by_id("cjs-login")):
            self.utils.wait_and_click_element_by_id("cjs-login")

    def run(self):
        self.task.run()

    # TODO: rewrite
    def daily_treasure_trade(self):
        self.utils.wait_and_click_element_by_class_name("btn-head-pop")
        self.utils.wait_and_click_element_by_class_name("txt-global-shop")
        self.utils.wait_and_click_element_by_class_name("btn-treasure-shop")
        self.utils.wait_and_click_element_by_class_name("btn-switch-treasure")
        Select(
            wait(self.driver, 10).until(
                ec.visibility_of_element_located(
                    (By.CLASS_NAME, "frm-list-select-treasure")))).select_by_value("5")
        es = wait(self.driver,
                  10).until(ec.visibility_of_all_elements_located((By.CLASS_NAME, "btn-exchange")))
        if len(es) < 6:
            return
        for i in range(2):
            es = wait(self.driver, 10).until(
                ec.visibility_of_all_elements_located((By.CLASS_NAME, "btn-exchange")))
            es[i + 2].click()
            s = Select(
                wait(self.driver,
                     10).until(ec.visibility_of_element_located((By.CLASS_NAME, "num-set"))))
            s.select_by_value(s.options[-1].text)
            self.utils.wait_and_click_element_by_class_name("btn-usual-text")
            self.utils.wait_and_click_element_by_class_name("btn-usual-ok")

    def boost_item_drop_rate(self):
        while self.driver.current_url != "http://gbf.game.mbga.jp/#shop/exchange/trajectory":
            self.driver.get("http://gbf.game.mbga.jp/#shop/exchange/trajectory")
        while True:
            try:
                es = self.driver.find_elements_by_class_name("btn-use-support")
                if es[-1].find_element_by_xpath("..").text.split()[0] != 'アイテムドロップ率UP':
                    return
                es[-1].click()
            except IndexError:
                continue
            except Exception:
                traceback.print_exc()
                breakpoint()
            else:
                break
        self.driver.find_elements_by_class_name("btn-level")[-1].click()
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        self.driver.refresh()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    config = load_config(args.config)
    driver = initialize(config)

    try:
        gbf = GBF(driver, config)
        gbf.move_to_game()
        if config["task_name"] == "daily":
            gbf.daily_casino_cage()
            # gbf.daily_treasure_trade()
        gbf.boost_item_drop_rate()
        gbf.run()
    except Exception:
        traceback.print_exc()
        breakpoint()
    finally:
        driver.quit()
