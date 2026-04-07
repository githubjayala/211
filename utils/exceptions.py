class DatabaseInsertException(Exception):
    def __init__(self, message: str = "Database insert operation failed"):
        self.message = message
        super().__init__(self.message)


class DatabaseUpdateException(Exception):
    def __init__(self, message: str = "Database update operation failed"):
        self.message = message
        super().__init__(self.message)


class DatabaseConnectionException(Exception):
    def __init__(self, message: str = "Database connection operation failed"):
        self.message = message
        super().__init__(self.message)


class DatabaseOperationException(Exception):
    def __init__(self, message: str = "Database operation failed"):
        self.message = message
        super().__init__(self.message)
