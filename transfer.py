
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(sender_id, receiver_id, amount):
    # Subtract the amount from the sender's account
    update_sender_query = text("""
        UPDATE accounts
        SET balance = balance - :amount
        WHERE id = :sender_id
    """)
    engine.execute(update_sender_query, {"sender_id": sender_id, "amount": amount})

    # Add the amount to the receiver's account
    update_receiver_query = text("""
        UPDATE accounts
        SET balance = balance + :amount
        WHERE id = :receiver_id
    """)
    engine.execute(update_receiver_query, {"receiver_id": receiver_id, "amount": amount})

    # Commit the changes
    engine.execute("COMMIT")
