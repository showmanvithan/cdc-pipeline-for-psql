from faker import Faker
import psycopg
from psycopg.rows import dict_row
from decimal import Decimal
from datetime import datetime, timezone
import random
import random
import time
from config import DB_CONFIG


fake = Faker()


def create_txn_table():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id BIGINT GENERATED ALWAYS AS IDENTITY (
                        START WITH 2000000001
                        INCREMENT BY 1) PRIMARY KEY,
                    account_id BIGINT GENERATED ALWAYS AS IDENTITY (
                                            START WITH 2000000001
                                            INCREMENT BY 1) PRIMARY KEY,
                    balance NUMERIC(12, 2) NOT NULL,
                    type VARCHAR(10) NOT NULL
                        CHECK (type IN ('DEBIT', 'CREDIT')),
                    txn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conn.commit()

    print("Transaction Table created successfully.")


def main():
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        try:
            create_txn_table()
            print("Table created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        


            

if __name__ == "__main__":
    main()
