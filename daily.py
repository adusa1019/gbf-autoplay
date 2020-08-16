from non_battle.casino.casino_cage import DailyCasinoCage
from battle.permanent.magna_1 import MagnaI


class Daily:

    def __init__(self, driver, config):
        self.driver = driver
        self.magna = MagnaI(driver, config)

    def run(self):
        DailyCasinoCage(self.driver).run()
        self.magna.run()
