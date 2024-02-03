from enum import Enum


class ElementType(str, Enum):
    BUTTON = "button"
    ANCHOR = "anchor"


class RoleType(str, Enum):
    USER = "user"
    SYSTEM = "system"
