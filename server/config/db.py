import redis


def create_redis_connection_pool():
    return redis.ConnectionPool(
        host="redis", port=6379, db=0, decode_responses=True
    )


redis_pool = create_redis_connection_pool()


def get_redis():
    # Here, we re-use our connection pool, not creating a new one
    return redis.Redis.from_pool(redis_pool)
