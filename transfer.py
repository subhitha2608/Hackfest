
from config import engine
import pandas as pd
from sqlalchemy import text

def transfer_funds(p_sender, p_receiver, p_amount):
    # Subtract the amount from the sender's account
    update_sender = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
    result = engine.execute(update_sender, {'sender': p_sender, 'amount': p_amount})
    conn = engine.connect()
    conn.execute("commit")
    
    # Add the amount to the receiver's account
    update_receiver = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
    result = engine.execute(update_receiver, {'receiver': p_receiver, 'amount': p_amount})
    conn.execute("commit")

    # Query the updated balances
    query = text("SELECT * FROM accounts WHERE id = :sender OR id = :receiver")
    result = engine.execute(query, {'sender': p_sender, 'receiver': p_receiver})
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=[c.key for c in result.keys()])
    
    return df
