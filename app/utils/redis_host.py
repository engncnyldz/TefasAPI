import redis
from ..config import settings

r = redis.Redis(
    host= settings.redis_hostname,
    port= settings.redis_port,
    charset="utf-8",
    decode_responses=True
)