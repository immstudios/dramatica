def top_idxs(keys, exp_ret):
    res =  keys[-exp_ret:]
    return res

def bottom_idxs(keys, exp_ret):
    res = keys[:exp_ret]
    return res

def rule_distance(dramatica, pool, exp_ret):
    keys = list(pool.keys())
    keys.sort(key=lambda x: pool[x].dr_distance)
    for key in bottom_idxs(keys, len(keys) - exp_ret):
        del (pool[key])

def rule_count(dramatica, pool, exp_ret):
    keys = list(pool.keys())
    keys.sort(key=lambda x: pool[x].dr_count)
    for key in top_idxs(keys, len(keys) - exp_ret):
        del (pool[key])

def rule_artist(dramatica, pool, exp_ret):
    keys = list(pool.keys())
    keys.sort(key=lambda x: pool[x]["role/performer"] in [item["role/performer"] for item in dramatica.parent.new_items])
    for key in top_idxs(keys, len(keys) - exp_ret):
        del (pool[key])

def rule_genre(dramatica, pool, exp_ret):
    keys = list(pool.keys())
    try:
        late_genre = dramatica.parent.new_items[-1]["genre"]
    except IndexError:
        return
    if not late_genre: # TODO: search history
        return
    keys.sort(key=lambda x: pool[x]["genre"] == late_genre)
    for key in top_idxs(keys, len(keys) - exp_ret):
        del (pool[key])

def rule_format(dramatica, pool, exp_ret):
    keys = list(pool.keys())
    try:
        late_format = dramatica.parent.new_items[-1]["editorial_format"]
    except IndexError:
        return
    if not late_format: # TODO: search history
        return
    keys.sort(key=lambda x: pool[x]["editorial_format"] == late_format)
    for key in bottom_idxs(keys, len(keys) - exp_ret):
        del (pool[key])

def rule_bpm(dramatica, pool, exp_ret):
    pass #TODO: vyrobit a pridat do processes



ruleset = [
        rule_distance,
        rule_count,
        rule_artist,
        rule_genre,
        rule_format,
    ]

