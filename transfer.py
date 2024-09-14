Python
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def process_payment(p_sender, p_receiver, p_amount):
    try:
        conn = engine.connect()

        # Subtract the amount from the sender's account
        update_sender_query = text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """)
        conn.execute(update_sender_query, {'p_sender': p_sender, 'p_amount': p_amount})

        # Add the amount to the receiver's account
        update_receiver_query = text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """)
        conn.execute(update_receiver_query, {'p_receiver': p_receiver, 'p_amount': p_amount})

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if 'conn' in locals():
            conn.close()

    # Successful execution
    return "Payment processed successfully"
