from psycopg import Connection, connect

class DatabaseConnectionProvider:
    '''Provides database connections for different repositories.'''

    def __init__(self, account_db_url: str, ledger_db_url: str):
        self._account_db_conn = connect(account_db_url, autocommit=False) 
        self._ledger_db_conn = connect(ledger_db_url, autocommit=False)

    @property
    def account_db(self) -> Connection: 
        '''Provides a database connection for account-related operations.'''
        return self._account_db_conn

    @property
    def ledger_db(self) -> Connection:
        '''Provides a database connection for ledger-related operations.'''
        return self._ledger_db_conn

    def close(self) -> None:
        '''Closes all database connections silently.'''
        try:
            self._account_db_conn.close()
        except Exception:
            pass  # Ignore errors during close
        try:
            self._ledger_db_conn.close()
        except Exception:
            pass  # Ignore errors during close
    