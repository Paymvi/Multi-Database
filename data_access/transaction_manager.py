
from data_access.transaction_log_repo import TransactionLogRepository

from .transaction import Transaction
from .database_connection_provider import DatabaseConnectionProvider


class TransactionManager:
    '''Manages database transactions.'''

    def __init__(self, db_provider: DatabaseConnectionProvider , transaction_log_repo: TransactionLogRepository):
        self._db_provider = db_provider
        self._transaction_log_repo = transaction_log_repo


    def begin(self) -> Transaction:
        '''Begins a new transaction.'''

        return Transaction(self._db_provider, self._transaction_log_repo)
