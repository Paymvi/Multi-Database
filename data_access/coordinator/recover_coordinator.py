from psycopg import Connection, OperationalError
from psycopg.errors import UndefinedObject

from data_access.database_connection_provider import DatabaseConnectionProvider
from data_access.transaction_log_repo import TransactionLogRepository
from entity.transaction_log_entry import TransactionLogEntry, TransactionStatus


class RecoverCoordinator:
    '''Handles recovery of in-progress transactions after a crash.'''
    
    def __init__(self, db_provider: DatabaseConnectionProvider, transaction_log_repo: TransactionLogRepository):
        self._db_provider = db_provider
        self._transaction_log_repo = transaction_log_repo

    def rollback(self, tx_id: str):
        '''Roll back the prepared transaction with the given transaction ID.'''
        
        # The loop is not guarded by try-except, so any error will case the recovery process halt.
        # Without updateing the log, the recovery process will remain in `preparing` state, and can be recovered in the next recovery process.
        for _, participant_conn in self._participants():
            participant_conn.autocommit = True
            try:
                participant_conn.execute(f"ROLLBACK PREPARED '{tx_id}'")
            except UndefinedObject as error:
                # continue with the next participant, as the transaction can be rolled back in the next recovery process.
                pass

        self._transaction_log_repo.write_log(TransactionLogEntry(tx_id = tx_id , status = TransactionStatus.ROLLBACKED))
        
    def commit(self, tx_id: str):
        '''Commit the prepared transaction with the given transaction ID.'''

        # The loop is not guarded by try-except, so any error will case the recovery process halt.
        # Without updateing the log, the recovery process will remain in `committing` state, and can be recovered in the next recovery process.
        for _, participant_conn in self._participants():
            participant_conn.autocommit=True
            try:
                participant_conn.execute(f"COMMIT PREPARED '{tx_id}'")
            except UndefinedObject as error:
                # continue with the next participant, as the transaction can be committed in the next recovery process.
                pass

        self._transaction_log_repo.write_log(TransactionLogEntry(tx_id = tx_id , status = TransactionStatus.COMMITTED))

    def get_pending_transactions(self) -> list[TransactionLogEntry]:
        '''Retrieves the list of pending transactions from the transaction log.'''
        return self._transaction_log_repo.get_pending_logs()

    def recover(self) -> int:
        '''Recovers from pending transactions.'''

        # Retrieve all the pending transaction logs
        pending_logs = self._transaction_log_repo.get_pending_logs()

        # Solve the pending transactions based on their status (PREPARING, COMMITTING, etc.)
        for log in pending_logs:
            if log.status == TransactionStatus.PREPARING:
                # rollback the transactions
                self.rollback(log.tx_id)
            elif log.status == TransactionStatus.COMMITTING:
                # continue with the commit process.
                self.commit(log.tx_id)
            else:
                # do nothing for other statuses, as they are not pending transactions
                pass

        return len(pending_logs)
    
    def _participants(self) -> list[tuple[str, Connection]]:
        '''Returns the list of participants in the transaction.'''
        return [
            ("account_db", self._db_provider.account_db),
            ("ledger_db", self._db_provider.ledger_db)
        ]