Python
from sqlalchemy import text
from config import engine
import pandas as pd

def transfer_funds(sender_id, receiver_id, p_amount):
    try:
        # Subtract the amount from the sender's account
        query = text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :sender_id")
        engine.execute(query, {"p_amount": p_amount, "sender_id": sender_id})

        # Add the amount to the receiver's account
        query = text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :receiver_id")
        engine.execute(query, {"p_amount": p_amount, "receiver_id": receiver_id})

        # Commit the changes
        engine.commit()
    except Exception as e:
        engine.rollback()
        raise e
