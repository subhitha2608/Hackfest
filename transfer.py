Python
from config import engine
import pandas as pd
from sqlalchemy import text
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    conn = engine.connect()
    
    # Subtract the amount from the sender's account
    query = text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender")
    conn.execute(query, {'p_sender': p_sender, 'p_amount': p_amount})
    conn.commit()

    # Add the amount to the receiver's account
    query = text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver")
    conn.execute(query, {'p_receiver': p_receiver, 'p_amount': p_amount})
    conn.commit()
    
    conn.close()

# Call the function
transfer_amount(1, 2, 100)

