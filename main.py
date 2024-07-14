from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel

import constants
from utils import get_consistent_hash_obj, get_db_configs, get_url_id, hash_url


class Url(BaseModel):
    url: str


class UrlResponse(BaseModel):
    shard: str
    url_id: str
    url: str


db_configs = get_db_configs()
servers = get_consistent_hash_obj()

# postgresql connection pool
pool1 = None
pool2 = None
pool3 = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool1
    global pool2
    global pool3

    pool1 = await asyncpg.create_pool(
        **db_configs["pgshard1"],
    )
    pool2 = await asyncpg.create_pool(
        **db_configs["pgshard2"],
    )
    pool3 = await asyncpg.create_pool(
        **db_configs["pgshard3"],
    )

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/url/{url_id}")
async def get_url(url_id: str):
    shard = servers.get_node(url_id)

    pools = {
        constants.PG_SHARD1: pool1,
        constants.PG_SHARD2: pool2,
        constants.PG_SHARD3: pool3
    }

    pool = pools.get(shard, pool3)
    async with pool.acquire() as connection:
        async with connection.transaction():
            response = await connection.fetchrow(
                "SELECT * FROM url_table WHERE url_id = $1", url_id
            )
            response_dict = dict(response or {})
            if response_dict:
                return UrlResponse(
                    shard=shard,
                    url_id=response_dict["url_id"],
                    url=response_dict["url"],
                )
            else:
                return {"error": "Url not exists"}


@app.post("/url")
async def create_url(url: Url):
    url = url.url
    url_hash = hash_url(url)
    url_id = get_url_id(url_hash)

    shard = servers.get_node(url_id)
    pools = {
        constants.PG_SHARD1: pool1,
        constants.PG_SHARD2: pool2,
        constants.PG_SHARD3: pool3
    }

    pool = pools.get(shard, pool3)

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                "INSERT INTO url_table (url_id, url) VALUES ($1, $2)", url_id, url
            )
            return UrlResponse(
                shard=shard,
                url_id=url_id,
                url=url,
            )
