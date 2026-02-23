from decimal import Decimal

from data_access.transaction_manager import TransactionManager
from entity import Account


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

                tx.account_repo.save_account(account)
                return account