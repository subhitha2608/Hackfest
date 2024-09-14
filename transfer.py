
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    # Define SQL queries as text objects
    update_sender_query = text("""
        UPDATE accounts
        SET balance = balance - :amount
        WHERE id = :sender;
    """)
    
    update_receiver_query = text("""
        UPDATE accounts
        SET balance = balance + :amount
        WHERE id = :receiver;
    """)
    
    # Execute queries with dictionary parameters
    with engine.connect() as conn:
        conn.execute(update_sender_query, {'sender': p_sender, 'amount': p_amount})
        conn.execute(update_receiver_query, {'receiver': p_receiver, 'amount': p_amount})
        
        # Commit changes
        conn.commit()

    # No return statement needed, as the function only performs updates
