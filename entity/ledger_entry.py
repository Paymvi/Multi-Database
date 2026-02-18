from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class LedgerEntryType(Enum):
    '''Enum for types of ledger entries.'''
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'


@dataclass
class LedgerEntry:
    '''Represents a ledger entry for a financial transaction.'''
    id: int
    account_id: int
    entry_type: LedgerEntryType
    amount: Decimal