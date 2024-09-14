Python
from config import engine
import pandas as pd

def transfer_amount(sender, receiver, amount):
    update_account = text("""
        UPDATE accounts SET balance = balance - :amount WHERE id = :sender;
        UPDATE accounts SET balance = balance + :amount WHERE id = :receiver;
    """)
    conn = engine.connect()
    conn.execute(update_account, {'sender': sender, 'receiver': receiver, 'amount': amount})
    conn.commit()
    conn.close()
Python
import pandas as pd

df = pd.read_sql_query("SELECT * FROM accounts", engine)
# Perform data transformations on df
update_account = text("""
    UPDATE accounts SET balance = balance - :amount WHERE id = :sender;
    UPDATE accounts SET balance = balance + :amount WHERE id = :receiver;
""")
conn = engine.connect()
conn.execute(update_account, {'sender': sender, 'receiver': receiver, 'amount': amount})
conn.commit()
conn.close()
