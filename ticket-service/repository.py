import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from models import TicketRequest
from utils.logger import get_logger
from exceptions import TicketNotFoundException, DuplicateCorrelationIdException
from utils.exceptions import (
    DatabaseInsertException,
    DatabaseUpdateException,
    DatabaseOperationException,
)

logger = get_logger("ticket-service")


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_ticket(self, payload) -> TicketRequest:
        """Insert a new ticket request."""
        # unify naming to match DB field
        cid = payload.correlation_id

        existing = (
            self.session.query(TicketRequest).filter_by(correlation_id=cid).first()
        )
        if existing:
            logger.warning("Duplicate request | correlation_id=%s", cid)
            raise DuplicateCorrelationIdException(correlation_id=cid)

        logger.info("Creating Ticket request | correlation_id=%s", cid)
        ticket_request = TicketRequest(id=uuid.uuid4(), **payload.dict())

        try:
            self.session.add(ticket_request)
            self.session.commit()
            logger.info("Ticket created | correlation_id=%s", cid)
            return ticket_request
        except (IntegrityError, OperationalError) as e:
            self.session.rollback()
            logger.error(
                "DB insertion failed | correlation_id=%s | error=%s",
                cid,
                str(e),
                exc_info=True,
            )
            raise DatabaseInsertException(str(e))
        except Exception as e:
            self.session.rollback()
            logger.error(
                "Unexpected error during creation | error=%s", str(e), exc_info=True
            )
            raise

    def get_by_correlation_id(self, correlation_id: str) -> TicketRequest | None:
        """Retrieve a single request by correlation ID."""
        try:
            ticket_request = (
                self.session.query(TicketRequest)
                .filter(TicketRequest.correlation_id == correlation_id)
                .one_or_none()
            )

            if not ticket_request:
                logger.warning("Ticket not found | correlation_id=%s", correlation_id)
                return None

            logger.info("Ticket retrieved | correlation_id=%s", correlation_id)
            return ticket_request

        except Exception as e:
            logger.error(
                "Query failed | correlation_id=%s | error=%s",
                correlation_id,
                str(e),
                exc_info=True,
            )
            raise DatabaseOperationException(str(e))

    def get_all(self) -> list[TicketRequest]:
        """Retrieve all ticket request."""
        try:
            tickets = self.session.query(TicketRequest).all()
            logger.info("Retrieved all tickets | count=%d", len(tickets))
            return tickets
        except Exception as e:
            logger.error("Query all failed | error=%s", str(e), exc_info=True)
            raise DatabaseOperationException(str(e))

    def update_status(self, correlation_id: str, status: str) -> TicketRequest:
        """Update status for a specific correlation ID."""
        try:
            ticket_request = (
                self.session.query(TicketRequest)
                .filter(TicketRequest.correlation_id == correlation_id)
                .first()
            )

            if not ticket_request:
                logger.warning(
                    "Update failed: not found | correlation_id=%s", correlation_id
                )
                raise TicketNotFoundException(correlation_id=correlation_id)

            ticket_request.status = status
            if status == "resolved":
                ticket_request.resolved_at = datetime.utcnow()

            self.session.commit()
            logger.info(
                "Status updated | correlation_id=%s | status=%s", correlation_id, status
            )
            return ticket_request

        except (IntegrityError, OperationalError) as e:
            self.session.rollback()
            logger.error(
                "DB update failed | correlation_id=%s | error=%s",
                correlation_id,
                str(e),
                exc_info=True,
            )
            raise DatabaseUpdateException(str(e))
        except Exception as e:
            self.session.rollback()
            logger.error(
                "Unexpected update error | correlation_id=%s | error=%s",
                correlation_id,
                str(e),
                exc_info=True,
            )
            raise
