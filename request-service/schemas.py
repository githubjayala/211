from pydantic import BaseModel
from datetime import datetime


class ServiceRequestCreate(BaseModel):
    correlation_id: str
    user_id: str
    full_name: str
    address: str
    district: str
    coordinates: dict
    issue: str
    contact: str


class ServiceRequestResponse(BaseModel):
    correlation_id: str
    status: str


class ServiceRequestDetail(BaseModel):
    correlation_id: str
    issue: str
    address: str
    status: str
    created_at: datetime
    updated_at: datetime
