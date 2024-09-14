
from config import engine
import pandas as pd
from sqlalchemy import text

def transfer_funds(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    # Subtract the amount from the sender's account
    update_sender_query = text("""
        UPDATE accounts
        SET balance = balance - :p_amount
        WHERE id = :p_sender
    """)
    conn.execute(update_sender_query, {"p_sender": p_sender, "p_amount": p_amount})

    # Add the amount to the receiver's account
    update_receiver_query = text("""
        UPDATE accounts
        SET balance = balance + :p_amount
        WHERE id = :p_receiver
    """)
    conn.execute(update_receiver_query, {"p_receiver": p_receiver, "p_amount": p_amount})

    conn.commit()

    # No return value is expected, so we'll return None
    return None
