
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_balance(p_sender, p_receiver, p_amount):
    # Create a connection to the database
    conn = engine.connect()

    try:
        # Update sender's balance
        update_sender_query = text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender")
        conn.execute(update_sender_query, {"p_sender": p_sender, "p_amount": p_amount})
        
        # Update receiver's balance
        update_receiver_query = text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver")
        conn.execute(update_receiver_query, {"p_receiver": p_receiver, "p_amount": p_amount})
        
        # Commit changes
        conn.commit()
    
    except psycopg2.Error as e:
        # Rollback changes if an error occurs
        conn.rollback()
        raise e
    
    finally:
        # Close the connection
        conn.close()

    # Return None, as the original procedure doesn't return any value
    return None
