class ResponseException(Exception):
    def __init__(self, status_code: int, body: bytes):
        self.status_code = status_code
        self.body = body

        super().__init__(f"Response exception [{status_code}]: {body}")
