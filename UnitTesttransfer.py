
import unittest
from your_module import transfer_funds
import pandas as pd

class TestTransferFunds(unittest.TestCase):

    def test_transfer_funds_valid_input(self):
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (1, 1000)"))
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (2, 0)"))
        transfer_funds(1, 2, 500)
        query = text("SELECT balance FROM accounts WHERE id = 1")
        result = engine.execute(query).fetchone()[0]
        self.assertEqual(result, 500)
        query = text("SELECT balance FROM accounts WHERE id = 2")
        result = engine.execute(query).fetchone()[0]
        self.assertEqual(result, 500)
        engine.execute(text("DELETE FROM accounts"))

    def test_transfer_funds_invalid_sender_id(self):
        with self.assertRaises(Exception):
            transfer_funds(0, 2, 500)

    def test_transfer_funds_invalid_receiver_id(self):
        with self.assertRaises(Exception):
            transfer_funds(1, 0, 500)

    def test_transfer_funds_amount_zero(self):
        with self.assertRaises(ZeroDivisionError):
            transfer_funds(1, 2, 0)

    def test_transfer_funds_negative_amount(self):
        try:
            transfer_funds(1, 2, -500)
            self.fail("Expected exception")
        except Exception as e:
            self.assertEqual(str(e), "transfer amount cannot be negative")

    def test_transfer_funds_insufficient_funds(self):
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (1, 100)"))
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (2, 0)"))
        with self.assertRaises(Exception):
            transfer_funds(1, 2, 200)
        query = text("SELECT balance FROM accounts WHERE id = 1")
        result = engine.execute(query).fetchone()[0]
        self.assertEqual(result, 100)
        query = text("SELECT balance FROM accounts WHERE id = 2")
        result = engine.execute(query).fetchone()[0]
        self.assertEqual(result, 0)

    def test_transfer_funds_connection_error(self):
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (1, 100)"))
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (2, 0)"))
        try:
            transfer_funds(1, 2, 500)
        except Exception as e:
            self.assertEqual(str(e), "connection failed")
        query = text("SELECT balance FROM accounts WHERE id = 1")
        result = engine.execute(query).fetchone()[0]
        self.assertEqual(result, 100)
        query = text("SELECT balance FROM accounts WHERE id = 2")
        result = engine.execute(query).fetchone()[0]
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
