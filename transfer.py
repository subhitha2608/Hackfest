Python
from config import engine
import pandas as pd
from sqlalchemy import text

def wallet_transfer(p_sender, p_receiver, p_amount):
    try:
        # Subtract the amount from the sender's account
        update_sender = text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender;
        """)
        engine.execute(update_sender, {"p_sender": p_sender, "p_amount": p_amount})

        # Add the amount to the receiver's account
        update_receiver = text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver;
        """)
        engine.execute(update_receiver, {"p_receiver": p_receiver, "p_amount": p_amount})

        engine.commit()
        return "Transfer successful"
    except Exception as e:
        engine.rollback()
        return str(e)

# test the function
wallet_transfer(1, 2, 100)
