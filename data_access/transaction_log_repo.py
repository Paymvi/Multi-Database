
from entity.transaction_log_entry import TransactionLogEntry


class TransactionLogRepository:
    '''Repository for managing transaction logs in the database.'''
    
    def write_log(self, transaction_log_entry: TransactionLogEntry) -> None:
        '''Writes a log entry for the transaction.'''
        print(f"Logging transaction {transaction_log_entry.tx_id} with status {transaction_log_entry.status.value}")
