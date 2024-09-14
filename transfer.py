
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    with engine.connect() as conn:
        # Subtract the amount from the sender's account
        update_sender_query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
        conn.execute(update_sender_query, {"amount": p_amount, "sender": p_sender})

        # Add the amount to the receiver's account
        update_receiver_query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
        conn.execute(update_receiver_query, {"amount": p_amount, "receiver": p_receiver})

        # Commit the changes
        conn.commit()

    # No explicit return statement, as the function doesn't need to return a value
