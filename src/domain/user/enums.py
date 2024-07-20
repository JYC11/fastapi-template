import enum


class UserType(enum.Enum):
    NORMAL = "NORMAL"
    ADMIN = "ADMIN"


class FeatureAuthorizations(enum.Enum):
    NONE = "NONE"
    ALL_USER_OPERATIONS = "ALL_USER_OPERATIONS"
