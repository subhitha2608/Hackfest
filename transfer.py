
from config import engine
import pandas as pd
from sqlalchemy import text
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    try:
        with engine.connect() as conn:
            # Subtract the amount from the sender's account
            update_sender = text("""
                UPDATE accounts
                SET balance = balance - :amount
                WHERE id = :sender
            """)
            conn.execute(update_sender, {'sender': p_sender, 'amount': p_amount})
            
            # Add the amount to the receiver's account
            update_receiver = text("""
                UPDATE accounts
                SET balance = balance + :amount
                WHERE id = :receiver
            """)
            conn.execute(update_receiver, {'receiver': p_receiver, 'amount': p_amount})
            
            conn.commit()
            
            # Return the updated balances as a pandas DataFrame
            query = text("""
                SELECT id, balance
                FROM accounts
                WHERE id IN (:sender, :receiver)
            """)
            result = conn.execute(query, {'sender': p_sender, 'receiver': p_receiver})
            df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.cursor.description])
            return df
    
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return None
