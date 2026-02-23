import uuid

from psycopg import Connection

from data_access.database_connection_provider import DatabaseConnectionProvider


class TwoPhaseCommitCoordinator:

    def __init__(self, db_provider: DatabaseConnectionProvider):
        self._db_provider = db_provider

    def rollback(self) -> None:
        '''Rolls back the transaction across both databases.'''
        rollback_errors: list[str] = []
        for participant_name, participant_conn in self._participants():
            try:
                participant_conn.rollback()
            except Exception as error:
                rollback_errors.append(f'{participant_name}: {error}')

        if rollback_errors:
            error_text = '; '.join(rollback_errors)
            raise RuntimeError(f'Rollback failed for one or more participants: {error_text}')

    def commit(self) -> None:
        '''Commits the transaction across both databases.'''
        tx_id = self._new_transaction_id()
        participants = self._participants()
        prepared_participants: list[tuple[str, Connection]] = []
        commit_decision_recorded = False

        self._append_log(tx_id, 'BEGIN_2PC')

        try:
            for participant_name, participant_conn in participants:
                self._execute(participant_conn, 'PREPARE TRANSACTION %s', (tx_id,))
                prepared_participants.append((participant_name, participant_conn))
                self._append_log(tx_id, 'PREPARED_PARTICIPANT', {'participant': participant_name})

            self._append_log(tx_id, 'DECISION_COMMIT')
            commit_decision_recorded = True

            commit_errors: list[str] = []
            for participant_name, participant_conn in participants:
                try:
                    self._execute(participant_conn, 'COMMIT PREPARED %s', (tx_id,))
                except Exception as error:
                    commit_errors.append(f'{participant_name}: {error}')

            if commit_errors:
                self._append_log(tx_id, 'COMMIT_PARTIAL_FAILURE', {'errors': commit_errors})
                raise RuntimeError('Commit decision recorded but COMMIT PREPARED failed on some participants.')

            self._append_log(tx_id, 'COMMITTED')
        except Exception as error:
            if commit_decision_recorded:
                raise

            if not prepared_participants:
                self.rollback()
                self._append_log(tx_id, 'ABORTED', {'reason': str(error)})
                raise

            self._append_log(tx_id, 'DECISION_ABORT', {'reason': str(error)})

            prepared_names = {name for name, _ in prepared_participants}
            abort_errors: list[str] = []

            for participant_name, participant_conn in prepared_participants:
                try:
                    self._execute(participant_conn, 'ROLLBACK PREPARED %s', (tx_id,))
                except Exception as rollback_error:
                    abort_errors.append(f'{participant_name}: {rollback_error}')

            for participant_name, participant_conn in participants:
                if participant_name in prepared_names:
                    continue
                try:
                    participant_conn.rollback()
                except Exception as rollback_error:
                    abort_errors.append(f'{participant_name}: {rollback_error}')

            if abort_errors:
                self._append_log(tx_id, 'ABORT_PARTIAL_FAILURE', {'errors': abort_errors})
                raise RuntimeError('Abort decision recorded but rollback failed on some participants.') from error

            self._append_log(tx_id, 'ABORTED', {'reason': str(error)})
            raise

    def _participants(self) -> list[tuple[str, Connection]]:
        return [
            ('account_db', self._db_provider.account_db),
            ('ledger_db', self._db_provider.ledger_db),
        ]

    def _append_log(self, tx_id: str, state: str, details: dict | None = None) -> None:
        return None

    @staticmethod
    def _execute(conn: Connection, query: str, params: tuple | None = None) -> None:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

    @staticmethod
    def _new_transaction_id() -> str:
        return f'tx_{uuid.uuid4().hex}'