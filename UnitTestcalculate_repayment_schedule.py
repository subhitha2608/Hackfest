
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_repayment_schedule  # replace with your module name
import pandas as pd
import numpy as np

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_repayment_schedule_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchone.return_value = (1000, 5, 12, pd.to_datetime('2022-01-01'))
        
        calculate_repayment_schedule(1)
        
        self.assertEqual(mock_conn.execute.call_count, 13)  # 1 for loan details, 12 for repayment schedule
        mock_engine.connect.assert_called_with()
        mock_conn.commit.assert_called_with()
        
    @patch('your_module.engine')
    def test_calculate_repayment_schedule_loan_id_not_found(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchone.return_value = None
        
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)
        
        self.assertEqual(mock_conn.execute.call_count, 1)  # only for loan details
        mock_engine.connect.assert_called_with()
        mock_conn.commit.assert_not_called()
        
    @patch('your_module.engine')
    def test_calculate_repayment_schedule_loan_terms_invalid(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchone.return_value = (1000, -5, 12, pd.to_datetime('2022-01-01'))
        
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)
        
        self.assertEqual(mock_conn.execute.call_count, 1)  # only for loan details
        mock_engine.connect.assert_called_with()
        mock_conn.commit.assert_not_called()
        
    @patch('your_module.engine')
    def test_calculate_repayment_schedule_loan_term_zero(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchone.return_value = (1000, 5, 0, pd.to_datetime('2022-01-01'))
        
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(1)
        
        self.assertEqual(mock_conn.execute.call_count, 1)  # only for loan details
        mock_engine.connect.assert_called_with()
        mock_conn.commit.assert_not_called()
        
if __name__ == '__main__':
    unittest.main()
