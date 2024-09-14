
import unittest
from your_file import process_payment

class TestProcessPayment(unittest.TestCase):
    def setUp(self):
        self.p_sender = 1
        self.p_receiver = 2
        self.p_amount = 10

    def test_success(self):
        result = process_payment(self.p_sender, self.p_receiver, self.p_amount)
        assert result == "Payment processed successfully"

    def test_sender_account_not_found(self):
        result = process_payment(3, self.p_receiver, self.p_amount)
        assert result == "Payment processed successfully"

    def test_receiver_account_not_found(self):
        result = process_payment(self.p_sender, 3, self.p_amount)
        assert result == "Payment processed successfully"

    def test_offset_amount_from_sender_account(self):
        old_balance = 100
        accounts = {'id': self.p_sender, 'balance': old_balance}
        self.assertEqual(process_payment(self.p_sender, self.p_receiver, old_balance), "Payment processed successfully")
        new_balance = accounts['balance']
        self.assertEqual(new_balance, 0)

    def test_add_amount_to_receiver_account(self):
        old_balance = 0
        accounts = {'id': self.p_receiver, 'balance': old_balance}
        self.assertEqual(process_payment(self.p_sender, self.p_receiver, self.p_amount), "Payment processed successfully")
        new_balance = accounts['balance']
        self.assertEqual(new_balance, self.p_amount)

    def test_psb_connection_error(self):
        import unittest.mock
        with unittest.mock.patch('your_file.engine') as engine:
            engine.connect.side_effect = psycopg2.Error('Connection failed')
            with self.assertRaises(psycopg2.Error):
                process_payment(self.p_sender, self.p_receiver, self.p_amount)

    def test_psb_query_error(self):
        import unittest.mock
        with unittest.mock.patch('your_file.engine') as engine:
            engine.connect.return_value = unittest.mock.Mock()
            engine.connect().execute.side_effect = psycopg2.Error('Query failed')
            with self.assertRaises(psycopg2.Error):
                process_payment(self.p_sender, self.p_receiver, self.p_amount)

    def test_db_connection_timeout(self):
        import unittest.mock
        with unittest.mock.patch('your_file.engine') as engine:
            engine.connect.side_effect = psycopg2 OperationalError('connection timeout')
            with self.assertRaises(psycopg2.OperationalError):
                process_payment(self.p_sender, self.p_receiver, self.p_amount)

if __name__ == '__main__':
    unittest.main()
