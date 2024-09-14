Python
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
import pandas as pd

def transfer_amount(p_sender, p_receiver, p_amount):
    engine = create_engine('postgresql://user:password@localhost/dbname')
    conn = engine.connect()
    
    # Create a DDL command if needed
    #cursor.execute('CREATE TABLE IF NOT EXISTS accounts (id INT, balance FLOAT);')
    
    try:
        # Execute the SQL query with parameters
        result = conn.execute(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender").execute(), {"p_sender": p_sender, "p_amount": p_amount})
        # Save the new data
        conn.commit()
        
        # Execute the SQL query with parameters again
        result = conn.execute(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver").execute(), {"p_receiver": p_receiver, "p_amount": p_amount})
        # Save the new data
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
    finally:
        conn.close()
        engine.dispose()

# Example usage:
transfer_amount(1, 2, 100.0)
