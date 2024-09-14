
import unittest
from your_module import transfer_funds  # Replace 'your_module' with the actual module name
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Rollback any changes and close the connection
        self.conn.rollback()
        self.conn.close()

    def test_transfer_funds SuccessfulTransfer(self):
        # Create test accounts with initial balances
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # Transfer 20 from account 1 to account 2
        transfer_funds(1, 2, 20)

        # Check the updated balances
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        self.assertEqual(result[0], 80)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()
        self.assertEqual(result[0], 70)

    def test_transfer_funds_InsufficientBalance(self):
        # Create test accounts with initial balances
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # Try to transfer 150 from account 1 to account 2 (should raise an error)
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 150)

        # Check that the balances remain unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        self.assertEqual(result[0], 100)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()
        self.assertEqual(result[0], 50)

    def test_transfer_funds_NegativeAmount(self):
        # Create test accounts with initial balances
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # Try to transfer -20 from account 1 to account 2 (should raise an error)
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, -20)

        # Check that the balances remain unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        self.assertEqual(result[0], 100)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()
        self.assertEqual(result[0], 50)

    def test_transfer_funds_NonExistingSender(self):
        # Create test accounts with initial balances
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # Try to transfer 20 from non-existing account 3 to account 2 (should raise an error)
        with self.assertRaises(psycopg2.Error):
            transfer_funds(3, 2, 20)

        # Check that the balances remain unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        self.assertEqual(result[0], 100)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()
        self.assertEqual(result[0], 50)

    def test_transfer_funds_NonExistingReceiver(self):
        # Create test accounts with initial balances
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # Try to transfer 20 from account 1 to non-existing account 3 (should raise an error)
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 3, 20)

        # Check that the balances remain unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        self.assertEqual(result[0], 100)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()
        self.assertEqual(result[0], 50)

if __name__ == '__main__':
    unittest.main()
