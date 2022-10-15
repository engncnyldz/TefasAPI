from .redis_host import r
from .refresh_time import get_expire_time

r.set("code", "yzc")

def check_if_exists(name):
    data = r.hgetall(name)  
    for key, value in data.items():
        data[key] = value if value != "" else None
    return data

def push_to_cache(name, mapping: dict):
    for key, value in mapping.items():
        mapping[key] = value if value is not None else ""
    r.hset(name=name, mapping=mapping)
    r.expireat(name=name, when=get_expire_time())