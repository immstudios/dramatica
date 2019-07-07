"""

Main
    Primary block content

    block_split
        When selected, block is splitted after the first asset from primary pool is
        inserted.

    update_event_meta
        When block_split mode is active, this option updates parent event metadata
        (title, description and so on) using the inserted asset.

Jingles
    Appear anywhere within the block when "span" time is reached

Fill
    Used to fill empty space at the end of the block


"""

import copy
import random

from .common import *
from .pool import *


class Dramatica():
    def __init__(self, parent, settings):
        self.settings = copy.copy(DRAMATICA_DEFAULT_CONFIG)
        self.parent = parent
        try:
            nconfig = config
        except:
            nconfig = {}

        for key in nconfig:
            if key.startswith("dramatica_"):
                nkey = key.replace("dramatica_", "", 1)
                self[nkey] = nconfig[key]
        for key in settings:
            if type(settings[key]) != dict or key not in self.settings:
                self.settings[key] = settings[key]
            else:
                self.settings[key].update(settings[key])

        logging.info("Initializing Dramatica for {}".format(self.parent.placeholder))

        self.last_attribs = {}
        self.new_assets = []

        self.position = 0
        self.last_jingle = 0
        self.most_common_vals = {}
        self.refine_cache = {}

        self.main_pools = []
        self.jingle_pools = []
        self.fill_pools = []


        for i, pool in enumerate(self.get("pools", [])):
            self.main_pools.append(DramaticaPool(
                    self,
                    pool.get("filters", {}),
                    weight=pool.get("weight", 1)
                ))

        jingles = self.get("jingles")
        if jingles:
            for i, pool in enumerate(jingles.get("pools", [])):
                self.jingle_pools.append(DramaticaPool(
                        self,
                        pool.get("filters", {}),
                        weight=pool.get("weight", 1),
                        reuse=True,
                    ))

        fill = self.get("fill")
        if fill:
            for i, pool in enumerate(fill.get("pools", [])):
                self.fill_pools.append(DramaticaPool(
                        self,
                        pool.get("filters", {}),
                        weight=pool.get("weight", 1),
                        reuse=False,
                    ))

    @property
    def target_duration(self):
        return min(self.parent.placeholder.duration, self.parent.needed_duration)

    @property
    def current_duration(self):
        return self.parent.current_duration

    @property
    def db(self):
        return self.parent.db

    def get_most_common(self, key):
        if not key in self.most_common_vals:
            values = [item.asset[key] for item in self.parent.new_items if item.asset[key]]
            if not values:
                self.most_common_vals[key] =  False
            self.most_common_vals[key] =  max(values, key=values.count)
        return self.most_common_vals[key]


    def __setitem__(self, key, value):
        self.settings["key"] = value

    def __getitem__(self, key):
        return self.settings.get(key)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def __iter__(self):
        return self

    def __next__(self):
        asset = self.refine()
        self.new_assets.append(asset)
        return asset

    def refine(self):

        self.most_common_vals = {}
        self.refine_cache = {}

        if self.current_duration > self.target_duration:
            logging.info("Iterator stopped with duration {}".format(s2tc(self.parent.current_duration)))
            raise StopIteration

        #
        # Jingles
        #

        jingle_pool_ids = []
        for i, pool in enumerate(self.jingle_pools):
            if pool.pool:
                jingle_pool_ids.extend([i]* pool.weight)

        if jingle_pool_ids:
            if self.position - self.last_jingle > self.get("jingles", {}).get("distance", 800):
                current_pool_id = random.choice(jingle_pool_ids)
                pool = self.jingle_pools[current_pool_id]
                asset = pool.refine()
                if asset:
                    for j in jingle_pool_ids:
                        if current_pool_id == j:
                            continue
                        self.jingle_pools[j].mark_used(asset.id)
                    self.position += asset.duration
                    self.last_jingle = self.position
                    return asset

        #
        # Main
        #

        main_pool_ids = []
        for i, pool in enumerate(self.main_pools):
            main_pool_ids.extend([i]* pool.weight)

        asset = None
        if main_pool_ids:
            current_pool_id = random.choice(main_pool_ids)
            asset = self.main_pools[current_pool_id].refine()
            if asset:

                for j in main_pool_ids:
                    if current_pool_id == j:
                        continue
                    self.main_pools[j].mark_used(asset.id)

                self.position += asset.duration

                if self["block_split"]:
                    if self.get("update_event_meta", True):
                        for key in asset.meta.keys():
                            if key in ["title", "subtitle", "description"]:
                                value = asset[key]
                                if value:
                                    self.parent.event[key] = value
                        self.parent.event["id_asset"] = asset.id
                        self.parent.event.save()

                    split_position = self.parent.event["start"] + self.position
                    split_position += 300
                    split_position -= split_position % 300

                    self.parent.block_split(split_position)
                    self.main_pools = []

                return asset


        fill_pool_ids = []
        for i, pool in enumerate(self.fill_pools):
            fill_pool_ids.extend([i]* pool.weight)

        if fill_pool_ids:
            current_pool_id = random.choice(fill_pool_ids)
            pool = self.fill_pools[current_pool_id]
            asset = pool.refine()
            if asset:
                for j in fill_pool_ids:
                    if current_pool_id == j:
                        continue
                    self.fill_pools[j].mark_used(asset.id)
                self.position += asset.duration
                return asset

        raise StopIteration
