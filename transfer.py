Python
from config import engine
import pandas as pd

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    try:
        # Subtract the amount from the sender's account
        update_sender_account = text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """).bindparams(p_sender=p_sender, p_amount=p_amount)
        conn.execute(update_sender_account)
        
        # Add the amount to the receiver's account
        update_receiver_account = text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """).bindparams(p_receiver=p_receiver, p_amount=p_amount)
        conn.execute(update_receiver_account)
        
        conn.commit()
        return None
    
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        conn.close()
