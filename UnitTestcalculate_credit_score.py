
import unittest
from unittest.mock import patch, Mock
from sqlalchemy import create_engine
from your_module import calculate_credit_score  # replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def setUp(self, mock_engine):
        self.mock_engine = mock_engine
        self.customer_id = 123

    @patch('your_module.engine.execute')
    def test_calculate_credit_score(self, mock_execute):
        # Test case 1: Total loan amount, total repayment, and outstanding balance
        mock_execute.return_value = [(1000, 500, 300)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 700)

        # Test case 2: Credit card balance
        mock_execute.return_value = [(200)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 700)

        # Test case 3: Late payments
        mock_execute.return_value = [(2)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 500)

        # Test case 4: Total loan amount is 0
        mock_execute.return_value = [(0, 0, 0)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 700)

        # Test case 5: Credit card balance is 0
        mock_execute.return_value = [(0)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 700)

        # Test case 6: Late payments count is 0
        mock_execute.return_value = [(0)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 700)

        # Test case 7: Credit score is less than 300
        mock_execute.return_value = [(1000, 0, 0), (0), (0)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 300)

        # Test case 8: Credit score is greater than 850
        mock_execute.return_value = [(0, 1000, 0), (0), (0)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 850)

        # Test case 9: Credit score is between 300 and 850
        mock_execute.return_value = [(500, 500, 0), (200), (1)]
        result = calculate_credit_score(self.customer_id)
        self.assertEqual(result, 550)

if __name__ == '__main__':
    unittest.main()
