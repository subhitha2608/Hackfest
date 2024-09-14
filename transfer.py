
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    # Define the update queries
    update_sender_query = sa.text("""
        UPDATE accounts
        SET balance = balance - :amount
        WHERE id = :sender;
    """)

    update_receiver_query = sa.text("""
        UPDATE accounts
        SET balance = :amount + balance
        WHERE id = :receiver;
    """)

    # Execute the queries
    with engine.connect() as conn:
        conn.execute(update_sender_query, {'sender': p_sender, 'amount': p_amount})
        conn.execute(update_receiver_query, {'receiver': p_receiver, 'amount': p_amount})
        conn.commit()

    # No return value, as the procedure only performs updates
    return None
