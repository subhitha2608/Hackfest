
from sqlalchemy import create_engine, text
from config import engine
import pandas as pd

def transfermoney(p_sender, p_receiver, p_amount):
    with engine.connect() as conn:
        # Subtract the amount from the sender's account
        conn.execute(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), 
                     {"p_sender": p_sender, "p_amount": p_amount})

        # Add the amount to the receiver's account
        conn.execute(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), 
                     {"p_receiver": p_receiver, "p_amount": p_amount})

        # Commit the changes
        conn.commit()

fromalchemy import create_engine, text

def create_table():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance INTEGER)"))
        
        # Commit the changes
        conn.commit()

import pandas as pd

def get_balance(p_id):
    with engine.connect() as conn:
        df = pd.read_sql_query(text("SELECT balance FROM accounts WHERE id = :p_id"), conn, 
                               params={"p_id": p_id})
        return df.iloc[0]['balance']
