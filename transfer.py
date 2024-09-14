
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    with engine.connect() as connection:
        # Subtract the amount from the sender's account
        subtract_query = text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender
        """)
        connection.execute(subtract_query, {'sender': p_sender, 'amount': p_amount})
        
        # Add the amount to the receiver's account
        add_query = text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver
        """)
        connection.execute(add_query, {'receiver': p_receiver, 'amount': p_amount})
        
        connection.commit()
