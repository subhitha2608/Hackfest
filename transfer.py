
from config import engine
import pandas as pd
from sqlalchemy import text

def transfer_funds(p_sender, p_receiver, p_amount):
    # Create a connection object
    conn = engine.connect()

    try:
        # Subtract the amount from the sender's account
        update_sender_query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
        conn.execute(update_sender_query, {'amount': p_amount, 'sender': p_sender})

        # Add the amount to the receiver's account
        update_receiver_query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
        conn.execute(update_receiver_query, {'amount': p_amount, 'receiver': p_receiver})

        # Commit the changes
        conn.commit()

        # Return the updated balances
        query = text("SELECT balance FROM accounts WHERE id IN (:sender, :receiver)")
        result = conn.execute(query, {'sender': p_sender, 'receiver': p_receiver})
        balances = [dict(row) for row in result]

        return balances

    except Exception as e:
        # Rollback the changes if an error occurs
        conn.rollback()
        raise e

    finally:
        # Close the connection
        conn.close()
