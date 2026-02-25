from dataclasses import dataclass
from enum import Enum

class TransactionStatus(Enum):
    '''Enum for transaction statuses.'''
    PREPARING = 'preparing'
    COMMITTING = 'committing'
    COMMITTED = 'committed'
    ROLLBACKED = 'rollbacked'

@dataclass
class TransactionLogEntry:
    '''Represents a log entry for a transaction in the two-phase commit protocol.'''
    tx_id: str
    status: TransactionStatus