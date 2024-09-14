
import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy import text
import pandas as pd
import psycopg2
from your_module import transfer_amount  # Replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    @patch('your_module.engine')
    def test_transfer_amount_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = [(1, 100), (2, 200)]
        p_amount = 50
        p_sender = 1
        p_receiver = 2
        result = transfer_amount(p_amount, p_sender, p_receiver)
        self.assertEqual(result.shape[0], 2)
        self.assertEqual(result.loc[0, 'id'], p_sender)
        self.assertEqual(result.loc[0, 'balance'], 50)
        self.assertEqual(result.loc[1, 'id'], p_receiver)
        self.assertEqual(result.loc[1, 'balance'], 250)

    @patch('your_module.engine')
    def test_transfer_amount_insufficient_funds(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = [(1, 0), (2, 200)]
        p_amount = 50
        p_sender = 1
        p_receiver = 2
        with self.assertRaises(psycopg2.Error):
            transfer_amount(p_amount, p_sender, p_receiver)

    @patch('your_module.engine')
    def test_transfer_amount_invalid_sender(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = []  # Sender not found
        p_amount = 50
        p_sender = 1
        p_receiver = 2
        with self.assertRaises(psycopg2.Error):
            transfer_amount(p_amount, p_sender, p_receiver)

    @patch('your_module.engine')
    def test_transfer_amount_invalid_receiver(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = [(1, 100)]  # Receiver not found
        p_amount = 50
        p_sender = 1
        p_receiver = 2
        with self.assertRaises(psycopg2.Error):
            transfer_amount(p_amount, p_sender, p_receiver)

    @patch('your_module.engine')
    def test_transfer_amount_db_error(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.side_effect = psycopg2.Error('DB error')
        p_amount = 50
        p_sender = 1
        p_receiver = 2
        with self.assertRaises(psycopg2.Error):
            transfer_amount(p_amount, p_sender, p_receiver)

if __name__ == '__main__':
    unittest.main()
