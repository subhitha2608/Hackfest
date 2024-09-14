
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    try:
        conn = engine.connect()
        
        # Subtract the amount from the sender's account
        update_sender_query = text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender;
        """)
        conn.execute(update_sender_query, {'sender': p_sender, 'amount': p_amount})
        
        # Add the amount to the receiver's account
        update_receiver_query = text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver;
        """)
        conn.execute(update_receiver_query, {'receiver': p_receiver, 'amount': p_amount})
        
        conn.commit()
        
        # Return success (no output is expected in this case)
        return True
    
    except psycopg2.Error as e:
        # Handle any database errors
        print(f"Error: {e}")
        return False
    
    finally:
        conn.close()
