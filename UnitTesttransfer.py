
import unittest
from your_module import transfer_amount
from psycopg2 import OperationalError 
from unittest.mock import patch

class TestTransferAmount(unittest.TestCase):

    @patch('config.engine.connect')
    @patch('your_module.engine')
    @patch('psycopg2.connect')
    def test_transfer_amount(self, mock_engine, mock_psql, mock_conn):
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None

        transfer_amount(1, 2, 100)

    @patch('config.engine.connect')
    @patch('your_module.engine')
    @patch('psycopg2.connect')
    def test_transfer_amount_with OperationalError(self, mock_engine, mock_psql, mock_conn):
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.side_effect = OperationalError('database operation failed')
        with self.assertRaises(OperationalError):
            transfer_amount(1, 2, 100)

    def test_transfer_amount_with_invalid_sender_id(self):
        with self.assertRaises(KeyError):
            transfer_amount('abc', 2, 100)

    def test_transfer_amount_with_invalid_receiver_id(self):
        with self.assertRaises(KeyError):
            transfer_amount(1, 'def', 100)

    def test_transfer_amount_with_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            transfer_amount(1, 2, 'abc')

    def test_transfer_amount_without_commit(self):
        conn = engine.connect()
        query = text("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        conn.execute(query, {'p_sender': 1, 'p_amount': 100})
        conn.close()
        with self.assertRaises(UncommittedResultError):
            transfer_amount(1, 2, 100)

if __name__ == '__main__':
    unittest.main()
