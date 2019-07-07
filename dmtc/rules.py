import statistics

#
# Utilities
#

SIMILAR = 0
DIFFERENT = 1


def get_value_list(key, assets):
    values = []
    for asset in assets:
        value = asset[key]
        if not asset[key]:
            continue
        if value in values:
            continue
        values.append(value)
    return values


def rate_similarity(pattern, values):
    result = {}
    if not pattern in values:
        values.append(pattern)
    values.sort()
    idx = values.index(pattern)
    for i, value in enumerate(values):
        result[value] = abs(idx - i)
    return result


def refine_minimum(pool, indices, count):
    for i in indices[count:]:
        del(pool[i])


def refine_maximum(pool, indices, count):
    for i in indices[:-count]:
        del(pool[i])


def refine_content(pool, target_key, target_value, count, find=SIMILAR):
    keys = list(pool.keys())
    values = get_value_list(target_key, [pool[i] for i in pool])
    if not values:
        return
    median_value = values[int(len(values)/2)]
    ratings = rate_similarity(target_value, values)
    keys.sort(key=lambda x: ratings[pool[x].get(target_key, median_value)])
    if find == SIMILAR:
        refine_minimum(pool, keys, count)
    else:
        refine_maximum(pool, keys, count)

#
# Rules
#

def rule_distance(dramatica, pool, count):
    keys = list(pool.keys())
    keys.sort(key=lambda x: pool[x].dr_distance)
    refine_maximum(pool, keys, count)

def rule_count(dramatica, pool, count):
    keys = list(pool.keys())
    keys.sort(key=lambda x: pool[x].dr_count)
    refine_minimum(pool, keys, count)

def rule_artist(dramatica, pool, count):
    keys = list(pool.keys())
    target_key = "role/performer"
    keys.sort(key=lambda x: pool[x][target_key] in [a[target_key] for a in dramatica.new_assets if a[target_key]])
    refine_minimum(pool, keys, count)

def rule_album(dramatica, pool, count):
    keys = list(pool.keys())
    target_key = "album"
    keys.sort(key=lambda x: pool[x][target_key] in [a[target_key] for a in dramatica.new_assets if a[target_key]])
    refine_minimum(pool, keys, count)

def rule_genre(dramatica, pool, count):
    target_key = "genre"
    find = SIMILAR
    target_value = dramatica.last_attribs.get(target_key, None)
    if not target_value:
        return
    refine_content(pool, target_key, target_value, count, find)
    nvals = set([pool[x][target_key] for x in pool.keys()])

def rule_format(dramatica, pool, count):
    target_key = "editorial_format"
    find = DIFFERENT
    target_value = dramatica.last_attribs.get(target_key, None)
    if not target_value:
        return
    refine_content(pool, target_key, target_value, count, find)
    nvals = set([pool[x][target_key] for x in pool.keys()])

def rule_bpm(dramatica, pool, count):
    lbpm = dramatica.last_attribs.get("audio/bpm", None)
    if not lbpm:
        return
    mbpm = dramatica.refine_cache.get("bpm_median", None)
    if not mbpm:
        mbpm = statistics.median([pool[x]["audio/bpm"] for x in pool.keys() ])
        dramatica.refine_cache["bpm_median"] = mbpm
    keys = list(pool.keys())
    if lbpm < mbpm:
        keys.sort(key=lambda x: (pool[x]["audio/bpm"] or mbpm) >= mbpm)
    else:
        keys.sort(key=lambda x: (pool[x]["audio/bpm"] or mbpm) <= mbpm)
    refine_maximum(pool, keys, count)

#
# Rule order
#

ruleset = [
        rule_count,
        rule_distance,
        rule_artist,
        rule_album,
        rule_genre,
        rule_format,
        rule_bpm,
]

