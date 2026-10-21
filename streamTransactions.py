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




def stream_transactions(conn, account_id, amount, txn_type):
    with conn.transaction():
        with conn.cursor() as cur:

            if txn_type == "DEBIT":
                cur.execute("""
                    UPDATE accounts
                    SET balance = balance - %s
                    WHERE account_id = %s
                      AND balance >= %s
                    RETURNING balance;
                """, (amount, account_id, amount))
                
            
                
                cur.execute("""
                                INSERT INTO transactions
                                    (account_id, amount, txn_type, txn_time)
                                VALUES (%s, %s, %s, NOW());
                            """, (account_id, amount, txn_type))
                


            elif txn_type == "CREDIT":
                cur.execute("""
                    UPDATE accounts
                    SET balance = balance + %s
                    WHERE account_id = %s
                    RETURNING balance;
                """, (amount, account_id))
                
                cur.execute("""
                                INSERT INTO transactions
                                    (account_id, amount, txn_type, txn_time)
                                VALUES (%s, %s, %s, NOW());
                            """, (account_id, amount, txn_type))

            else:
                raise ValueError("Invalid transaction type")

        
def main():
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:

                print("Creating transaction...", flush=True)
                stream_transactions(
                    conn=conn,
                    account_id= 5300000002,
                    # amount=round(random.uniform(50.00, 10_000.00), 2),
                    amount=50000,
                    txn_type='DEBIT'
                )
                
                

    

if __name__ == "__main__":
    main()
