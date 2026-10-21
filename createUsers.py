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


def create_table():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT GENERATED ALWAYS AS IDENTITY (
                        START WITH 1300000001
                        INCREMENT BY 1) PRIMARY KEY,
                    user_name VARCHAR(100) NOT NULL,
                    email VARCHAR(150) UNIQUE,
                    risk_tier VARCHAR(10) NOT NULL
                        CHECK (risk_tier IN ('MEDIUM', 'LOW', 'HIGH'))
                );
            """)

        conn.commit()

    print("Table created successfully.")


def create_user(conn, user_name, email, risk_tier):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (user_name, email, risk_tier)
            VALUES (%s, %s, %s)
            RETURNING user_id, user_name, email, risk_tier;
            """,
            (user_name, email, risk_tier),
        )
        
    conn.commit()
    


def main():
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        create_table()
        while True:
            try:
                print("Creating user...", flush=True)
                create_user(
                    conn=conn,
                    user_name=fake.name(),
                    email=fake.unique.email(),
                    risk_tier=random.choices(
                        ["HIGH", "LOW", "MEDIUM"],
                        weights=[0.1, 0.7, 0.2],
                        k=1
                    )[0]
                )
                print("User created successfully", flush=True)
                # time.sleep(0.2)
            except Exception as e:
                print("skipping")


            

if __name__ == "__main__":
    main()
