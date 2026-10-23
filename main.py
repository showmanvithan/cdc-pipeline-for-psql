from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
from config import DB_CONFIG
app = FastAPI()


@app.get("/transactions")
def get_transactions():
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM transactions
                LIMIT 10
            """)
            return cur.fetchall()