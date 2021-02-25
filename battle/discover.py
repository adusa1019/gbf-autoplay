import time


class Discover:

    ns = {
        "n_lv2": "ティアマグ コロマグ リヴァマグ ユグマグ シュヴァマグ セレマグ".split(),
        "n_lv3": "ナタク フラムグラス マキュラマリウス メドゥーサ アポロン オリヴィエ".split(),
        "n_lv4": "アテナ グラニ バアル ガルーダ オーディン リッチ".split(),
        "n_lv5": "グランデ プロバハ 黄龍 黒麒麟".split(),
        "n_lv6": "ミカエル ガブリエル ウリエル ラファエル".split(),
        "n_lv7": "アルバハ",
    }
    hls = {
        "hl_lv1": "ティアマグ コロマグ リヴァマグ ユグマグ シュヴァマグ セレマグ".split(),
        "hl_lv2": "ナタク フラムグラス マキュラマリウス メドゥーサ アポロン オリヴィエ ローズクイーン".split(),
        "hl_lv3": "シヴァ エウロペ ブローディア グリームニル メタトロン アバター".split(),
        "hl_lv4": "プロメテウス カーオン ギルガメッシュ バイヴカハ ヘクトル アヌビス".split(),
        "hl_lv5": "ティアマリス リヴァマリス フロネシス".split(),
        "hl_lv6": "黄龍黒麒麟 ルシN 四大天司 リンドヴルム".split(),
        "hl_lv7": "ウィルナス ワムデュス ガレヲン イーウィヤ ルオー フェディエル".split(),
        "hl_lv8": "プロバハ アーカーシャ グランデ アルバハ".split(),
        "hl_lv9": "ルシH ベルゼバブ".split(),
    }

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    # NOTE: raise error when discovers n_lv2
    def _discover(self, is_hl, difficulty, index):
        self.driver.refresh()
        time.sleep(1)
        url = "http://gbf.game.mbga.jp/?#quest/multi"
        while self.driver.current_url != url:
            self.driver.get(url)
            time.sleep(1)
        self.driver.find_elements_by_class_name("btn-stage-type")[is_hl].click()
        time.sleep(1)
        self.driver.find_elements_by_class_name("btn-stage-detail")[difficulty].click()
        time.sleep(1)
        self.driver.find_elements_by_class_name("btn-set-quest")[index].click()
        time.sleep(1)
        self.driver.find_element_by_class_name("btn-offer").click()
        time.sleep(1)
        if self.driver.find_elements_by_class_name("btn-usual-close"):
            self.driver.refresh()
            time.sleep(1)
            return False
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        time.sleep(1)
        return True

    def discover(self, name):
        is_hl, difficulty, index = self.name2position(name)
        is_discovered = self._discover(is_hl, difficulty, index)
        if len(self.driver.find_elements_by_class_name("use-item-num")):
            self.use_elixir_half()
        return is_discovered

    def name2position(self, name):
        is_hl = any(e in name for e in "hl ルシ".split())
        name = name.replace("hl", "")
        enemys = self.hls if is_hl else self.ns
        for lv, es in enemys.items():
            if name in es:
                return is_hl, int(lv[-1]) - 1, es.index(name)
        assert False

    def use_elixir_half(self, full=False):
        self.driver.find_elements_by_class_name("btn-use-full")[-1].click()
        time.sleep(1)
        self.driver.find_element_by_class_name("btn-usual-ok").click()
        time.sleep(1)
