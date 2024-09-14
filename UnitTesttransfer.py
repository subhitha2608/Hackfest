
import unittest
from your_module import transfer_funds
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

class TestTransferFunds(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()
        self.conn.execute("CREATE TABLE accounts (id SERIAL PRIMARY KEY, balance INTEGER)")
        self.conn.execute("INSERT INTO accounts (balance) VALUES (100), (200)")

    def tearDown(self):
        self.conn.execute("DROP TABLE accounts")
        self.conn.close()

    def test_transfer_funds_positive_amount(self):
        result = transfer_funds(1, 2, 50)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.loc[result['id'] == 1, 'balance'].values[0], 50)
        self.assertEqual(result.loc[result['id'] == 2, 'balance'].values[0], 250)

    def test_transfer_funds_zero_amount(self):
        result = transfer_funds(1, 2, 0)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.loc[result['id'] == 1, 'balance'].values[0], 100)
        self.assertEqual(result.loc[result['id'] == 2, 'balance'].values[0], 200)

    def test_transfer_funds_negative_amount(self):
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, -50)

    def test_transfer_funds_sender_not_exists(self):
        with self.assertRaises(psycopg2.Error):
            transfer_funds(3, 2, 50)

    def test_transfer_funds_receiver_not_exists(self):
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 3, 50)

if __name__ == '__main__':
    unittest.main()
