from data_access.transaction_manager import TransactionManager
from entity import Account, LedgerEntry
from decimal import Decimal


class DepositUseCase:
    def __init__(self, tx_manager: TransactionManager):
        self.tx_manager = tx_manager

    def deposit(self, account_id: int, amount: Decimal) -> Account:

        # Checks to make sure the input is positive
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        with self.tx_manager.begin() as tx:
            # Fetches the account
            account = tx.account_repo.get_account_by_id(account_id) 

            if account is None:
                raise ValueError(f"Account not found: {account_id}")

            # Update balance
            account.balance += amount
            tx.account_repo.save_account(account)

            # Record ledger entry
            entry = LedgerEntry(
                id=0,  # placeholder; DB will generate the real id
                account_id=account_id,
                entry_type="deposit",
                amount=amount,
            )

            tx.ledger_repo.create_ledger_entry(entry)

            return account