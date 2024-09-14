
from config import engine
import pandas as pd

def transfer_funds(sender_id, receiver_id, amount):
    # Subtract the amount from the sender's account
    update_sender = text("""
        UPDATE accounts
        SET balance = balance - :amount
        WHERE id = :sender_id;
    """)
    update_sender_params = {"sender_id": sender_id, "amount": amount}
    engine.execute(update_sender, **update_sender_params)

    # Add the amount to the receiver's account
    update_receiver = text("""
        UPDATE accounts
        SET balance = balance + :amount
        WHERE id = :receiver_id;
    """)
    update_receiver_params = {"receiver_id": receiver_id, "amount": amount}
    engine.execute(update_receiver, **update_receiver_params)

    # Commit the changes
    engine.commit()
    return None
