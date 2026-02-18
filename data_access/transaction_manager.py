
from .transaction import Transaction
from .database_connection_provider import DatabaseConnectionProvider


class TransactionManager:
    '''Manages database transactions.'''

    def __init__(self, db_provider: DatabaseConnectionProvider):
        self._db_provider = db_provider

    def begin(self) -> Transaction:
        '''Begins a new transaction.'''

        return Transaction(self._db_provider)
