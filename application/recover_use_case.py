
from data_access.coordinator.recover_coordinator import RecoverCoordinator
from data_access.transaction_log_repo import TransactionLogRepository


class RecoverUseCase:

    def __init__(self, recover_cooridinator: RecoverCoordinator):
        self._recover_coordinator = recover_cooridinator

    def recover(self) -> int:
        '''Recovers from pending transactions.
        
        Returns:
            int: The number of transactions recovered.
        '''
        return self._recover_coordinator.recover()
