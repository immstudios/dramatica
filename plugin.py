from .dramatica import *


class Plugin(SolverPlugin):
    def solve(self):
        config = json.load(open("/mnt/nebula_01/.nx/dramatica.json"))
        try:
            item_config = config[self.placeholder["title"]]
        except KeyError:
            log_traceback()
            raise Exception("this item cannot be solved")
        dramatica = Dramatica(self, item_config)
        for asset in dramatica:
            meta = {
                    "id_asset" : asset.id
                }
            if asset["mark_in"]:
                meta["mark_in"] = asset["mark_in"]
            if asset["mark_out"]:
                meta["mark_out"] = asset["mark_out"]
            item = Item(meta=meta, db=self.db)
            item._asset = asset
            yield item
