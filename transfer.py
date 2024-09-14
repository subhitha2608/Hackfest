
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    
    try:
        # Subtract the amount from the sender's account
        update_sender_query = sa.text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender
        """)
        conn.execute(update_sender_query, {'sender': p_sender, 'amount': p_amount})
        
        # Add the amount to the receiver's account
        update_receiver_query = sa.text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver
        """)
        conn.execute(update_receiver_query, {'receiver': p_receiver, 'amount': p_amount})
        
        conn.commit()
        
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    
    finally:
        conn.close()
    
    return None  # Return None as per the original procedure
