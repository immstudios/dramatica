from nebula import *

SAFE_OVERFLOW = 40

DRAMATICA_DEFAULT_CONFIG = {
    "search_distance" : 3600 * 24 * 30,
    "block_split" : False,
    "pool_keys" : [
            "id",
            "title",
            "subtitle",    # we need subtitle and description to propagate the values to the event
            "description",
            "id_folder",
            "ctime",
            "status",
            "mark_in",
            "mark_out",
            "media_type",
            "content_type",
            "subclips",
            "promoted",
            "editorial_format",
            "genre",
            "content_alert",
            "content_alert/scheme",
            "keywords",
            "date/valid",
            "date/valid/ott",
            "runs/daily",
            "runs/weekly",
            "runs/monthly",
            "total",
            "album",
            "serie",
            "serie/season",
            "serie/episode",
            "role/director",
            "role/performer",
            "role/composer",
            "role/cast",
            "duration",
            "audio/bpm",
            "qc/state"
        ],
    "default_filters" : {
        "content_type" : VIDEO,
        "media_type" : FILE,
        "status" : ONLINE,
        "qc/state" : 4
    }
}

