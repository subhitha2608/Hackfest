
import unittest
from your_module import transfer_funds  # Replace with the actual module name

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()
        self.conn.execute("CREATE TABLE accounts (id SERIAL PRIMARY KEY, balance DECIMAL(10, 2))")

        # Insert some test data
        self.conn.execute("INSERT INTO accounts (balance) VALUES (100.00), (200.00)")
        self.conn.commit()

    def tearDown(self):
        # Drop the test table and close the connection
        self.conn.execute("DROP TABLE accounts")
        self.conn.close()

    def test_transfer_funds_positive(self):
        # Test a successful transfer
        sender_id = 1
        receiver_id = 2
        amount = 50.00
        transfer_funds(sender_id, receiver_id, amount)
        self.conn.commit()

        # Check the balances
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1")
        self.assertEqual(result.scalar(), 50.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2")
        self.assertEqual(result.scalar(), 250.00)

    def test_transfer_funds_negative_sender(self):
        # Test a transfer with a non-existent sender
        sender_id = 3
        receiver_id = 2
        amount = 50.00
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

    def test_transfer_funds_negative_receiver(self):
        # Test a transfer with a non-existent receiver
        sender_id = 1
        receiver_id = 3
        amount = 50.00
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

    def test_transfer_funds_negative_amount(self):
        # Test a transfer with a negative amount
        sender_id = 1
        receiver_id = 2
        amount = -50.00
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

    def test_transfer_funds_insufficient_funds(self):
        # Test a transfer with insufficient funds
        sender_id = 1
        receiver_id = 2
        amount = 150.00
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

if __name__ == '__main__':
    unittest.main()
