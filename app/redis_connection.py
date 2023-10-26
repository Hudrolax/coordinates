import redis.asyncio as redis
from config import REDIS_HOST, REDIS_DB


r = redis.Redis(host=REDIS_HOST, db=REDIS_DB)
