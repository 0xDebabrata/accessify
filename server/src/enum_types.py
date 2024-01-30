from enum import Enum


class ElementType(Enum):
    BUTTON = "button"
    ANCHOR = "anchor"


class RoleType(Enum):
    USER = "user"
    SYSTEM = "system"
