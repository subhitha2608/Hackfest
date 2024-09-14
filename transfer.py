Python
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from config import engine
import pandas as pd

def transfer_amount(sender, receiver, amount):
    try:
        # Create a connection from the engine
        conn = engine.connect()

        # Create a DDL command to check if the 'accounts' table exists
        conn.execute("""CREATE TABLE IF NOT EXISTS accounts (
            id SERIAL PRIMARY KEY,
            balance INTEGER DEFAULT 0
        )""")

        # Execute the SQL query with parameters
        result = conn.execute(text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender;

            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver;
        "), {"sender": sender, "receiver": receiver, "amount": amount})

        # Commit the transaction
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error: ", str(e))
    finally:
        conn.close()
