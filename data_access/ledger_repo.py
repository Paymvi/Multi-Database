from psycopg import Connection

from entity import LedgerEntry

class LedgerRepository:
    '''Ledger entry data access.'''

    def __init__(self, db_conn: Connection):
        self._conn = db_conn

    def create_ledger_entry(self, entry: LedgerEntry) -> None:
        '''Creates a new ledger entry in the database.'''
        ...

    def get_ledger_entries_by_account_id(self, account_id: int) -> list[LedgerEntry]:
        '''Retrieves all ledger entries for a given account ID.'''
        ...