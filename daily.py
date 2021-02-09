from battle.permanent.magna_1 import MagnaI
from non_battle.casino.cage import Cage
from non_battle.shop.journey_drops import JourneyDrops
from non_battle.shop.treasure_trade import DailyTrade


class Daily:

    def __init__(self, driver, config):
        self.driver = driver
        self.magna = MagnaI(driver, config)

    def run(self):
        Cage(self.driver).run()
        DailyTrade(self.driver).run()
        JourneyDrops(self.driver).drop_rate()
        self.magna.run()
