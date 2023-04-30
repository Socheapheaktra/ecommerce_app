import socket

DEFAULT_ERROR_MESSAGE = "An unexpected error occurred."

class Response:
    def __init__(
        self, 
        data: any = {}, 
        code: int = 200, 
        status: str = "OK",
        message: str = "Query Successful",
    ) -> None:
        self.code = code
        self.status = status
        self.data = data
        self.message = message

    @property
    def json(self) -> dict:
        return {
            "code": self.code,
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

    def without_data(self) -> dict:
        return {
            "code": self.code,
            "status": self.status,
            "message": self.message,
        }
    
    @classmethod
    def unimplemented(cls) -> "Response":
        return cls(
            code=501, 
            status="Not Implemented.", 
            message="Sorry, This feature is not yet implemented."
        )
    
    @classmethod
    def server_error(cls, message: str = DEFAULT_ERROR_MESSAGE) -> "Response":
        return cls(
            code=500,
            status="Internal Server Error",
            message=message
        )

    @classmethod
    def bad_request(cls, message: str = DEFAULT_ERROR_MESSAGE) -> "Response":
        return cls(
            code=400,
            status="Bad Request",
            message=message,
        )
    
    @classmethod
    def not_found(cls, message: str = DEFAULT_ERROR_MESSAGE) -> "Response":
        return cls(
            code=404,
            status="Not found",
            message=message
        )

    @classmethod
    def access_denied(cls) -> "Response":
        return cls(
            code=403,
            status="Access Denied.",
            message="Permission denied. Please contact admin."
        )