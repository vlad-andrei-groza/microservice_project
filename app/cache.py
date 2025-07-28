import os
import redis
import json


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port)


def get_cache(key: str):
    """Get value from cache by key."""
    value = r.get(key)
    return json.loads(value) if value else None


def set_cache(key: str, value, ttl=3600):
    """Set value in cache with a key and optional TTL."""
    r.set(key, json.dumps(value), ex=ttl)
