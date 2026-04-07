from database import SessionLocal
from models import ServiceRequest
from repository import RequestRepository
from utils.logger import get_logger


logger = get_logger("request-service")


class RequestService:
    def create_request(self, payload) -> ServiceRequest:
        logger.info(
            "Creating service request | correlation_id=%s", payload.correlation_id
        )
        db = SessionLocal()
        try:
            repo = RequestRepository(db)
            result = repo.create_request(payload)
            return result
        except Exception as e:
            db.rollback()
            logger.error("Failed to create request | error=%s", str(e), exc_info=True)
            raise
        finally:
            db.close()

    def get_by_correlation_id(self, correlation_id: str) -> ServiceRequest | None:
        logger.info(
            "Retrieving request by id | correlation_id=%s",
            correlation_id,
        )
        db = SessionLocal()
        try:
            repo = RequestRepository(db)
            result = repo.get_by_correlation_id(correlation_id)
            return result
        except Exception as e:
            db.rollback()
            logger.error("Failed to retrieve request | error=%s", str(e), exc_info=True)
            raise
        finally:
            db.close()

    def get_all(self) -> list[ServiceRequest]:
        logger.info("Retrieving all requests")
        db = SessionLocal()
        try:
            repo = RequestRepository(db)
            result = repo.get_all()
            return result
        except Exception as e:
            db.rollback()
            logger.error(
                "Failed to retrieve all requests | error=%s", str(e), exc_info=True
            )
            raise
        finally:
            db.close()

    def update_status(self, correlation_id: str, status: str) -> ServiceRequest:
        logger.info(
            "Updating status request | correlation_id=%s | status=%s",
            correlation_id,
            status,
        )
        db = SessionLocal()
        try:
            repo = RequestRepository(db)
            result = repo.update_status(correlation_id, status)
            return result
        except Exception as e:
            db.rollback()
            logger.error("Failed to update request | error=%s", str(e), exc_info=True)
            raise
        finally:
            db.close()
