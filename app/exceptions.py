from http import HTTPStatus

class AppException(Exception): 
    def __init__(self, status_code: int, detail: str): 
        self.detail = detail
        self.status_code = status_code


class OrderNotFoundException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="Order not found.")


class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")


class PaymentNotFoundException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="Payment not found.")


class ProductNotFoundException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="Product not found.")


class OrderProductException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid relationship between order and product.")


class InvalidPasswordException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid password.")


class UnauthorizedException(AppException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail="You are not authorized to access this resource.")

class ValueError(AppException): 
    def __init__(self):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail="Total value is equal or less than 0")