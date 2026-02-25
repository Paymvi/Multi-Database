import os

import dotenv

from application.get_account_use_case import GetAccountUseCase
from application.recover_use_case import RecoverUseCase
from application.withdraw_use_case import WithdrawUseCase
from data_access.coordinator.recover_coordinator import RecoverCoordinator
from data_access.database_connection_provider import DatabaseConnectionProvider
from data_access.transaction_log_repo import TransactionLogRepository
from data_access.transaction_manager import TransactionManager
from application.deposit_use_case import DepositUseCase


class ApplicationContext:
    """The composition root of the application"""

    def __init__(self):
        # Load environment variables from .env file
        dotenv.load_dotenv()

        # Initialize any shared resources or services here
        self.db_provider = DatabaseConnectionProvider(
            account_db_url=os.getenv('ACCOUNT_DB_URL'),
            ledger_db_url=os.getenv('LEDGER_DB_URL')
        )

        # Init Transaction Log Repo
        self.transaction_log_repo = TransactionLogRepository()

        # The TransactionManager
        self.tx_manager = TransactionManager(self.db_provider, self.transaction_log_repo)

        # The recover coordinator
        self.recover_coordinator = RecoverCoordinator(self.db_provider, self.transaction_log_repo)

        # The use cases of the application layer
        self.get_account_use_case = GetAccountUseCase(self.tx_manager)
        self.withdraw_use_case = WithdrawUseCase(self.tx_manager)
        self.deposit_use_case = DepositUseCase(self.tx_manager)
        self.recover_use_case = RecoverUseCase(self.recover_coordinator)

    def shutdown(self):
        """Clean up any resources if necessary."""
        self.db_provider.close()
