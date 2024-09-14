
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    try:
        # Subtract the amount from the sender's account
        update_sender = text("""UPDATE accounts
                                SET balance = balance - :p_amount
                                WHERE id = :p_sender""")
        result_sender = engine.execute(update_sender, p_sender=p_sender, p_amount=p_amount)
        conn = engine.connect()
        conn.commit()

        # Add the amount to the receiver's account
        update_receiver = text("""UPDATE accounts
                                 SET balance = balance + :p_amount
                                 WHERE id = :p_receiver""")
        result_receiver = engine.execute(update_receiver, p_receiver=p_receiver, p_amount=p_amount)
        conn.commit()

        # Get the updated balances
        get_balances = text("SELECT * FROM accounts")
        result_balances = engine.execute(get_balances).fetchall()

        df_balances = pd.DataFrame(result_balances, columns=['id', 'balance'])
        df_balances = df_balances.sort_values(by='id')

        return result_balances

    except Exception as e:
        print(f"Error: {e}")
        return None

transfer_amount(sender, receiver, amount)
