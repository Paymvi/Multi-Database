from decimal import Decimal

from data_access.transaction_manager import TransactionManager
from entity import Account
from entity.ledger_entry import LedgerEntry, LedgerEntryType


class WithdrawUseCase:

    def __init__(self, tx_manager: TransactionManager):
        self.tx_manager = tx_manager
    
    def withdraw(self, account_id: int, amount: Decimal) -> Account | None:
        """Withdraws an amount from an account."""

        print(f'Attempting to withdraw {amount} from account ID {account_id}...')

        with self.tx_manager.begin() as tx:
                account = tx.account_repo.get_account_by_id(account_id)
                if not account:
                    print(f'Account ID {account_id} not found.')
                    return None
                
                if account.balance < amount:
                    print(f'Insufficient funds in account ID {account_id}. Current balance: {account.balance}')
                    return None
                
                account.balance -= amount

                # Record account entry
                tx.account_repo.save_account(account)

                # Record ledger entry
                entry = LedgerEntry(
                    id=0,  # placeholder; DB will generate the real id
                    account_id=account_id,
                    entry_type=LedgerEntryType.WITHDRAW, # Updated to not use hard coded string
                    amount=amount,
                )

                tx.ledger_repo.create_ledger_entry(entry)


                return account