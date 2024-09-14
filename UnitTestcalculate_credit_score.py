
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_credit_score  # replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.psycopg2')
    def test_calculate_credit_score(self, mock_psycopg2, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1000, 800, 200)

        mock_cursor2 = MagicMock()
        mock_conn.execute.return_value = mock_cursor2
        mock_cursor2.fetchone.return_value = (500,)

        mock_cursor3 = MagicMock()
        mock_conn.execute.return_value = mock_cursor3
        mock_cursor3.fetchone.return_value = (2,)

        customer_id = 123
        result = calculate_credit_score(customer_id)
        self.assertIsNotNone(result)

        # Test with no loans
        mock_cursor.fetchone.return_value = (None, None, None)
        result = calculate_credit_score(customer_id)
        self.assertIsNotNone(result)

        # Test with no credit card balance
        mock_cursor2.fetchone.return_value = (None,)
        result = calculate_credit_score(customer_id)
        self.assertIsNotNone(result)

        # Test with no late payments
        mock_cursor3.fetchone.return_value = (0,)
        result = calculate_credit_score(customer_id)
        self.assertIsNotNone(result)

        # Test with error
        mock_psycopg2.Error = Exception('Error')
        with self.assertRaises(Exception):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
