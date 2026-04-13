import httpx
from utils.logger import get_logger
from exceptions import NominatimServiceException


logger = get_logger("location")


async def validate_address(address: str) -> dict:
    logger.info("Validating address | address=%s", address)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": address,
                    "format": "json",
                    "addressdetails": 1,
                    "limit": 1,
                },
                headers={"User-Agent": "211-civic-platform/1.0"},
            )
        return response.json()
    except Exception as e:
        logger.error(" Failed to retrieve address | error=%s", str(e), exc_info=True)
        raise NominatimServiceException(str(e))
