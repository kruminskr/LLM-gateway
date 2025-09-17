import time

from .....utiles.redis import redis_client

async def set_redis_cache (provider, latency):
    previos_data = await redis_client.hgetall(provider)
    
    EMA_ALPHA = 0.3 # Smoothing factor for EMA 

    if previos_data:
        old_avg_latency = float(previos_data.get("avg_latency"))
        avg_latency = EMA_ALPHA * latency + (1-EMA_ALPHA) * old_avg_latency

    if not previos_data:
        avg_latency = latency

    data = {
        "avg_latency": avg_latency,
        "last_latency": latency,
        "last_updated": time.time()
    }

    async with redis_client.pipeline() as pipe:
        await pipe.hset(provider, mapping=data)
        await pipe.expire(provider, 600)
        await pipe.execute()