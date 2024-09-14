
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_credit_score  # replace 'your_module' with the actual module name
from config import engine

class TestCalculateCreditScore(unittest.TestCase):

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_valid(self, mock_connect):
        mock_result = Mock()
        mock_result.fetchall.return_value = [100.0, 50.0, 500.0, 10000.0, 5]

        mock_connect.return_value = mock_result
        
        result = calculate_credit_score(1)
        self.assertEqual(result, 550)
        
    @patch('your_module.engine.connect')
    def test_calculate_credit_score_missing_loans(self, mock_connect):
        mock_result = Mock()
        mock_result.fetchall.return_value = [0, 0, 0, 0, 0]

        mock_connect.return_value = mock_result
        
        result = calculate_credit_score(1)
        self.assertEqual(result, 700)
        
    @patch('your_module.engine.connect')
    def test_calculate_credit_score_no_data(self, mock_connect):
        mock_result = Mock()
        mock_result.fetchall.return_value = None

        mock_connect.return_value = mock_result

        with self.assertRaises(ValueError):
            calculate_credit_score(1)
            
    @patch('your_module.engine.connect')
    def test_calculate_credit_score_invalid_credit_score(self, mock_connect):
        mock_result = Mock()
        mock_result.fetchall.return_value = [1000.0, 50.0, 500.0, 10000.0, 5]

        mock_connect.return_value = mock_result
        
        result = calculate_credit_score(1)
        self.assertEqual(result, 850)
        
    @patch('your_module.engine.connect')
    def test_calculate_credit_score_multiple_rows(self, mock_connect):
        with self.assertRaises(ValueError):
            calculate_credit_score(1)

if __name__ == '__main__':
    unittest.main()
