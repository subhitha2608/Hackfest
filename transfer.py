Python
from config import engine
import pandas as pd
from sqlalchemy import text
import psycopg2

def transaction(p_sender, p_receiver, p_amount):
    try:
        conn = engine.connect()
        query = text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender")
        conn.execute(query, {"sender": p_sender, "amount": p_amount})
        conn.commit()
        
        query = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver")
        conn.execute(query, {"receiver": p_receiver, "amount": p_amount})
        conn.commit()
        
        # If you need the updated balances
        query = text("SELECT * FROM accounts WHERE id = :sender OR id = :receiver")
        result = conn.execute(query, {"sender": p_sender, "receiver": p_receiver}).fetchall()
        conn.commit()
        
        conn.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

result = transaction(1, 2, 100.0)
