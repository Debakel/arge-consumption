class BaseError(Exception):
    error_code: int
    message: str


class AutorizationFailure(BaseError):
    error_code = 401
    message = "Authorization failure."


class PermissionError(BaseError):
    error_code = 403
    message = "No permission to the requested data with the given credentials."


class NotFound(BaseError):
    error_code = 404
    message = "No data found for the given billing unit and/or period."


class TechnicalError(BaseError):
    error_code = 500
    message = "Technical error."


class UnsopportedOperation(BaseError):
    error_code = 501
    message = "Operation is not supported by the MSC."
