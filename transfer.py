
from config import engine
from sqlalchemy import text
import pandas as pd

def transfer(p_sender, p_receiver, p_amount):
    # Subtract the amount from the sender's account
    update_sender = text("""
        UPDATE accounts
        SET balance = balance - :p_amount
        WHERE id = :p_sender
    """)
    params = {'p_sender': p_sender, 'p_amount': p_amount}
    conn = engine.connect()
    conn.execute(update_sender, params)
    conn.commit()

    # Add the amount to the receiver's account
    update_receiver = text("""
        UPDATE accounts
        SET balance = balance + :p_amount
        WHERE id = :p_receiver
    """)
    params = {'p_receiver': p_receiver, 'p_amount': p_amount}
    conn.execute(update_receiver, params)
    conn.commit()

    # Execute the query to get the final balance of accounts
    get_balance = text("""
        SELECT id, balance
        FROM accounts
        WHERE id = :p_sender
    """)
    params = {'p_sender': p_sender}
    result = conn.execute(get_sender_balance, params)
    sender_balance = result.fetchone()
    
    get_balance = text("""
        SELECT id, balance
        FROM accounts
        WHERE id = :p_receiver
    """)
    params = {'p_receiver': p_receiver}
    result = conn.execute(get_balance, params)
    receiver_balance = result.fetchone()
    
    return sender_balance, receiver_balance
