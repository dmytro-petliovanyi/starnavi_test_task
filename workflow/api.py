from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from workflow.routers.edge import edge_router
from workflow.routers.node import node_router
from workflow.routers.workflow import workflow_router

app = FastAPI()

app.include_router(workflow_router)
app.include_router(node_router)
app.include_router(edge_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
