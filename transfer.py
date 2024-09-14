
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    try:
        # Subtract the amount from the sender's account
        update_sender_query = text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender
        """)
        conn.execute(update_sender_query, {'sender': p_sender, 'amount': p_amount})
        
        # Add the amount to the receiver's account
        update_receiver_query = text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver
        """)
        conn.execute(update_receiver_query, {'receiver': p_receiver, 'amount': p_amount})
        
        # Commit the changes
        conn.commit()
    except psycopg2.Error as e:
        # Rollback the changes if an error occurs
        conn.rollback()
        raise e
    finally:
        # Close the connection
        conn.close()
