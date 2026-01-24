class AppBaseException(Exception):
    pass

class NotFoundException(AppBaseException):
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail

class BadRequestException(AppBaseException):
    def __init__(self, detail: str = "Bad request"):
        self.detail = detail

class ForbiddenException(AppBaseException):
    def __init__(self, detail: str = "Permission denied"):
        self.detail = detail

class UnauthorizedException(AppBaseException):
    def __init__(self, detail: str = "Not authenticated"):
        self.detail = detail

# Specific Exceptions
class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("User not found")

class CompanyNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Company not found")

class OfficeNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Office not found")

class ShipmentNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Shipment not found")

class UserAlreadyExistsException(BadRequestException):
    def __init__(self):
        super().__init__("User with this email already exists")

class CompanyAlreadyExistsException(BadRequestException):
    def __init__(self):
        super().__init__("Company with this name already exists")

class InvalidCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Could not validate credentials")
