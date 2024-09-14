Python
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    try:
        # Subtract the amount from the sender's account
        cur = conn.execute(text("""
            UPDATE accounts 
            SET balance = balance - :p_amount 
            WHERE id = :p_sender
        """), {"p_sender": p_sender, "p_amount": p_amount})

        # Add the amount to the receiver's account
        cur = conn.execute(text("""
            UPDATE accounts 
            SET balance = balance + :p_amount 
            WHERE id = :p_receiver
        """), {"p_receiver": p_receiver, "p_amount": p_amount})

        conn.commit()
        return "Funds transfer successful."
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return "Funds transfer failed."

# Testing the function
print(transfer_funds(1, 2, 100))
