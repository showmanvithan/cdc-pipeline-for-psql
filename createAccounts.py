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


def create_accounts_table():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id BIGINT GENERATED ALWAYS AS IDENTITY (
                        START WITH 5300000001
                        INCREMENT BY 1) PRIMARY KEY,
                    user_id BIGINT GENERATED ALWAYS AS IDENTITY (
                                            START WITH 1300000001
                                            INCREMENT BY 1) ,
                    balance NUMERIC(12, 2) NOT NULL,
                    txn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conn.commit()

    print("Accounts Table created successfully.")


def create_accounts(conn, balance):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO accounts (balance)
            VALUES (%s)
          
            """,
            (balance,)
        )
        
    conn.commit()
    


def main():
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        create_accounts_table()
        for _ in range(241146):
                print("Creating user...", flush=True)
                create_accounts(
                    conn=conn,
                    balance=round(random.uniform(50.00, 50_000.00), 2),
                    
                )
                
                print("User created successfully", flush=True)

    

if __name__ == "__main__":
    main()
