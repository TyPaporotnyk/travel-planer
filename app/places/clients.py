from dataclasses import dataclass

from httpx import AsyncClient, HTTPStatusError


@dataclass(kw_only=True)
class PlacesClient:
    client: AsyncClient

    async def validate_place(self, place_id: str) -> bool:
        try:
            response = await self.client.get(f"places/{place_id}")
            response.raise_for_status()
        except HTTPStatusError:
            return False
        else:
            return True
