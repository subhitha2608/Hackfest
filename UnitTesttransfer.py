
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_funds  # Replace 'your_module' with the actual module name
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

class TestTransferFunds(unittest.TestCase):

    @patch('your_module.engine')
    def test_transfer_funds_success(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = 100

        transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_failure(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = 100
        mock_conn.execute.side_effect = psycopg2.Error()

        with self.assertRaises(psycopg2.Error):
            transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.rollback.assert_called()
        mock_conn.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_sender_receiver_same(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 1
        p_amount = 100

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.rollback.assert_not_called()
        mock_conn.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_amount_zero(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = 0

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.rollback.assert_not_called()
        mock_conn.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_amount_negative(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = -100

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.rollback.assert_not_called()
        mock_conn.close.assert_called()

if __name__ == '__main__':
    unittest.main()
