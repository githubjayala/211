from database import SessionLocal
from models import TicketRequest
from repository import TicketRepository
from utils.logger import get_logger

logger = get_logger("ticket-service")


class TicketService:
    def create_ticket(self, payload) -> TicketRequest:
        db = SessionLocal()
        try:
            repo = TicketRepository(db)
            result = repo.create_ticket(payload)
            return result
        except Exception as e:
            db.rollback()
            logger.error("Failed to create ticket | error=%s", str(e), exc_info=True)
            raise
        finally:
            db.close()

    def get_by_correlation_id(self, correlation_id: str) -> TicketRequest | None:
        logger.info("Retrieving ticket by id | correlation_id=%s", correlation_id)
        db = SessionLocal()
        try:
            repo = TicketRepository(db)
            result = repo.get_by_correlation_id(correlation_id)
            return result
        except Exception as e:
            db.rollback()
            logger.error("Failed to retrieve ticket | error=%s", str(e), exc_info=True)
            raise
        finally:
            db.close()

    def get_all(self) -> list[TicketRequest]:
        logger.info("Retrieving all requests")
        db = SessionLocal()
        try:
            repo = TicketRepository(db)
            result = repo.get_all()
            return result
        except Exception as e:
            db.rollback()
            logger.error(
                "Failed to retrieve all request | error=%s", str(e), exc_info=True
            )
            raise
        finally:
            db.close()

    def update_status(self, correlation_id: str, status: str) -> TicketRequest:
        logger.info(
            "Updating ticket status | correlation_id=%s | status=%s",
            correlation_id,
            status,
        )
        db = SessionLocal()
        try:
            repo = TicketRepository(db)
            result = repo.update_status(correlation_id, status)
            return result
        except Exception as e:
            db.rollback()
            logger.error("Failed to update ticket | error=%s", str(e), exc_info=True)
            raise
        finally:
            db.close()
