import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from battle import Battle


class Quest(Battle):

    def __init__(self, driver, config):
        super().__init__(driver,
                         supporter=config.get("supporter", None),
                         supporter2=config.get("supporter2", None))
        self.continue_ = True
        self.target = config.get("target")

    # free quest
    def favorite_01(self):
        while self.continue_:
            self.utils.wait_and_click_element_by_class_name("btn-quest-list", 1)
            self.unit()

    # extra quest
    def angel_halo(self):
        while self.continue_:
            if len(self.driver.find_elements_by_class_name("btn-stage-detail")) == 9:
                self.utils.wait_and_click_element_by_class_name("btn-stage-detail", 1)
                self.utils.wait_and_click_element_by_class_name("btn-set-quest")
                *es, = filter(lambda x: x.text,
                              self.driver.find_elements_by_class_name("btn-supporter"))
                breakpoint()
                self.utils.wait_and_click_element_by_class_name("btn-usual-ok")
                self.wait_until_battle_start()
                self.auto_battle()
                self.battle_result()
                continue
            self.utils.wait_and_click_element_by_class_name("btn-stage-detail", 7)
            self.utils.wait_and_click_element_by_class_name("btn-set-quest", 3)
            self.unit()

    def campaign_quest(self):
        while self.continue_:
            self.utils.wait_and_click_element_by_class_name("btn-stage-detail", 1)
            self.utils.wait_and_click_element_by_class_name("btn-set-quest")
            self.unit()

    # side story
    def side_story_base(self):
        self.driver.get(self.base_url)
        while self.continue_:
            self.utils.wait_and_click_element_by_class_name("prt-button-cover", 1)
            self.unit()

    def lovelive(self):
        self.base_url = "http://gbf.game.mbga.jp/?#sidestory/story/6021"
        self.side_story_base()

    def princess_connect(self):
        self.base_url = "http://gbf.game.mbga.jp/?#sidestory/story/6023"
        self.side_story_base()

    targets = {
        "fav01": favorite_01,
        "halo": angel_halo,
        "campaign": campaign_quest,
        "lovelive": lovelive,
        "priconne": princess_connect
    }

    def run(self):
        self.move_to_quest()
        while True:
            try:
                self.targets[self.target](self)
            except Exception:
                traceback.print_exc()
                breakpoint()

    def move_to_quest(self):
        if self.target in ["fav01"]:
            self.quest_type = "free"
            self.base_url = "http://gbf.game.mbga.jp/?#quest/index/0/0/1"
        elif self.target in ["halo", "campaign"]:
            self.quest_type = "extra"
            self.base_url = "http://gbf.game.mbga.jp/#quest/extra"
        elif self.target in ["lovelive", "priconne"]:
            self.quest_type = "side"
            self.base_url = "http://gbf.game.mbga.jp/?#sidestory"
        self.driver.get(self.base_url)

    def unit(self):
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()
        self.select_supporter_stone()
        self.utils.wait_and_click_element_by_class_name("btn-usual-ok")
        if self.quest_type == "free":
            wait(self.driver, 10).until(
                ec.presence_of_element_located(
                    (By.XPATH, '//div[@class="pop-usual pop-skip-result pop-show"]')))
            self.utils.wait_and_click_element_by_class_name("btn-usual-ok", 2)
        self.utils.wait_and_click_element_by_class_name("btn-attack-start", time=120)
        self.utils.wait_and_click_element_by_class_name("btn-auto")
        wait(self.driver, 120).until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-usual-ok")))
        self.battle_result()
