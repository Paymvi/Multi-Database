from contextlib import closing
import sqlite3
from entity.transaction_log_entry import TransactionLogEntry, TransactionStatus

DATABASE_FILE = "transaction_log.sqlite3"

class TransactionLogRepository:
    """Repository for managing transaction logs in the database.
    This repository opens the SQLite connection on demand to mimic the behavior of a durable log.
    """

    def __init__(self):
        # Initialize the SQLite database if it doesn't exist
        durable_log_conn = sqlite3.connect(DATABASE_FILE, autocommit=True)
        durable_log_conn.execute("PRAGMA journal_mode=WAL;")
        durable_log_conn.execute("""
            CREATE TABLE IF NOT EXISTS transaction_log (
                tx_id TEXT PRIMARY KEY,
                status TEXT NOT NULL
            );
        """)

    def _connect(self) -> sqlite3.Connection:
        '''Creates a new connection to the SQLite database.'''
        conn = sqlite3.connect(DATABASE_FILE, autocommit=True)
        # Set journal mode to WAL for better and durability
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn


    def write_log(self, transaction_log_entry: TransactionLogEntry) -> None:
        """Writes a log entry for the transaction."""
        with closing(self._connect()) as conn:
            conn.execute("REPLACE INTO transaction_log (tx_id, status) VALUES (?, ?)", (transaction_log_entry.tx_id, transaction_log_entry.status.value))

    def get_pending_logs(self) -> list[TransactionLogEntry]:
        """Retrieves all pending transaction logs."""
        with closing(self._connect()) as conn, closing(conn.cursor()) as cursor:
            cursor.execute("SELECT tx_id, status FROM transaction_log WHERE status in (?, ?)", (TransactionStatus.PREPARING.value, TransactionStatus.COMMITTING.value))
            rows = cursor.fetchall()
            return [TransactionLogEntry(tx_id=row[0], status=TransactionStatus(row[1])) for row in rows]