
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    try:
        # Subtract the amount from the sender's account
        update_sender_query = text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender
        """)
        conn.execute(update_sender_query, {'amount': p_amount, 'sender': p_sender})

        # Add the amount to the receiver's account
        update_receiver_query = text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver
        """)
        conn.execute(update_receiver_query, {'amount': p_amount, 'receiver': p_receiver})

        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

    return None
