
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_repayment_schedule
import pandas as pd
from sqlalchemy import text
from psycopg2 import Error

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine')
    @patch('your_module.pd')
    def test_calculate_repayment_schedule(self, mock_pd, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = mock_engine
        mock_engine.execute.return_value.fetchone.return_value = (1000, 5, 12, pd.Timestamp('2022-01-01'))
        mock_pd.DateOffset.return_value = pd.DateOffset(months=1)
        
        calculate_repayment_schedule(1)
        
        mock_engine.execute.assert_called()
        mock_engine.commit.assert_called()
        mock_engine.close.assert_called()
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    def test_calculate_repayment_schedule_no_loan_found(self, mock_pd, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = mock_engine
        mock_engine.execute.return_value.fetchone.return_value = None
        
        result = calculate_repayment_schedule(1)
        
        self.assertIsNone(result)
        mock_engine.close.assert_called()
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    def test_calculate_repayment_schedule_psycopg2_error(self, mock_pd, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = mock_engine
        mock_engine.execute.side_effect = Error
        
        result = calculate_repayment_schedule(1)
        
        self.assertEqual(result, "Error occurred: ")
        mock_engine.close.assert_called()
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    def test_calculate_repayment_schedule_loan_term_zero(self, mock_pd, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = mock_engine
        mock_engine.execute.return_value.fetchone.return_value = (1000, 5, 0, pd.Timestamp('2022-01-01'))
        
        result = calculate_repayment_schedule(1)
        
        self.assertEqual(result, "Repayment schedule calculated successfully")
        mock_engine.close.assert_called()
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    def test_calculate_repayment_schedule_loan_term_negative(self, mock_pd, mock_engine):
        mock_engine.connect.return_value.__enter__.return_value = mock_engine
        mock_engine.execute.return_value.fetchone.return_value = (1000, 5, -12, pd.Timestamp('2022-01-01'))
        
        result = calculate_repayment_schedule(1)
        
        self.assertEqual(result, "Repayment schedule calculated successfully")
        mock_engine.close.assert_called()

if __name__ == '__main__':
    unittest.main()
