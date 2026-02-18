
from data_access.database_connection_provider import DatabaseConnectionProvider


class TwoPhaseCommitCoordinator:

    def __init__(self, db_provider: DatabaseConnectionProvider):
        self._db_provider = db_provider
    
    def rollback(self):
        '''Rolls back the transaction across both databases.'''
        # Implement rollback logic for both databases to ensure consistency in case of failure
        ...

    def commit(self):
        '''Commits the transaction across both databases.'''
        # Implement the Two-Phase Commit protocol here to ensure atomicity across both databases
        ...