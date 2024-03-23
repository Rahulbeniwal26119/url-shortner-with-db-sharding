from hashlib import md5

from uhashring import HashRing

import constants


def hash_url(url):
    return md5(url.encode("utf-8")).hexdigest()


def get_url_id(url_digest):
    return url_digest[:10]


def get_db_configs():
    return {
        constants.PG_SHARD1: {
            "user": "postgres",
            "password": "password",
            "host": "172.17.0.4", # docker container ip can be found by running `docker inspect <container_id>`
            "port": "5432",
            "database": "postgres",
        },
        constants.PG_SHARD2: {
            "user": "postgres",
            "password": "password",
            "host": "172.17.0.5", # docker container ip can be found by running `docker inspect <container_id>`
            "port": "5432",
            "database": "postgres",
        },
        constants.PG_SHARD3: {
            "user": "postgres",
            "password": "password",
            "host": "172.17.0.6", # docker container ip can be found by running `docker inspect <container_id>`
            "port": "5432",
            "database": "postgres",
        },
    }


def get_consistent_hash_obj():
    servers = [constants.PG_SHARD1, constants.PG_SHARD2, constants.PG_SHARD3]
    return HashRing(nodes=servers)