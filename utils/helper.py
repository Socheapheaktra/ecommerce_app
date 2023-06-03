import socket

DEFAULT_ERROR_MESSAGE = "An unexpected error occurred."
DEFAULT_SUCCESS_MESSAGE = "Query Successful"

class Response:
    def __init__(
        self, 
        data: any = {}, 
        code: int = 200, 
        status: str = "Success",
        message: str = DEFAULT_SUCCESS_MESSAGE,
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
    def created(cls, data: any = {}, message: str = DEFAULT_SUCCESS_MESSAGE) -> "Response":
        res = cls(
            code=201,
            message=message,
            data=data,
        )
        return res, 201

    @classmethod
    def unimplemented(cls) -> "Response":
        res = cls(
            code=501, 
            status="Not Implemented.", 
            message="Sorry, This feature is not yet implemented."
        )
        return res, 501

    @classmethod
    def server_error(cls, message: str = DEFAULT_ERROR_MESSAGE) -> "Response":
        res = cls(
            code=500,
            status="Internal Server Error",
            message=message
        )
        return res, 500

    @classmethod
    def bad_request(cls, message: str = DEFAULT_ERROR_MESSAGE) -> "Response":
        res = cls(
            code=400,
            status="Bad Request",
            message=message,
        )
        return res, 400

    @classmethod
    def not_found(cls, message: str = DEFAULT_ERROR_MESSAGE) -> "Response":
        res = cls(
            code=404,
            status="Not found",
            message=message
        )
        return res, 404

    @classmethod
    def access_denied(cls) -> "Response":
        res = cls(
            code=403,
            status="Access Denied.",
            message="Permission denied. Please contact admin."
        )
        return res, 403
