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
    keys.sort(key=lambda x: pool[x]["role/performer"] in [item["role/performer"] for item in dramatica.parent.new_items])
    refine_minimum(pool, keys, count)

def rule_genre(dramatica, pool, count):
    target_key = "genre"
    target_value = "3.6.4.14"
    find = DIFFERENT
    refine_content(pool, target_key, target_value, count, find)

def rule_format(dramatica, pool, count):
    target_key = "genre"
    target_value = "3.6.4.14"
    find = SIMILAR
    refine_content(pool, target_key, target_value, count, find)

def rule_bpm(dramatica, pool, count):
    pass #TODO: vyrobit a pridat do processes

#
# Rule order
#

ruleset = [
        rule_distance,
        rule_count,
        rule_artist,
        rule_genre,
        rule_format,
    ]

