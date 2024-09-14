
import unittest
from unittest.mock import patch, MagicMock
from psycopg2 import ProgrammingError
from sqlalchemy.exc import DBAPIError
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score(self, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = (1000, 500, 500)
        mock_conn.execute.return_value.fetchone.return_value = (100,)
        mock_conn.execute.return_value.fetchone.return_value = (2,)
        
        result = calculate_credit_score(1)
        self.assertIsInstance(result, int)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_loans(self, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = (0, 0, 0)
        mock_conn.execute.return_value.fetchone.return_value = (100,)
        mock_conn.execute.return_value.fetchone.return_value = (2,)
        
        result = calculate_credit_score(1)
        self.assertIsInstance(result, int)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_credit_card(self, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = (1000, 500, 500)
        mock_conn.execute.return_value.fetchone.return_value = (None,)
        mock_conn.execute.return_value.fetchone.return_value = (2,)
        
        result = calculate_credit_score(1)
        self.assertIsInstance(result, int)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_late_payments(self, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = (1000, 500, 500)
        mock_conn.execute.return_value.fetchone.return_value = (100,)
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = calculate_credit_score(1)
        self.assertIsInstance(result, int)

    @patch('your_module.engine')
    def test_calculate_credit_score_db_error(self, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_conn.execute.side_effect = ProgrammingError('Mocked DB error')
        
        with self.assertRaises(ProgrammingError):
            calculate_credit_score(1)

    @patch('your_module.engine')
    def test_calculate_credit_score_sqlalchemy_error(self, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_conn.execute.side_effect = DBAPIError('Mocked SQLAlchemy error', '', '')
        
        with self.assertRaises(DBAPIError):
            calculate_credit_score(1)

if __name__ == '__main__':
    unittest.main()
