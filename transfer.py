
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()

    # Subtract the amount from the sender's account
    query = text("""UPDATE accounts
                    SET balance = balance - :p_amount
                    WHERE id = :p_sender""")
    conn.execute(query, {"p_amount": p_amount, "p_sender": p_sender})
    conn.commit()

    # Add the amount to the receiver's account
    query = text("""UPDATE accounts
                    SET balance = balance + :p_amount
                    WHERE id = :p_receiver""")
    conn.execute(query, {"p_amount": p_amount, "p_receiver": p_receiver})
    conn.commit()

    conn.close()
    return None
