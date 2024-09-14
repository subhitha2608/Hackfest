
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    # Subtract the amount from the sender's account
    update_sender_query = text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender")
    conn.execute(update_sender_query, {"p_amount": p_amount, "p_sender": p_sender})

    # Add the amount to the receiver's account
    update_receiver_query = text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver")
    conn.execute(update_receiver_query, {"p_amount": p_amount, "p_receiver": p_receiver})

    conn.commit()
    conn.close()

    # No return value is expected in this case, as the procedure only updates the accounts
    return None
