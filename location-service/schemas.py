from pydantic import BaseModel


class AddressValidationRequest(BaseModel):
    address: str
    correlation_id: str


class AddressValidationResponse(BaseModel):
    correlation_id: str
    valid: bool
    address: str
    district: str
    coordinates: dict
