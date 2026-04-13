class AddressNotFoundException(Exception):
    def __init__(self, correlation_id: str = None):
        self.message = (
            f"Location not found | correlation_id={correlation_id}"
            if correlation_id
            else "Location not found"
        )
        super().__init__(self.message)


class NominatimServiceException(Exception):
    def __init__(self, message: str = "Nominatim service unavailable"):
        self.message = message
        super().__init__(self.message)
