
from config import engine
from sqlalchemy import text, exc
import pandas as pd
import psycopg2

def transfer_amount(p_sender, p_receiver, p_amount):
    try:
        # Subtract the amount from the sender's account
        sender_update = text("""
        UPDATE accounts
        SET balance = balance - :p_amount
        WHERE id = :p_sender;
        """)
        engine.execute(sender_update, {'p_sender': p_sender, 'p_amount': p_amount})

        # Add the amount to the receiver's account
        receiver_update = text("""
        UPDATE accounts
        SET balance = balance + :p_amount
        WHERE id = :p_receiver;
        """)
        engine.execute(receiver_update, {'p_receiver': p_receiver, 'p_amount': p_amount})

        # Commit changes
        engine.execute('COMMIT;')

        return "Amount transferred successfully"
    except psycopg2.Error as e:
        # Roll back changes on error
        engine.execute('ROLLBACK;')
        return str(e)
    except exc.IntegrityError as e:
        # Roll back changes on error
        engine.execute('ROLLBACK;')
        return str(e)
    except Exception as e:
        # Roll back changes on error
        engine.execute('ROLLBACK;')
        return str(e)
