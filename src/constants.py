from enum import Enum

class SortBy(str, Enum):
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    TOTAL = "total"