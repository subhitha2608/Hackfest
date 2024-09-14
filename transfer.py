
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    trans = conn.begin()

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

        trans.commit()
    except psycopg2.Error as e:
        trans.rollback()
        raise e
    finally:
        conn.close()

    return None  # or return a success message if needed
