
import unittest
from your_module import transfer_funds  # Import the function to be tested
import pandas as pd

class TestTransferFunds(unittest.TestCase):
    def test_transfer_funds_success(self):
        # Setup: Create a test database connection
        conn = engine.connect()

        # Execute the function to be tested
        transfer_funds(1, 2, 10.0)

        # Query the database to verify the results
        query = "SELECT balance FROM accounts WHERE id = 1"
        sender_balance = pd.read_sql(query, conn)['balance'][0]
        self.assertEquals(sender_balance, 90.0)  # Assume initial balance was 100.0

        conn.close()

    def test_transfer_funds_insufficient_funds(self):
        # Setup: Create a test database connection
        conn = engine.connect()

        # Execute the function to be tested with insufficient funds
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 150.0)

        # Query the database to verify the results
        query = "SELECT balance FROM accounts WHERE id = 1"
        sender_balance = pd.read_sql(query, conn)['balance'][0]
        self.assertEquals(sender_balance, 100.0)  # Balance should not have changed

        conn.close()

    def test_transfer_funds_invalid_receiver_id(self):
        # Setup: Create a test database connection
        conn = engine.connect()

        # Execute the function to be tested with an invalid receiver ID
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 999, 10.0)

        # Query the database to verify the results
        query = "SELECT balance FROM accounts WHERE id = 1"
        sender_balance = pd.read_sql(query, conn)['balance'][0]
        self.assertEquals(sender_balance, 100.0)  # Balance should not have changed

        conn.close()

if __name__ == '__main__':
    unittest.main()
