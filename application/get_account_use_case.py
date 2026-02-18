
from data_access.transaction_manager import TransactionManager
from entity import Account


class GetAccountUseCase:

    def __init__(self, tx_manager: TransactionManager):
        self.tx_manager = tx_manager
    
    def get_account(self, account_id: int) -> Account | None:
        """Retrieves an account by its ID."""

        with self.tx_manager.begin() as tx:
            return tx.account_repo.get_account_by_id(account_id)