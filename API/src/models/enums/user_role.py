from enum import Enum


class UserRole(Enum):
    CLIENT = 'client'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'
