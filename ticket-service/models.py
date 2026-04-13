import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Text, JSON, TIMESTAMP, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class TicketPriority(PyEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class TicketStatus(PyEnum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class TicketRequest(Base):
    __tablename__ = "tickets"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    correlation_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), nullable=False, default=TicketStatus.PENDING
    )
    priority: Mapped[TicketPriority] = mapped_column(
        Enum(TicketPriority), nullable=False, default=TicketPriority.MEDIUM
    )
    assigned_team: Mapped[str] = mapped_column(String, nullable=True)
    assignee_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    internal_notes: Mapped[JSON] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    resolved_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, default=None
    )
