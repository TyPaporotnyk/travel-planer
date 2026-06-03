from dataclasses import dataclass

from redis.asyncio import Redis
from httpx import AsyncClient, HTTPStatusError

CACHE_TTL = 86400


@dataclass(kw_only=True)
class PlacesClient:
    client: AsyncClient
    redis_client: Redis

    @staticmethod
    def get_cache_key(place_id) -> str:
        return f"place_valid:{place_id}"

    async def validate_place(self, place_id: str) -> bool:
        cache_key = self.get_cache_key(place_id)

        cached_result = await self.redis_client.get(cache_key)
        if cached_result is not None:
            return cached_result == "1"

        try:
            response = await self.client.get(f"places/{place_id}")
            response.raise_for_status()
        except HTTPStatusError:
            return False
        else:
            await self.redis_client.set(cache_key, "1", ex=CACHE_TTL)
            return True
