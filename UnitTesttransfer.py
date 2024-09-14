
import unittest
from your_module import transfer_amount

class TestTransferAmount(unittest.TestCase):

    def setUp(self):
        self.engine = your_engine_object  # replace with your actual engine object
        self.p_sender = 1
        self.p_receiver = 2
        self.p_amount = 100
        self.query = text("""
        UPDATE accounts
        SET balance = balance + 0
        WHERE id = :p_sender;
        """)
        result = self.engine.execute(self.query, p_sender=self.p_sender, p_amount=0)
        self.query = text("""
        UPDATE accounts
        SET balance = balance + 0
        WHERE id = :p_receiver;
        """)
        result = self.engine.execute(self.query, p_receiver=self.p_receiver, p_amount=0)
        conn = self.engine.connect()
        conn.commit()

    def test_transfer_amount_positive(self):
        transfer_amount(self.p_sender, self.p_receiver, self.p_amount)
        query = text("""
        SELECT balance FROM accounts WHERE id = :p_sender;
        """)
        result = self.engine.execute(query, p_sender=self.p_sender)
        sender_balance = result.fetchone()[0]
        self.assertEqual(sender_balance, 0)
        query = text("""
        SELECT balance FROM accounts WHERE id = :p_receiver;
        """)
        result = self.engine.execute(query, p_receiver=self.p_receiver)
        receiver_balance = result.fetchone()[0]
        self.assertEqual(receiver_balance, self.p_amount)
        conn = self.engine.connect()
        conn.commit()

    def test_transfer_amount_negative(self):
        with self.assertRaises(ValueError):
            transfer_amount(self.p_sender, self.p_receiver, -self.p_amount)

    def test_transfer_amount_zero(self):
        transfer_amount(self.p_sender, self.p_receiver, 0)
        query = text("""
        SELECT balance FROM accounts WHERE id = :p_sender;
        """)
        result = self.engine.execute(query, p_sender=self.p_sender)
        sender_balance = result.fetchone()[0]
        self.assertEqual(sender_balance, 0)
        query = text("""
        SELECT balance FROM accounts WHERE id = :p_receiver;
        """)
        result = self.engine.execute(query, p_receiver=self.p_receiver)
        receiver_balance = result.fetchone()[0]
        self.assertEqual(receiver_balance, 0)
        conn = self.engine.connect()
        conn.commit()

    def test_transfer_amount_sender(self):
        with self.assertRaises(ValueError):
            transfer_amount(3, self.p_receiver, self.p_amount)

    def test_transfer_amount_receiver(self):
        with self.assertRaises(ValueError):
            transfer_amount(self.p_sender, 3, self.p_amount)

    def test_transfer_amount_to_self(self):
        with self.assertRaises(ValueError):
            transfer_amount(self.p_sender, self.p_sender, self.p_amount)

if __name__ == '__main__':
    unittest.main()
