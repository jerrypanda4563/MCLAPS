import redis
from app import settings

cache=redis.Redis.from_url(settings.REDIS_URI, db = 0)

def cache_connection_test() -> bool:
    try:
        cache.set("testkey","testValue")
        value=cache.get("testKey")
        print(f'Redis connection successful {value}')
        return True
    except Exception as e:
        print(f'Cache connection test failed {e}')
        return False





