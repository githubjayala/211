class TicketNotFoundException(Exception):
    def __init__(self, correlation_id: str | None):
        self.message = (
            f"Ticket not found | correlation_id={correlation_id}"
            if correlation_id
            else "Ticket not found"
        )
        super().__init__(self.message)


class DuplicateCorrelationIdException(Exception):
    def __init__(self, correlation_id: str | None):
        self.message = (
            f"Duplicate correlation_id detected | correlation_id={correlation_id}"
            if correlation_id
            else "Duplicate correlation_id detected"
        )
        super().__init__(self.message)
