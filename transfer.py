
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_amount, p_sender, p_receiver):
    conn = engine.connect()
    try:
        # Subtract the amount from the sender's account
        query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
        conn.execute(query, {'amount': p_amount, 'sender': p_sender})

        # Add the amount to the receiver's account
        query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
        conn.execute(query, {'amount': p_amount, 'receiver': p_receiver})

        conn.commit()
        
        # Return the updated account balances
        query = text("SELECT id, balance FROM accounts WHERE id IN (:sender, :receiver)")
        result = conn.execute(query, {'sender': p_sender, 'receiver': p_receiver})
        df = pd.DataFrame(result.fetchall(), columns=['id', 'balance'])
        return df
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()
