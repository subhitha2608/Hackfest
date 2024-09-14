
import unittest
from your_module import transfer_balance  # Replace 'your_module' with the actual module name

class TestTransferBalance(unittest.TestCase):

    def setUp(self):
        # Create test data in the database
        conn = engine.connect()
        conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")
        conn.commit()
        conn.close()

    def tearDown(self):
        # Clean up test data in the database
        conn = engine.connect()
        conn.execute("DELETE FROM accounts")
        conn.commit()
        conn.close()

    def test_transfer_balance_positive(self):
        # Test a valid transfer
        transfer_balance(1, 2, 20)
        conn = engine.connect()
        result = conn.execute("SELECT balance FROM accounts WHERE id = 1")
        self.assertEqual(result.scalar(), 80)
        result = conn.execute("SELECT balance FROM accounts WHERE id = 2")
        self.assertEqual(result.scalar(), 70)
        conn.close()

    def test_transfer_balance_insufficient_funds(self):
        # Test a transfer with insufficient funds
        with self.assertRaises(Exception):
            transfer_balance(2, 1, 60)  # Receiver has insufficient funds
        conn = engine.connect()
        result = conn.execute("SELECT balance FROM accounts WHERE id = 1")
        self.assertEqual(result.scalar(), 100)
        result = conn.execute("SELECT balance FROM accounts WHERE id = 2")
        self.assertEqual(result.scalar(), 50)
        conn.close()

    def test_transfer_balance_invalid_sender(self):
        # Test a transfer with an invalid sender
        with self.assertRaises(Exception):
            transfer_balance(3, 2, 20)  # Sender does not exist
        conn = engine.connect()
        result = conn.execute("SELECT balance FROM accounts WHERE id = 1")
        self.assertEqual(result.scalar(), 100)
        result = conn.execute("SELECT balance FROM accounts WHERE id = 2")
        self.assertEqual(result.scalar(), 50)
        conn.close()

    def test_transfer_balance_invalid_receiver(self):
        # Test a transfer with an invalid receiver
        with self.assertRaises(Exception):
            transfer_balance(1, 3, 20)  # Receiver does not exist
        conn = engine.connect()
        result = conn.execute("SELECT balance FROM accounts WHERE id = 1")
        self.assertEqual(result.scalar(), 100)
        result = conn.execute("SELECT balance FROM accounts WHERE id = 2")
        self.assertEqual(result.scalar(), 50)
        conn.close()

    def test_transfer_balance_non_positive_amount(self):
        # Test a transfer with a non-positive amount
        with self.assertRaises(Exception):
            transfer_balance(1, 2, 0)  # Amount is zero
        conn = engine.connect()
        result = conn.execute("SELECT balance FROM accounts WHERE id = 1")
        self.assertEqual(result.scalar(), 100)
        result = conn.execute("SELECT balance FROM accounts WHERE id = 2")
        self.assertEqual(result.scalar(), 50)
        conn.close()

if __name__ == '__main__':
    unittest.main()
