
import unittest
from your_module import transfer_balance  # Replace with the actual module name

class TestTransferBalance(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_positive_transfer(self):
        # Test a successful transfer
        p_sender = 1
        p_receiver = 2
        p_amount = 10
        initial_sender_balance = 100
        initial_receiver_balance = 50

        # Set up the initial balances
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {"id": p_sender, "balance": initial_sender_balance})
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {"id": p_receiver, "balance": initial_receiver_balance})
        self.conn.commit()

        # Perform the transfer
        transfer_balance(p_sender, p_receiver, p_amount)

        # Check the new balances
        sender_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {"id": p_sender}).fetchone()[0]
        receiver_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {"id": p_receiver}).fetchone()[0]

        self.assertEqual(sender_balance, initial_sender_balance - p_amount)
        self.assertEqual(receiver_balance, initial_receiver_balance + p_amount)

    def test_negative_transfer(self):
        # Test a transfer with a negative amount
        p_sender = 1
        p_receiver = 2
        p_amount = -10

        with self.assertRaises(psycopg2.Error):
            transfer_balance(p_sender, p_receiver, p_amount)

    def test_insufficient_balance(self):
        # Test a transfer where the sender doesn't have enough balance
        p_sender = 1
        p_receiver = 2
        p_amount = 100
        initial_sender_balance = 50

        # Set up the initial balance
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {"id": p_sender, "balance": initial_sender_balance})
        self.conn.commit()

        with self.assertRaises(psycopg2.Error):
            transfer_balance(p_sender, p_receiver, p_amount)

    def test_invalid_sender_id(self):
        # Test a transfer with an invalid sender ID
        p_sender = 999
        p_receiver = 2
        p_amount = 10

        with self.assertRaises(psycopg2.Error):
            transfer_balance(p_sender, p_receiver, p_amount)

    def test_invalid_receiver_id(self):
        # Test a transfer with an invalid receiver ID
        p_sender = 1
        p_receiver = 999
        p_amount = 10

        with self.assertRaises(psycopg2.Error):
            transfer_balance(p_sender, p_receiver, p_amount)

if __name__ == "__main__":
    unittest.main()
