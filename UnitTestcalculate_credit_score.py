
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_credit_score
import pandas as pd
import psycopg2

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score_happy_path(self, mock_engine):
        customer_id = 1
        mock_engine.raw_connection.return_value = MagicMock()
        mock_connection = mock_engine.raw_connection.return_value
        mock_connection.cursor.return_value = MagicMock()
        mock_cursor = mock_connection.cursor.return_value

        # Mock query results
        mock_cursor.fetchone.return_value = (1000.0, 800.0, 200.0)
        mock_cursor.fetchone.return_value = (500.0,)
        mock_cursor.fetchone.return_value = (2,)

        # Run the function
        credit_score = calculate_credit_score(customer_id)

        # Asserts
        self.assertEqual(credit_score, 650)
        mock_engine.execute.assert_called()
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_calculate_credit_score_no_loans(self, mock_engine):
        customer_id = 1
        mock_engine.raw_connection.return_value = MagicMock()
        mock_connection = mock_engine.raw_connection.return_value
        mock_connection.cursor.return_value = MagicMock()
        mock_cursor = mock_connection.cursor.return_value

        # Mock query results
        mock_cursor.fetchone.return_value = (None, None, None)
        mock_cursor.fetchone.return_value = (500.0,)
        mock_cursor.fetchone.return_value = (2,)

        # Run the function
        credit_score = calculate_credit_score(customer_id)

        # Asserts
        self.assertEqual(credit_score, 500)
        mock_engine.execute.assert_called()
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_calculate_credit_score_no_credit_card(self, mock_engine):
        customer_id = 1
        mock_engine.raw_connection.return_value = MagicMock()
        mock_connection = mock_engine.raw_connection.return_value
        mock_connection.cursor.return_value = MagicMock()
        mock_cursor = mock_connection.cursor.return_value

        # Mock query results
        mock_cursor.fetchone.return_value = (1000.0, 800.0, 200.0)
        mock_cursor.fetchone.return_value = (None,)
        mock_cursor.fetchone.return_value = (2,)

        # Run the function
        credit_score = calculate_credit_score(customer_id)

        # Asserts
        self.assertEqual(credit_score, 650)
        mock_engine.execute.assert_called()
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_calculate_credit_score_no_late_payments(self, mock_engine):
        customer_id = 1
        mock_engine.raw_connection.return_value = MagicMock()
        mock_connection = mock_engine.raw_connection.return_value
        mock_connection.cursor.return_value = MagicMock()
        mock_cursor = mock_connection.cursor.return_value

        # Mock query results
        mock_cursor.fetchone.return_value = (1000.0, 800.0, 200.0)
        mock_cursor.fetchone.return_value = (500.0,)
        mock_cursor.fetchone.return_value = (0,)

        # Run the function
        credit_score = calculate_credit_score(customer_id)

        # Asserts
        self.assertEqual(credit_score, 700)
        mock_engine.execute.assert_called()
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_calculate_credit_score_exception(self, mock_engine):
        customer_id = 1
        mock_engine.raw_connection.return_value = MagicMock()
        mock_connection = mock_engine.raw_connection.return_value
        mock_connection.cursor.return_value = MagicMock()
        mock_cursor = mock_connection.cursor.return_value

        # Mock query results
        mock_cursor.fetchone.side_effect = psycopg2.Error('Error')

        # Run the function
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

        # Asserts
        mock_engine.execute.assert_called()
        mock_connection.rollback.assert_called()
        mock_connection.close.assert_called()

if __name__ == '__main__':
    unittest.main()
