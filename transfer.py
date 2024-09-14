
from config import engine
from sqlalchemy import text
import pandas as pd

def transfer_funds(p_sender, p_receiver, p_amount):
    # Create a Connection from the engine
    conn = engine.connect()

    try:
        # Subtract the amount from the sender's account
        result = conn.execute(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), 
                             p_sender=p_sender, p_amount=p_amount)
        
        # Add the amount to the receiver's account
        result = conn.execute(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), 
                             p_receiver=p_receiver, p_amount=p_amount)
        
        conn.commit()  
    except Exception as e:
        conn.rollback()  
        print(f"Error: {e}")
    finally:
        conn.close()
