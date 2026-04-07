class RequestNotFoundException(Exception):
    def __init__(self, ticket_id: str = None):
        self.message = (
            f"Service request not found | ticket_id={ticket_id}"
            if ticket_id
            else "Service request not found"
        )
        super().__init__(self.message)


class DuplicateCorrelationIdException(Exception):
    def __init__(self, correlation_id: str = None):
        self.message = (
            f"Duplicate correlation_id detected | correlation_id={correlation_id}"
            if correlation_id
            else "Duplicate correlation_id detected"
        )
        super().__init__(self.message)
