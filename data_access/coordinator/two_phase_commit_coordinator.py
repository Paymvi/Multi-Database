import uuid

from psycopg import Connection

from data_access.database_connection_provider import DatabaseConnectionProvider


# Logs are not implemented yet
class TwoPhaseCommitCoordinator:

    def __init__(self, db_provider: DatabaseConnectionProvider):
        self._db_provider = db_provider

    def rollback(self) -> None:
        '''Rolls back the transaction across both databases.'''
        # Not Needed since we have a recover command 

    def commit(self) -> None:
        '''Commits the transaction across both databases using 2PC.'''
        # Createa a unique transaction ID for this 2PC transaction
        tx_id = self._new_transaction_id()
        participants = self._participants()
        prepared_participants: list[tuple[str, Connection]] = []

        try:
            # Phase 1: Prepare
            for participant_name, participant_conn in participants:
                self._execute(participant_conn, 'PREPARE TRANSACTION %s', (tx_id,))
                prepared_participants.append((participant_name, participant_conn))

            # Phase 2: Commit
            for participant_name, participant_conn in participants:
                self._execute(participant_conn, 'COMMIT PREPARED %s', (tx_id,))

        except Exception as error:
            # Abort: throw out the error since we have a recover command we can run later to manually revocer the transaction if needed
            print(f"Error handling the transaction: {error}")


    #Hardcoded participant list for now but we can make it dynamic later
    def _participants(self) -> list[tuple[str, Connection]]:
        return [
            ('account_db', self._db_provider.account_db),
            ('ledger_db', self._db_provider.ledger_db),
        ]

    @staticmethod
    def _execute(conn: Connection, query: str, params: tuple | None = None) -> None:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

    @staticmethod
    def _new_transaction_id() -> str:
        return f'tx_{uuid.uuid4().hex}'