
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    try:
        # Subtract the amount from the sender's account
        update_sender_query = sa.text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """)
        conn.execute(update_sender_query, {"p_sender": p_sender, "p_amount": p_amount})

        # Add the amount to the receiver's account
        update_receiver_query = sa.text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """)
        conn.execute(update_receiver_query, {"p_receiver": p_receiver, "p_amount": p_amount})

        # Commit changes
        conn.commit()

    except psycopg2.Error as e:
        # Rollback changes if an error occurs
        conn.rollback()
        raise e

    finally:
        # Close the database connection
        conn.close()

    return None
