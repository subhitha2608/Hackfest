py
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    try:
        # Subtract the amount from the sender's account
        conn = engine.connect()
        result = conn.execute(text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender_id"), sender_id=p_sender, amount=p_amount)
        conn.commit()

        # Add the amount to the receiver's account
        result = conn.execute(text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver_id"), receiver_id=p_receiver, amount=p_amount)
        conn.commit()
        
        # Ensure all operation are done
        conn.close()
        return f"Amount {p_amount} transferred successfully from {p_sender} to {p_receiver}"
    except (psycopg2.Error, Exception) as e:
        print(f"An error occurred: {e}")
        return f"Error transferring amount: {e}"

# Example usage
print(transfer_amount(1, 2, 100))
