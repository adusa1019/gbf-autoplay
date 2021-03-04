from non_battle import SkipHard
from non_battle.casino.cage import Cage
from non_battle.gacha.gacha import Gacha
from non_battle.shop.treasure_trade import DailyTrade


class Daily:

    def __init__(self, driver, *_):
        self.driver = driver

    def run(self):
        Cage(self.driver).run()
        Gacha(self.driver).lupi()
        DailyTrade(self.driver).run()
        SkipHard(self.driver).run()
