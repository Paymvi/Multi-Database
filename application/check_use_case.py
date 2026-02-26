
from data_access.transaction_manager import TransactionManager
from entity import CheckResponce


class CheckUseCase:

    def __init__(self, tx_manager: TransactionManager):
        self.tx_manager = tx_manager
    
    # def check_databases(self) -> CheckResponce | None:
        # with self.tx_manager.begin() as tx:
            # return tx.check_repo.check_accounts()
    
    def check_databases(self) -> CheckResponce | None:
        """Checks if the databases are in a consistent state."""

        with self.tx_manager.begin() as tx:

            accounts = tx.check_repo.fetch_accounts()
            if not accounts:
                return None

            ledger_balances = tx.check_repo.fetch_ledger_balances()

            # Convert ledger results into dictionary
            ledger_map = {account_id: balance for account_id, balance in ledger_balances}

            mismatched_accounts = []

            for account_id, account_balance in accounts:
                ledger_balance = ledger_map.get(account_id, 0)

                if account_balance != ledger_balance:
                    mismatched_accounts.append(account_id)

            if mismatched_accounts:
                print("Mismatched Accounts Found:", mismatched_accounts)
            else:
                print("All accounts reconciled successfully.")

            return CheckResponce(
                message="Check completed successfully.",
                accounts=mismatched_accounts
            )