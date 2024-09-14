
from config import engine
import pandas as pd
from sqlalchemy import text
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    try:
        # Subtract the amount from the sender's account
        update_sender_query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
        conn.execute(update_sender_query, {'amount': p_amount, 'sender': p_sender})

        # Add the amount to the receiver's account
        update_receiver_query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
        conn.execute(update_receiver_query, {'amount': p_amount, 'receiver': p_receiver})

        # Commit the changes
        conn.commit()

        # Return a success message (or the updated account balances if needed)
        return "Funds transferred successfully"
    except psycopg2.Error as e:
        # Rollback the changes if an error occurs
        conn.rollback()
        raise e
    finally:
        # Close the connection
        conn.close()
