import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from models import ServiceRequest
from utils.logger import get_logger
from exceptions import RequestNotFoundException, DuplicateCorrelationIdException
from utils.exceptions import (
    DatabaseInsertException,
    DatabaseUpdateException,
    DatabaseOperationException,
)

logger = get_logger("request-service")


class RequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_request(self, payload) -> ServiceRequest:
        """Insert a new service request."""
        # Unify naming: using 'correlation_id' to match DB field
        cid = payload.correlation_id

        existing = (
            self.session.query(ServiceRequest).filter_by(correlation_id=cid).first()
        )
        if existing:
            logger.warning("Duplicate request | correlation_id=%s", cid)
            raise DuplicateCorrelationIdException(correlation_id=cid)

        logger.info("Creating request | correlation_id=%s", cid)
        service_request = ServiceRequest(id=uuid.uuid4(), **payload.dict())

        try:
            self.session.add(service_request)
            self.session.commit()
            logger.info("Request created | correlation_id=%s", cid)
            return service_request
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

    def get_by_correlation_id(self, correlation_id: str) -> ServiceRequest | None:
        """Retrieve a single request by correlation ID."""
        try:
            service_request = (
                self.session.query(ServiceRequest)
                .filter(ServiceRequest.correlation_id == correlation_id)
                .one_or_none()
            )

            if not service_request:
                logger.warning("Request not found | correlation_id=%s", correlation_id)
                return None

            logger.info("Request retrieved | correlation_id=%s", correlation_id)
            return service_request
        except Exception as e:
            logger.error(
                "Query failed | correlation_id=%s | error=%s",
                correlation_id,
                str(e),
                exc_info=True,
            )
            raise DatabaseOperationException(str(e))

    def get_all(self) -> list[ServiceRequest]:
        """Retrieve all service requests."""
        try:
            requests = self.session.query(ServiceRequest).all()
            logger.info("Retrieved all requests | count=%d", len(requests))
            return requests
        except Exception as e:
            logger.error("Query all failed | error=%s", str(e), exc_info=True)
            raise DatabaseOperationException(str(e))

    def update_status(self, correlation_id: str, status: str) -> ServiceRequest:
        """Update status for a specific correlation ID."""
        try:
            service_request = (
                self.session.query(ServiceRequest)
                .filter(ServiceRequest.correlation_id == correlation_id)
                .first()
            )

            if not service_request:
                logger.warning(
                    "Update failed: not found | correlation_id=%s", correlation_id
                )
                raise RequestNotFoundException(ticket_id=correlation_id)

            service_request.status = status
            self.session.commit()

            logger.info(
                "Status updated | correlation_id=%s | status=%s", correlation_id, status
            )
            return service_request

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
