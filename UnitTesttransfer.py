
import unittest
from your_module import transfer_funds
from sqlalchemy import create_engine
import pandas as pd
import psycopg2

class TestTransferFunds(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('postgresql://user:password@localhost/dbname')
        self.conn = self.engine.connect()

    def test_transfer_funds_positive(self):
        # setup sample data
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # test function
        result = transfer_funds(1, 2, 20)

        # assertions
        self.assertEqual(result, "Funds transferred successfully")
        sender_balance = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0]
        receiver_balance = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()[0]
        self.assertEqual(sender_balance, 80)
        self.assertEqual(receiver_balance, 70)

    def test_transfer_funds_insufficient_balance(self):
        # setup sample data
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 50)")

        # test function
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 150)

    def test_transfer_funds_receiver_not_found(self):
        # setup sample data
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (1, 100)")

        # test function
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 3, 20)

    def test_transfer_funds_sender_not_found(self):
        # setup sample data
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (2, 50)")

        # test function
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 20)

    def tearDown(self):
        self.conn.execute("DELETE FROM accounts")
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
