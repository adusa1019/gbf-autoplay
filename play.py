import argparse
import os
import traceback

import yaml
from selenium import webdriver

from battle.permanent.quest import Quest
from daily import Daily
from event.dread_barrage import DreadBarrage
from event.proving_grounds import ProvingGrounds
from event.revival_event import RevivalEvent
from event.rise_of_the_beasts import RiseOfTheBeasts
from event.showdowns import Showdowns
from event.story_event import StoryEvent
from event.unite_and_fight import UniteAndFight
from utils import Utils


def load_config(file="config.yaml"):
    with open(file, encoding="utf-8") as f:
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
    if os.name == "posix":
        driver = webdriver.Chrome("./chromedriver", desired_capabilities=options.to_capabilities())
    else:
        driver = webdriver.Chrome("./chromedriver.exe",
                                  desired_capabilities=options.to_capabilities())
    return driver


class GBF:
    tasks = {
        "daily": Daily,
        "db": DreadBarrage,
        "quest": Quest,
        "story": StoryEvent,
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
        url = "http://gbf.game.mbga.jp/#mypage"
        self.driver.get(url)
        self.get_login_bonus()
        if self.driver.current_url != url:
            self.driver.get(url)
        self.driver.refresh()

    def get_login_bonus(self):
        driver.implicitly_wait(2)
        while len(self.driver.find_elements_by_id("cjs-login")):
            self.utils.wait_and_click_element_by_id("cjs-login")

    def run(self):
        self.task.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    config = load_config(args.config)
    driver = initialize(config)

    try:
        gbf = GBF(driver, config)
        gbf.move_to_game()
        gbf.run()
    except Exception:
        traceback.print_exc()
        breakpoint()
    finally:
        driver.quit()
