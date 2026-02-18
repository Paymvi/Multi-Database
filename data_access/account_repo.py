from psycopg import Connection

from entity import Account


class AccountRepository:
    '''Repository for account data access.'''

    def __init__(self, db_conn: Connection):
        self._conn = db_conn


    def get_account_by_id(self, account_id: int) -> Account | None:
        '''Retrieves an account by its ID.'''
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT id, name, balance FROM accounts WHERE id = %s", (account_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Account(id=row[0], name=row[1], balance=row[2])

    def save_account(self, account: Account) -> None:
        '''Save an account to the database.'''
        with self._conn.cursor() as cursor:
            cursor.execute(
                "UPDATE accounts SET name = %s, balance = %s WHERE id = %s",
                (account.name, account.balance, account.id)
            )