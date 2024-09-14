Python
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(sender_id, receiver_id, amount):
    try:
        # Subtract the amount from the sender's account
        update_sender_query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender_id")
        update_sender_result = engine.execute(update_sender_query, {"amount": amount, "sender_id": sender_id})
        conn = engine.connect()
        conn.commit()

        # Add the amount to the receiver's account
        update_receiver_query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver_id")
        update_receiver_result = engine.execute(update_receiver_query, {"amount": amount, "receiver_id": receiver_id})
        conn.commit()

        # Update the accounts table
        update_accounts_query = text("SELECT * FROM accounts WHERE id = :sender_id OR id = :receiver_id")
        update_accounts_result = engine.execute(update_accounts_query, {"sender_id": sender_id, "receiver_id": receiver_id})
        result = update_accounts_result.fetchall()
        return result

    except (Exception, psycopg2.Error) as error:
        print("Failed to transfer amount: ", error)
