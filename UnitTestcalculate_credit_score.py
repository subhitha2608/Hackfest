
import unittest
from unittest.mock import patch, Mock

class TestCalculateCreditScore(unittest.TestCase):

    @patch('config.engine')
    @patch('psycopg2.connect')
    @patch('pandas.DataFrame')
    def test_calculate_credit_score(self, mock_pandas_df, mock_connect, mock_config_engine):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (100, 50, 20)
        mock_cursor.execute.return_value = mock_cursor
        mock_connect.return_value = mock_cursor
        mock_df = Mock()
        mock_pandas_df.return_value = mock_df
        mock_engine = Mock()
        mock_engine.connect.return_value = mock_cursor
        mock_config_engine.return_value = mock_engine

        self.assertEqual(calculate_credit_score(1), 600)

    @patch('config.engine')
    @patch('psycopg2.connect')
    @patch('pandas.DataFrame')
    def test_calculate_credit_score_no_loans(self, mock_pandas_df, mock_connect, mock_config_engine):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (0, 0, 0)
        mock_cursor.execute.return_value = mock_cursor
        mock_connect.return_value = mock_cursor
        mock_df = Mock()
        mock_pandas_df.return_value = mock_df
        mock_engine = Mock()
        mock_engine.connect.return_value = mock_cursor
        mock_config_engine.return_value = mock_engine

        self.assertEqual(calculate_credit_score(1), 700)

    @patch('config.engine')
    @patch('psycopg2.connect')
    @patch('pandas.DataFrame')
    def test_calculate_credit_score_no_credit_card(self, mock_pandas_df, mock_connect, mock_config_engine):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (100, 50, 20)
        mock_cursor.execute.return_value = mock_cursor
        mock_connect.return_value = mock_cursor
        mock_df = Mock()
        mock_pandas_df.return_value = mock_df
        mock_engine = Mock()
        mock_engine.connect.return_value = mock_cursor
        mock_config_engine.return_value = mock_engine

        self.assertEqual(calculate_credit_score(1), 700)

    @patch('config.engine')
    @patch('psycopg2.connect')
    @patch('pandas.DataFrame')
    def test_calculate_credit_score_late_payments(self, mock_pandas_df, mock_connect, mock_config_engine):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (100, 50, 20)
        mock_cursor.execute.return_value = mock_cursor
        mock_connect.return_value = mock_cursor
        mock_df = Mock()
        mock_pandas_df.return_value = mock_df
        mock_engine = Mock()
        mock_engine.connect.return_value = mock_cursor
        mock_config_engine.return_value = mock_engine

        self.assertEqual(calculate_credit_score(1), 550)

    @patch('config.engine')
    @patch('psycopg2.connect')
    @patch('pandas.DataFrame')
    def test_calculate_credit_score_update_customer(self, mock_pandas_df, mock_connect, mock_config_engine):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (100, 50, 20)
        mock_cursor.execute.return_value = mock_cursor
        mock_connect.return_value = mock_cursor
        mock_df = Mock()
        mock_pandas_df.return_value = mock_df
        mock_engine = Mock()
        mock_engine.connect.return_value = mock_cursor
        mock_config_engine.return_value = mock_engine
        
        calculate_credit_score(1)
        
        mock_cursor.execute.assert_called_once_with(text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """), {"p_customer_id": 1, "v_credit_score": 600})

if __name__ == '__main__':
    unittest.main()
