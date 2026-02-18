
from data_access.account_repo import AccountRepository
from data_access.database_connection_provider import DatabaseConnectionProvider
from data_access.ledger_repo import LedgerRepository


class Transaction:
    '''Represents a database transaction.'''

    def __init__(self, db_provider: DatabaseConnectionProvider):
        self._db_provider = db_provider
        self._account_repo = AccountRepository(self._db_provider.account_db)
        self._ledger_repo = LedgerRepository(self._db_provider.ledger_db)
    
    ###########
    # Repository accessors
    ###########

    @property
    def account_repo(self) -> AccountRepository:
        '''Provides access to the account repository within the transaction.'''
        return self._account_repo

    @property
    def ledger_repo(self) -> LedgerRepository:
        '''Provides access to the ledger repository within the transaction.'''
        return self._ledger_repo

    ########## 
    # Transactional operations
    ########## 

    def commit(self) -> None:
        '''Commits the transaction.'''
        # Implement the Two-Phase Commit protocol here to ensure atomicity across both databases
        ...

    def rollback(self) -> None:
        '''Rolls back the transaction.'''
        # Implement rollback logic for both databases to ensure consistency in case of failure
        ...

    ###########
    # Context manager methods for automatic transaction handling
    ###########

    def __enter__(self):
        '''Starts a new transaction.'''
        # Do nothing because the psycopg connections automatically start transactions
        # when autocommit is set to False. Just return self to allow access to repositories.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Commits the transaction if no exception, otherwise rolls back.'''
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
