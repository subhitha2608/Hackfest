Python
import unittest
from unittest.mock import patch, Mock
from config import engine
import pandas as pd
from sqlalchemy import text
import psycopg2

class TestTransaction(unittest.TestCase):

    @patch('config.engine.connect')
    def test_transaction_success(self, mock_connect):
        result = mock_connect.return_value
        result.execute.return_value = Mock.fetchall.return_value = [{"id": 1, "balance": 100.0}, {"id": 2, "balance": 100.0}]
        mock_connect.return_value.close.return_value = None
        result.execute.return_value.rowcount = 2
        result.close.return_value = None
        
        tester = transaction(1, 2, 100.0)
        self.assertEqual(tester, [{"id": 1, "balance": 100.0}, {"id": 2, "balance": 100.0}])
        
    @patch('config.engine.connect')
    def test_transaction_error(self, mock_connect):
        result = mock_connect.return_value
        result.execute.side_effect = psycopg2.Error('Database error')
        mock_connect.return_value.close.return_value = None
        with self.assertRaises(psycopg2.Error):
            transaction(1, 2, 100.0)
        
    @patch('config.engine.connect')
    def test_transaction_zero_sent(self, mock_connect):
        result = mock_connect.return_value
        result.execute.return_value = Mock.fetchall.return_value = [{"id": 1, "balance": 1000.0}, {"id": 2, "balance": 1000.0}]
        mock_connect.return_value.close.return_value = None
        result.execute.return_value.rowcount = 2
        result.close.return_value = None
        
        tester = transaction(1, 2, 1000.0)
        self.assertEqual(tester, [{"id": 1, "balance": 1000.0}, {"id": 2, "balance": 1000.0}])
        
    @patch('config.engine.connect')
    def test_transaction_zero_recieved(self, mock_connect):
        result = mock_connect.return_value
        result.execute.side_effect = psycopg2.Error('Database error')
        mock_connect.return_value.close.return_value = None
        with self.assertRaises(psycopg2.Error):
            transaction(1, 2, -100.0)
        
    @patch('config.engine.connect')
    def test_transaction_large_amount(self, mock_connect):
        result = mock_connect.return_value
        result.execute.return_value = Mock.fetchall.return_value = [{"id": 1, "balance": 1000.0}, {"id": 2, "balance": 1000.0}]
        mock_connect.return_value.close.return_value = None
        result.execute.return_value.rowcount = 2
        result.close.return_value = None
        
        tester = transaction(1, 2, 10000.0)
        self.assertEqual(tester, [{"id": 1, "balance": 0.0}, {"id": 2, "balance": 10000.0}])
        
    @patch('config.engine.connect')
    def test_transaction_negative_amount(self, mock_connect):
        result = mock_connect.return_value
        result.execute.side_effect = psycopg2.Error('Database error')
        mock_connect.return_value.close.return_value = None
        with self.assertRaises(psycopg2.Error):
            transaction(1, 2, -10.0)

if __name__ == '__main__':
    unittest.main()
