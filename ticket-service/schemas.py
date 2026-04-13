from pydantic import BaseModel
from datetime import datetime


class TicketCreate(BaseModel):
    correlation_id: str
    district: str
    assigned_team: str | None = None
    assignee_id: str | None = None
    priority: str


class TicketResponse(BaseModel):
    correlation_id: str
    status: str
    priority: str


class TicketDetail(BaseModel):
    correlation_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
