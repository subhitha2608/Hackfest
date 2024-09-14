
from config import engine
import pandas as pd
from sqlalchemy import text

def transfer_funds(sender_id, receiver_id, amount):
    # Subtract the amount from the sender's account
    sender_query = text("""
        UPDATE accounts
        SET balance = balance - :amount
        WHERE id = :sender_id
    """)
    result = engine.execute(sender_query, {'sender_id': sender_id, 'amount': amount})
    sender_result = result.fetchall()

    # Add the amount to the receiver's account
    receiver_query = text("""
        UPDATE accounts
        SET balance = balance + :amount
        WHERE id = :receiver_id
    """)
    result = engine.execute(receiver_query, {'receiver_id': receiver_id, 'amount': amount})
    receiver_result = result.fetchall()

    # Commit the changes
    engine.execute("commit")

    return sender_result, receiver_result
