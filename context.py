import os

import dotenv

from application.get_account_use_case import GetAccountUseCase
from application.withdraw_use_case import WithdrawUseCase
from data_access.database_connection_provider import DatabaseConnectionProvider
from data_access.transaction_manager import TransactionManager


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

        # The TransactionManager
        self.tx_manager = TransactionManager(self.db_provider)

        # The use cases of the application layer
        self.get_account_use_case = GetAccountUseCase(self.tx_manager)
        self.withdraw_use_case = WithdrawUseCase(self.tx_manager)

    def shutdown(self):
        """Clean up any resources if necessary."""
        self.db_provider.close()
