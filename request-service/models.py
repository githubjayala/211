import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Text, JSON, TIMESTAMP, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class RequestStatus(PyEnum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    correlation_id: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    district: Mapped[str] = mapped_column(String, nullable=False)
    coordinates: Mapped[dict] = mapped_column(JSON, nullable=False)
    issue: Mapped[str] = mapped_column(String, nullable=False)
    contact: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus), nullable=False, default=RequestStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
