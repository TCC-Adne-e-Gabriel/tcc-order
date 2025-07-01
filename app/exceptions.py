class AppException(Exception): 
    def __init__(self, status_code: int, detail: str): 
        self.detail = detail
        self.status_code = status_code

class OrderNotFound(AppException): 
    pass

class UserNotFoundException(AppException): 
    pass

class PaymentNotFoundException(AppException): 
    pass

class OrderNotFoundException(AppException): 
    pass

class ProductNotFoundException(AppException): 
    pass

class OrderProductException(AppException):
    pass

class InvalidPasswordException(AppException): 
    pass

class UnauthorizedException(AppException): 
    pass
