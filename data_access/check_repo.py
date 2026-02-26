from psycopg import Connection

class CheckRepository:
    '''Repository for account and Ledger data access.'''

    def __init__(self, account_db: Connection, ledger_db: Connection):
        self._account_db = account_db
        self._ledger_db = ledger_db

    def fetch_accounts(self) -> list[tuple[int, float]] | None:
        """Fetch account balances from Accounts DB"""
        with self._account_db.cursor() as cursor:
            cursor.execute("SELECT id, balance FROM accounts")
            rows = cursor.fetchall()
            return rows if rows else None
    
    def fetch_ledger_balances(self) -> list[tuple[int, float]]:
        """Fetch computed ledger balances from Ledger DB"""
        with self._ledger_db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    account_id,
                    SUM(
                        CASE 
                            WHEN type = 'deposit' THEN amount
                            ELSE -amount
                        END
                    ) AS net_balance
                FROM ledger
                GROUP BY account_id
            """)
            return cursor.fetchall()