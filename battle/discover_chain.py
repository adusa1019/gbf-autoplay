from non_battle.shop.journey_drops import JourneyDrops

from battle.battle import Battle, Party, Result, Supporter
from battle.discover import Discover


class DiscoverChain:

    def __init__(self, driver, config):
        super().__init__()
        self.drop = JourneyDrops(driver)
        self.discover = Discover(driver)
        self.supporter = Supporter(driver)
        self.party = Party(driver)
        self.battle = Battle(driver)
        self.result = Result(driver, "http://gbf.game.mbga.jp/?#quest")
        self.enemies = config.get("enemies", [])
        self.supporter1 = config.get("supporter", None)
        self.supporter2 = config.get("supporter2", None)

    def _run(self, name):
        while True:
            is_discovered = self.discover.discover(name)
            if not is_discovered:
                break
            self.supporter.choose(self.supporter1, self.supporter2)
            self.party.no_change()
            self.battle.run()
            self.result.skip()

    def run(self):
        self.drop.drop_rate(1)
        for name in self.enemies:
            self._run(name)
