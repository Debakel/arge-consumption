class ArgeError(Exception):
    """Base error for all exceptions specified in by the ARGE consumption-data API"""

    error_code: int
    message: str


class AutorizationFailure(ArgeError):
    error_code = 401
    message = "Authorization failure."


class PermissionError(ArgeError):
    error_code = 403
    message = "No permission to the requested data with the given credentials."


class NotFound(ArgeError):
    error_code = 404
    message = "No data found for the given billing unit and/or period."


class TechnicalError(ArgeError):
    error_code = 500
    message = "Technical error."


class UnsopportedOperation(ArgeError):
    error_code = 501
    message = "Operation is not supported by the MSC."


class UnsupportedResponse(Exception):
    """Raised if the API returned an unsupported response (which is not defined in the ARGE HAWEIKO spec)"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
