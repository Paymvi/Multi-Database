from psycopg import Connection
from entity import CheckResponce

class CheckRepository:
    '''Repository for account and Ledger data access.'''

    def __init__(self, account_db: Connection, ledger_db: Connection):
        self._account_db = account_db
        self._ledger_db = ledger_db

    def check_accounts(self) -> CheckResponce | None:
        '''Retrieves accounts and sum of ledger entries from two databases.'''

        # Query Accounts DB
        with self._account_db.cursor() as account_cursor:
            account_cursor.execute("SELECT id, balance FROM accounts")
            account_rows = account_cursor.fetchall()

        if not account_rows:
            return None

        # Query Ledger DB
        with self._ledger_db.cursor() as ledger_cursor:
            ledger_cursor.execute(
                "SELECT account_id, SUM(amount) FROM ledger GROUP BY account_id"
            )
            ledger_rows = ledger_cursor.fetchall()

        # Convert ledger results into dictionary for easy matching
        ledger_map = {row[0]: row[1] for row in ledger_rows}

        # Store mismatched account IDs
        mismatched_accounts = []

        for account_id, balance in account_rows:
            ledger_sum = ledger_map.get(account_id, 0)

            # Compare balances
            if balance != ledger_sum:
                mismatched_accounts.append(account_id)

        # If needed for debugging
        if mismatched_accounts:
            print("Mismatched Accounts Found:")
            print(mismatched_accounts)
        else:
            print("All accounts reconciled successfully.")

        return CheckResponce(
            message="Check completed successfully.",
            accounts=mismatched_accounts
        )

        