
import unittest
from your_module import transfer_funds  # Import the function to be tested
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()
        
        # Create a test table
        self.conn.execute('CREATE TABLE accounts (id SERIAL PRIMARY KEY, balance INTEGER)')
        
        # Insert some test data
        self.conn.execute('INSERT INTO accounts (balance) VALUES (100), (200)')

    def tearDown(self):
        # Drop the test table and close the connection
        self.conn.execute('DROP TABLE accounts')
        self.conn.close()

    def test_transfer_funds_positive(self):
        # Test a successful transfer
        transfer_funds(1, 2, 50)
        result = self.conn.execute('SELECT balance FROM accounts WHERE id = 1').fetchone()
        self.assertEqual(result[0], 50)
        result = self.conn.execute('SELECT balance FROM accounts WHERE id = 2').fetchone()
        self.assertEqual(result[0], 250)

    def test_transfer_funds_negative_insufficient_funds(self):
        # Test a transfer with insufficient funds
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 150)

    def test_transfer_funds_negative_invalid_sender(self):
        # Test a transfer with an invalid sender
        with self.assertRaises(psycopg2.Error):
            transfer_funds(3, 2, 50)

    def test_transfer_funds_negative_invalid_receiver(self):
        # Test a transfer with an invalid receiver
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 3, 50)

    def test_transfer_funds_negative_zero_amount(self):
        # Test a transfer with a zero amount
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 0)

    def test_transfer_funds_negative_negative_amount(self):
        # Test a transfer with a negative amount
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, -50)

if __name__ == '__main__':
    unittest.main()
