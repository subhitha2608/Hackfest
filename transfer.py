Python
from config import engine
from sqlalchemy import text
import pandas as pd

def transfer_money(sender_id, receiver_id, amount):
    conn = engine.connect()
    
    # Subtract the amount from the sender's account
    query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
    conn.execute(query, {'sender': sender_id, 'amount': amount})
    
    # Add the amount to the receiver's account
    query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
    conn.execute(query, {'receiver': receiver_id, 'amount': amount})
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    conn.close()
