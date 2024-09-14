
import unittest
from your_module import transfer_amount  # replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    def test_transfer_amount_same_accounts(self):
        sender_id = 1
        receiver_id = 1
        amount = 10
        initial_balance = 100
        
        # create a test account with initial balance
        with engine.connect() as connection:
            connection.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_balance, 'id': sender_id})
            connection.commit()
        
        transfer_amount(sender_id, receiver_id, amount)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': sender_id})
            balance = result.fetchone()[0]
            self.assertEqual(balance, initial_balance)  # balance should not change when sender and receiver are the same

    def test_transfer_amount_different_accounts(self):
        sender_id = 1
        receiver_id = 2
        amount = 10
        initial_sender_balance = 100
        initial_receiver_balance = 50
        
        # create test accounts with initial balances
        with engine.connect() as connection:
            connection.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_sender_balance, 'id': sender_id})
            connection.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_receiver_balance, 'id': receiver_id})
            connection.commit()
        
        transfer_amount(sender_id, receiver_id, amount)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': sender_id})
            sender_balance = result.fetchone()[0]
            result = connection.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': receiver_id})
            receiver_balance = result.fetchone()[0]
            self.assertEqual(sender_balance, initial_sender_balance - amount)  # sender's balance should decrease
            self.assertEqual(receiver_balance, initial_receiver_balance + amount)  # receiver's balance should increase

    def test_transfer_amount_insufficient_funds(self):
        sender_id = 1
        receiver_id = 2
        amount = 1000
        initial_sender_balance = 100
        
        # create a test account with initial balance
        with engine.connect() as connection:
            connection.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_sender_balance, 'id': sender_id})
            connection.commit()
        
        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)  # should raise an error since sender has insufficient funds
