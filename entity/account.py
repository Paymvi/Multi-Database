
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Account:
    '''Represents a financial account.'''
    id: int
    name: str
    balance: Decimal
