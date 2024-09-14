
import unittest
from your_module import transfer_amount  # Replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()
        # Create test accounts with initial balances
        self.conn.execute(text("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)"))
        self.conn.commit()

    def tearDown(self):
        # Rollback any changes made during the test
        self.conn.rollback()
        # Close the database connection
        self.conn.close()

    def test_transfer_amount_positive(self):
        # Test a successful transfer
        transfer_amount(1, 2, 20)
        # Check the updated balances
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 1")).fetchone()[0]
        self.assertEqual(result, 80)
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 2")).fetchone()[0]
        self.assertEqual(result, 70)

    def test_transfer_amount_negative_insufficient_funds(self):
        # Test a transfer with insufficient funds
        with self.assertRaises(Exception):
            transfer_amount(1, 2, 150)
        # Check that the balances remain unchanged
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 1")).fetchone()[0]
        self.assertEqual(result, 100)
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 2")).fetchone()[0]
        self.assertEqual(result, 50)

    def test_transfer_amount_negative_invalid_sender(self):
        # Test a transfer with an invalid sender
        with self.assertRaises(Exception):
            transfer_amount(3, 2, 20)
        # Check that the balances remain unchanged
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 1")).fetchone()[0]
        self.assertEqual(result, 100)
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 2")).fetchone()[0]
        self.assertEqual(result, 50)

    def test_transfer_amount_negative_invalid_receiver(self):
        # Test a transfer with an invalid receiver
        with self.assertRaises(Exception):
            transfer_amount(1, 3, 20)
        # Check that the balances remain unchanged
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 1")).fetchone()[0]
        self.assertEqual(result, 100)
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 2")).fetchone()[0]
        self.assertEqual(result, 50)

    def test_transfer_amount_negative_zero_amount(self):
        # Test a transfer with a zero amount
        with self.assertRaises(Exception):
            transfer_amount(1, 2, 0)
        # Check that the balances remain unchanged
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 1")).fetchone()[0]
        self.assertEqual(result, 100)
        result = self.conn.execute(text("SELECT balance FROM accounts WHERE id = 2")).fetchone()[0]
        self.assertEqual(result, 50)

if __name__ == '__main__':
    unittest.main()
