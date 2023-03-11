from enum import Enum


class SortField(str, Enum):
    CODE: str = "code"
    NAME: str = "name"
    DESCRIPTION: str = "description"
    IS_HIDDEN: str = "is_hidden"
