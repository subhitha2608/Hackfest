
import unittest
from your_module import transfer_funds  # replace with the actual module name

class TestTransferFunds(unittest.TestCase):
    def test_transfer_funds_valid(self):
        # Setup initial balances for testing
        conn = engine.connect()
        conn.execute(text("UPDATE accounts SET balance = 100 WHERE id = 1"))
        conn.execute(text("UPDATE accounts SET balance = 50 WHERE id = 2"))
        conn.commit()
        conn.close()

        # Call the function to transfer funds
        transfer_funds(1, 2, 20)

        # Check the updated balances
        conn = engine.connect()
        sender_balance = conn.execute(text("SELECT balance FROM accounts WHERE id = 1")).scalar()
        receiver_balance = conn.execute(text("SELECT balance FROM accounts WHERE id = 2")).scalar()
        conn.close()

        self.assertEqual(sender_balance, 80)  # only one assertion per test
        # Alternatively, you can assert both balances in one line:
        # self.assertEqual((sender_balance, receiver_balance), (80, 70))

    def test_transfer_funds_insufficient_funds(self):
        # Setup initial balances for testing
        conn = engine.connect()
        conn.execute(text("UPDATE accounts SET balance = 50 WHERE id = 1"))
        conn.execute(text("UPDATE accounts SET balance = 50 WHERE id = 2"))
        conn.commit()
        conn.close()

        # Call the function to transfer funds
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 100)

    def test_transfer_funds_invalid_sender(self):
        # Call the function to transfer funds with an invalid sender
        with self.assertRaises(psycopg2.Error):
            transfer_funds(999, 2, 20)

if __name__ == '__main__':
    unittest.main()
