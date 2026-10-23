
import os
import sys
import psycopg2
import psycopg2.extras 



# Configure these environment variables before running the script.
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "appdb",
    "user": "replicator",
    "password": os.environ.get("DB_PASSWORD")
}

SLOT_NAME = "transactions_slot"


class ChangeLogger:
    """Print decoded PostgreSQL changes and acknowledge processed messages."""

    def __call__(self, msg):
        try:
            print(f"[DATABASE CHANGE] {msg.payload}", flush=True)

            # Acknowledge only after the message has been logged.
            msg.cursor.send_feedback(flush_lsn=msg.data_start)

        except Exception as exc:
            print(f"Error processing change: {exc}", file=sys.stderr)
            raise


def main():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            **DB_CONFIG,
            connection_factory=(
                psycopg2.extras.LogicalReplicationConnection
            ),
        )
        cur = conn.cursor()

        print(f"Connected to database: {DB_CONFIG['dbname']}")
        print(f"Replication slot: {SLOT_NAME}")
        print("Waiting for database changes... (Ctrl+C to stop)")

        cur.start_replication(
            slot_name=SLOT_NAME,
            decode=True,
            status_interval=10,
        )

        cur.consume_stream(ChangeLogger())

    except KeyboardInterrupt:
        print("\nStopping CDC logger...")

    except Exception as exc:
        print(f"CDC logger failed: {exc}", file=sys.stderr)
        raise

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
