
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = MagicMock(fetchone=MagicMock(return_value=(1000.0, 800.0, 200.0)))
        mock_conn.execute.return_value.fetchone.return_value = (100.0,)
        mock_conn.execute.return_value.fetchone.return_value = (2,)

        result = calculate_credit_score(1)
        self.assertEqual(result, 740)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_loans(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = MagicMock(fetchone=MagicMock(return_value=(0.0, 0.0, 0.0)))
        mock_conn.execute.return_value.fetchone.return_value = (100.0,)
        mock_conn.execute.return_value.fetchone.return_value = (2,)

        result = calculate_credit_score(1)
        self.assertEqual(result, 650)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_credit_card(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = MagicMock(fetchone=MagicMock(return_value=(1000.0, 800.0, 200.0)))
        mock_conn.execute.return_value.fetchone.return_value = (0.0,)
        mock_conn.execute.return_value.fetchone.return_value = (2,)

        result = calculate_credit_score(1)
        self.assertEqual(result, 740)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_late_payments(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = MagicMock(fetchone=MagicMock(return_value=(1000.0, 800.0, 200.0)))
        mock_conn.execute.return_value.fetchone.return_value = (100.0,)
        mock_conn.execute.return_value.fetchone.return_value = (0,)

        result = calculate_credit_score(1)
        self.assertEqual(result, 790)

    @patch('your_module.engine')
    def test_calculate_credit_score_db_error(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.side_effect = psycopg2.Error()

        result = calculate_credit_score(1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
