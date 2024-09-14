
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    try:
        # Subtract the amount from the sender's account
        update_sender_query = text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender")
        conn.execute(update_sender_query, {'p_sender': p_sender, 'p_amount': p_amount})

        # Add the amount to the receiver's account
        update_receiver_query = text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver")
        conn.execute(update_receiver_query, {'p_receiver': p_receiver, 'p_amount': p_amount})

        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

    return None
