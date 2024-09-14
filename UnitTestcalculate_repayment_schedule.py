
import unittest
from unittest.mock import patch, Mock
from generate_repayment_schedule import generate_repayment_schedule
import pandas as pd

class TestGenerateRepaymentSchedule(unittest.TestCase):

    @patch('generate_repayment_schedule.engine')
    def test_generate_repayment_schedule(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 5, 12, '2022-01-01')
        mock_conn.execute.return_value = mock_result
        result = generate_repayment_schedule(1)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 12)

    @patch('generate_repayment_schedule.engine')
    def test_generate_repayment_schedule_zero_loan_term(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 5, 0, '2022-01-01')
        mock_conn.execute.return_value = mock_result
        result = generate_repayment_schedule(1)
        self.assertIsNone(result)

    @patch('generate_repayment_schedule.engine')
    def test_generate_repayment_schedule_null_loan_details(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result
        with self.assertRaises(TypeError):
            generate_repayment_schedule(1)

    @patch('generate_repayment_schedule.engine')
    def test_generate_repayment_schedule_invalid_loan_id(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result
        result = generate_repayment_schedule(-1)
        self.assertIsNone(result)

    @patch('generate_repayment_schedule.engine')
    def test_generate_repayment_schedule_non_numeric_loan_id(self, mock_engine):
        with self.assertRaises(TypeError):
            generate_repayment_schedule('a')

if __name__ == '__main__':
    unittest.main()
