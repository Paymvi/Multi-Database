
from dataclasses import dataclass


@dataclass
class TransactionLogEntry:
    '''Represents a log entry for a transaction in the two-phase commit protocol.'''
    pass

class TransactionLogStore:
    '''The actual durable storage for transaction logs.'''
    pass