
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_credit_score  # replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = Mock(fetchone=Mock(return_value=(1000, 800, 200)))
        mock_conn.execute.side_effect = [
            Mock(fetchone=Mock(return_value=(1000, 800, 200))),
            Mock(fetchone=Mock(return_value=(500,))),
            Mock(fetchone=Mock(return_value=(2,))),
        ]

        result = calculate_credit_score(1)
        self.assertEqual(result, 740)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_loans(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = Mock(fetchone=Mock(return_value=(0, 0, 0)))
        mock_conn.execute.side_effect = [
            Mock(fetchone=Mock(return_value=(0, 0, 0))),
            Mock(fetchone=Mock(return_value=(500,))),
            Mock(fetchone=Mock(return_value=(0,))),
        ]

        result = calculate_credit_score(1)
        self.assertEqual(result, 700)

    @patch('your_module.engine')
    def test_calculate_credit_score_no_credit_card(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = Mock(fetchone=Mock(return_value=(1000, 800, 200)))
        mock_conn.execute.side_effect = [
            Mock(fetchone=Mock(return_value=(1000, 800, 200))),
            Mock(fetchone=Mock(return_value=(None,))),
            Mock(fetchone=Mock(return_value=(2,))),
        ]

        result = calculate_credit_score(1)
        self.assertEqual(result, 740)

    @patch('your_module.engine')
    def test_calculate_credit_score_late_payments(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.return_value = Mock(fetchone=Mock(return_value=(1000, 800, 200)))
        mock_conn.execute.side_effect = [
            Mock(fetchone=Mock(return_value=(1000, 800, 200))),
            Mock(fetchone=Mock(return_value=(500,))),
            Mock(fetchone=Mock(return_value=(5,))),
        ]

        result = calculate_credit_score(1)
        self.assertEqual(result, 590)

    @patch('your_module.engine')
    def test_calculate_credit_score_db_error(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_conn.execute.side_effect = psycopg2.Error('Test error')

        result = calculate_credit_score(1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
