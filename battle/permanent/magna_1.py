import time
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from battle.base import Battle


# TODO: 適切な名前をつける
# TODO: マグナ1以外を作成するかどうか決める
class MagnaI(Battle):
    enemys = "ティアマト コロッサス リヴァイアサン ユグドラシル シュヴァリエ セレスト アドウェルサ".split()
    # TODO: 複数許容できるものをどうするか考える
    supporters = "カグヤ エウロペ ブローディア グリームニル バハムート ルシフェル".split()

    def __init__(self, driver, config):
        super().__init__(driver, supporter=config.get("supporter", None))
        self.use_debuff = config.get("use_debuff", False)
        self.use_treasure_hunt = config.get("use_treasure_hunt", False)
        self.continue_ = True
        self.base_url = "http://gbf.game.mbga.jp/#quest"

    def run(self):
        self.move_to_quest()
        while self.continue_:
            try:
                self.process_magnaI()
            except Exception:
                traceback.print_exc()
                breakpoint()

    def process_magnaI(self):
        wait(self.driver,
             30).until(ec.visibility_of_element_located((By.CLASS_NAME, "prt-list-contents")))
        ele = self.driver.find_elements_by_class_name("prt-list-contents")[1]
        quest_name = ele.get_attribute("data-quest-name").replace("討伐戦", "").split("・")
        enemy_name, is_magna = quest_name[0], quest_name[-1] == "マグナ"
        is_assault_time = self.driver.find_element_by_class_name("prt-assault-time").is_displayed()

        if enemy_name not in self.enemys:
            self.continue_ = False
            return

        if is_magna:
            self.supporter = self.supporters[self.enemys.index(enemy_name)]
        ele.click()
        wait(self.driver,
             30).until(ec.visibility_of_element_located((By.CLASS_NAME, "btn-select-pair-quest")))
        self.driver.find_elements_by_class_name("btn-select-pair-quest")[1].click()
        if is_magna:
            self.utils.wait_and_click_element_by_class_name("btn-offer")

        # TODO: 現在のスタミナと使用APから計算する
        time.sleep(1)
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()

        self.select_supporter_stone()
        self.utils.wait_and_click_element_by_class_name("btn-usual-ok")
        self.wait_until_battle_start()
        self.summon()
        if enemy_name == "シュヴァリエ":
            # TODO: 奥義OFF
            self.attack()
        self.treasure_hunt()
        if enemy_name == "シュヴァリエ":
            self.attack()
            # TODO: 奥義ON
        # TODO: 召喚石を使う
        if is_assault_time:
            if self.use_debuff and is_magna:
                self.debuff()
            self.attack()
        self.auto_battle()
        self.battle_result()

    def move_to_quest(self):
        self.utils.wait_and_click_element_by_class_name("btn-head-pop")
        self.utils.wait_and_click_element_by_class_name("btn-global-quest")
