from curses import error
import uuid

from psycopg import Connection

from data_access.database_connection_provider import DatabaseConnectionProvider
from data_access.transaction_log_repo import TransactionLogRepository
from entity.transaction_log_entry import TransactionLogEntry, TransactionStatus


# Logs are not implemented yet
class TwoPhaseCommitCoordinator:

    def __init__(self, db_provider: DatabaseConnectionProvider , transaction_log_repo: TransactionLogRepository):
        self._db_provider = db_provider
        self._transaction_log_repo = transaction_log_repo

    def rollback(self) -> None:
        '''Rolls back the transaction across both databases.'''
        # Not Needed since we have a recover command 

    def commit(self) -> None:
        '''Commits the transaction across both databases using 2PC.'''
        tx_id = self._new_transaction_id()
        participants = self._participants()
        prepared_participants: list[tuple[str, Connection]] = []

        print(f'Starting 2PC transaction with ID: {tx_id}')

        try:
            # Phase 1: PREPARE
            self._transaction_log_repo.write_log(TransactionLogEntry(tx_id = tx_id , status = TransactionStatus.PREPARING))
            for participant_name, participant_conn in participants:
                with participant_conn.cursor() as cursor:
                    cursor.execute(f"PREPARE TRANSACTION '{tx_id}'")
                prepared_participants.append((participant_name, participant_conn))
            
            self._transaction_log_repo.write_log(TransactionLogEntry(tx_id = tx_id , status = TransactionStatus.COMMITTING))

            # Phase 2: COMMIT PREPARED
            for participant_name, participant_conn in participants:
                participant_conn.autocommit = True   # critical
                with participant_conn.cursor() as cursor:
                    cursor.execute(f"COMMIT PREPARED '{tx_id}'")
            self._transaction_log_repo.write_log(TransactionLogEntry(tx_id = tx_id , status = TransactionStatus.COMMITTED))

        except Exception as error:
            raise RuntimeError(f"Error handling the transaction: {error}")

    #Hardcoded participant list for now but we can make it dynamic later
    def _participants(self) -> list[tuple[str, Connection]]:
        return [
            ('account_db', self._db_provider.account_db),
            ('ledger_db', self._db_provider.ledger_db),
        ]


    @staticmethod
    def _new_transaction_id() -> str:
        return f'tx_{uuid.uuid4().hex}'