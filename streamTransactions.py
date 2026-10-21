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
    try:
        with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
            i=1000
            while True:
                
                    print(f"CREATING TRANSACTION {i}", flush=True)
                    i+=1
                    stream_transactions(
                        conn=conn,
                        account_id=random.randint(5300000001, 5300241146),
                        amount=round(random.uniform(50.00, 780.00), 2),
                        txn_type=random.choice(['DEBIT', 'CREDIT'])
                    )
                    time.sleep(round(random.uniform(0.1, 4.7), 2))
                    
    except KeyboardInterrupt as e:
        print("\n\nSUCCESSFULLY INTERRUPTED BY THE USER")


if __name__ == "__main__":
    main()
