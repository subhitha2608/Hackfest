
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def transfer_balance(p_sender, p_receiver, p_amount):
    # Create a connection to the database
    conn = engine.connect()

    try:
        # Subtract the amount from the sender's account
        update_sender_query = sa.text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender
        """)
        conn.execute(update_sender_query, {"sender": p_sender, "amount": p_amount})

        # Add the amount to the receiver's account
        update_receiver_query = sa.text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver
        """)
        conn.execute(update_receiver_query, {"receiver": p_receiver, "amount": p_amount})

        # Commit the changes
        conn.execute("COMMIT")

        # Return the updated balances
        query = sa.text("SELECT balance FROM accounts WHERE id IN (:sender, :receiver)")
        result = conn.execute(query, {"sender": p_sender, "receiver": p_receiver})
        balances = [row[0] for row in result.fetchall()]
        return balances

    except psycopg2.Error as e:
        # Rollback the changes in case of an error
        conn.execute("ROLLBACK")
        raise e

    finally:
        # Close the connection
        conn.close()
