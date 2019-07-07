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
            "keywords",

            "mark_in",
            "mark_out",
            "media_type",
            "content_type",
            "id_folder",
            "ctime",
            "status",
            "subclips",
            "duration",
            "qc/state",

            "promoted",
            "editorial_format",
            "genre",
            "atmosphere",
            "place",
            "intention",
            "intended_audience",
            "audio/bpm",
            "album",

            "role/director",
            "role/performer",
            "role/composer",
            "role/cast",

            "content_alert",
            "content_alert/scheme",

            "serie",
            "serie/season",
            "serie/episode",

            #TODO: use date valid, runs total and ohter values to prioritize content by rights
            "runs/daily",
            "runs/weekly",
            "runs/monthly",
            "runs/total",
            "date/valid",
            "date/valid/ott",
        ],

    "default_filters" : {
        "content_type" : VIDEO,
        "media_type" : FILE,
        "status" : ONLINE,
        "qc/state" : 4
    },

    #
    # Parental lock. Do not schedule assets of inpropriate assets between 06:00 and 22:00
    #

    "pg_start" : 22,
    "pg_end" : 6,
    "pg" : [
            "1.4", "1.5",   # AR-INCAA
            "10.4", "10.5", # CA-OFRB
            "12.6",         # CA-CBSC-CCNR-English and third-languages
            "14.6",
            "15.3", "15.4", "15.5",
            "16.1.2",
            "17.5", "17.6",
            "21.3",         # Denmark radio
            "53.1.4",       # CZECH
        ]
}

