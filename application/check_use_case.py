
from data_access.transaction_manager import TransactionManager
from entity import CheckResponce


class CheckUseCase:

    def __init__(self, tx_manager: TransactionManager):
        self.tx_manager = tx_manager
    
    def check_databases(self) -> CheckResponce | None:
        """Checks if the databases are in a consistent state."""

        with self.tx_manager.begin() as tx:
            return tx.check_repo.check_accounts()