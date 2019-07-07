from nebula import *
from dmtc import Dramatica

class Plugin(SolverPlugin):
    def solve(self):
        config_path = config.get(
                    "dramatica_config_path",
                    os.path.join(storages[1].local_path, ".nx", "dramatica.json")
                )
        try:
            dramatica_config = json.load(open(config_path))
        except Exception:
            log_traceback()
            raise Exception("Unable to open Dramatica configuration file")
        try:
            item_config = dramatica_config[self.placeholder["title"]]
        except KeyError:
            log_traceback()
            raise Exception("This item cannot be solved")
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
