
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_balance(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    # Subtract the amount from the sender's account
    query = text("""
        UPDATE accounts
        SET balance = balance - :amount
        WHERE id = :sender;
    """)
    conn.execute(query, {'amount': p_amount, 'sender': p_sender})

    # Add the amount to the receiver's account
    query = text("""
        UPDATE accounts
        SET balance = balance + :amount
        WHERE id = :receiver;
    """)
    conn.execute(query, {'amount': p_amount, 'receiver': p_receiver})

    conn.commit()

    # Return the updated balances
    query = text("""
        SELECT balance
        FROM accounts
        WHERE id IN (:sender, :receiver);
    """)
    result = conn.execute(query, {'sender': p_sender, 'receiver': p_receiver})
    balances = [row[0] for row in result]
    conn.close()

    return balances
