import copy

from .common import *
from .rules import *

class DramaticaPool():
    def __init__(self, parent, filters, **kwargs):
        """

        reuse (False)

        """
        self.config = kwargs
        self.parent = parent
        self.reuse = kwargs.get("reuse", False)
        self.weight = kwargs.get("weight", 1)
        self.pool = {}
        self.take_id = 0
        self.used_assets = [item["id_asset"] for item in self.parent.parent.event.bin.items if item["id_asset"]]

        # Asset conditions based on filters
        conds_list = []
        for key in filters:
            if type(filters[key]) == list:
                opts = ["'{}'".format(opt) for opt in filters[key]]
                conds_list.append("a.meta->>'{}' IN ({})".format(key, ",".join(opts)))
            elif type(filters[key]) == str and filters[key].split(" ")[0].lower() in ["=", "like", "~"]:
                conds_list.append("a.meta->>'{}' {}".format(key, str(filters[key])))
            else:
                conds_list.append("a.meta->>'{}' = '{}'".format(key, str(filters[key])))
        asset_conds = " AND ".join(conds_list)


        # Pool query construction

        db = DB()
        query = "SELECT a.meta FROM assets AS a WHERE {}".format(asset_conds)
        logging.debug(query)
        db.query(query)

        tdur = parent.target_duration - parent.current_duration
        for meta, in db.fetchall():
            id_asset = meta["id"]
            if not self.reuse:
                if id_asset in self.used_assets:
                    continue
            for key in list(meta.keys()):
                if not key in self.parent["pool_keys"]:
                    del(meta[key])
            asset = Asset(meta=meta)
            if asset.duration > tdur:
                continue

            asset.dr_distance = self.parent["search_distance"]
            asset.dr_count = 0
            self.pool[asset.id] = asset


        # Find schedule count and distance from now

        db.query("""
            SELECT i.id_asset, ABS(e.start - %s)
                FROM
                    items AS i,
                    events AS e
                WHERE
                    e.id_channel = %s
                AND e.start >= %s
                AND e.start < %s
                AND e.id_magic = i.id_bin
                AND i.id_asset > 0

                ORDER BY
                    ABS(e.start - %s) ASC
        """, [
                self.parent.parent.event["start"],
                self.parent.parent.event["id_channel"],
                self.parent.parent.event["start"] - self.parent["search_distance"],
                self.parent.parent.event["start"] + self.parent["search_distance"],
                self.parent.parent.event["start"]
            ])

        for id_asset, distance in db.fetchall():
            if not id_asset in self.pool:
                continue
            asset = self.pool[id_asset]
            asset.dr_distance = min(asset.dr_distance, distance)
            asset.dr_count += 1

    def __getitem__(self, key):
        return self.pool[key]


    def best_fit(self, duration):
        pool = copy.deepcopy(self.pool)
        keys = list(pool.keys())
        keys.sort(key=lambda x: abs(pool[x].duration - duration))
        asset = pool[keys[0]]
        return asset




    def refine(self):
        self.take_id += 1

        pool = {}
        tdur = self.parent.target_duration - self.parent.current_duration
        for key in self.pool:
            if self.pool[key].duration > tdur + SAFE_OVERFLOW:
                continue
            pool[key] = copy.copy(self.pool[key])

        while True:
            for rule in ruleset:
                keys = list(pool.keys())
                exp_ret = len(keys)
                if exp_ret > 1000:
                    exp_ret *= 1/2
                elif exp_ret > 50:
                    exp_ret *= (3/4)
                else:
                    exp_ret -= 1
                exp_ret = int(exp_ret)

                rule(self.parent, pool, exp_ret)

                if len(pool) < 2:
                    break
            if len(pool) < 2:
                break

        try:
            id_asset = list(pool.keys())[0]
        except IndexError:
            return False

        asset = self.pool[id_asset]

        logging.debug("Refined {}. DST:{} CNT:{}".format(asset, asset.dr_distance, asset.dr_count))

        self.mark_used(id_asset)
        return asset


    def mark_used(self, id_asset):
        if not id_asset in self.pool:
            return
        if self.reuse:
            self.pool[id_asset].dr_distance = - self.take_id
            self.pool[id_asset].dr_count += 1
        else:
            del(self.pool[id_asset])

