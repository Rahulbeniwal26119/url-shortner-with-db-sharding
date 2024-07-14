import os
from hashlib import md5

from uhashring import HashRing

import constants

PG_SHARD1_HOST = os.getenv('PG_SHARD1_HOST')
PG_SHARD2_HOST = os.getenv('PG_SHARD2_HOST')
PG_SHARD3_HOST = os.getenv('PG_SHARD3_HOST')
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'password')
PG_DATABASE = os.getenv('PG_DATABASE', 'postgres')


def hash_url(url):
    return md5(url.encode("utf-8")).hexdigest()


def get_url_id(url_digest):
    return url_digest[:10]


def get_db_configs():
    return {
        "pgshard1": {
            "user": PG_USER,
            "password": PG_PASSWORD,
            "host": PG_SHARD1_HOST,
            "port": "5432",
            "database": PG_DATABASE,
        },
        "pgshard2": {
            "user": PG_USER,
            "password": PG_PASSWORD,
            "host": PG_SHARD2_HOST,
            "port": "5432",
            "database": PG_DATABASE,
        },
        "pgshard3": {
            "user": PG_USER,
            "password": PG_PASSWORD,
            "host": PG_SHARD3_HOST,
            "port": "5432",
            "database": PG_DATABASE,
        },
}


def get_consistent_hash_obj():
    servers = [constants.PG_SHARD1, constants.PG_SHARD2, constants.PG_SHARD3]
    return HashRing(nodes=servers)