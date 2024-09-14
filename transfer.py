Python
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(sender_id, receiver_id, amount):
    # Subtract the amount from the sender's account
    update_sender = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender_id")
    result = engine.execute(update_sender, {"sender_id": sender_id, "amount": amount})
    conn = engine.connect()
    conn.commit()
    
    # Add the amount to the receiver's account
    update_receiver = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver_id")
    result = engine.execute(update_receiver, {"receiver_id": receiver_id, "amount": amount})
    conn.commit()
    
    return result.fetchall()
