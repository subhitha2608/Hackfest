
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.psycopg2')
    def test_calculate_credit_score(self, mock-psycopg2, mock_engine):
        # Test case 1: Positive score for a customer with no loans or credit cards
        customer_id = 123
        mock_result = Mock()
        mock_result.fetchone.return_value = (0, 0, 0)
        mock_engine.connect.return_value.execute.return_value = mock_result
        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 400)

        # Test case 2: Positive score for a customer with loans and credit cards
        customer_id = 456
        mock_result = Mock()
        mock_result.fetchone.side_effect = [(100, 50, 20), 100]
        mock_engine.connect.return_value.execute.return_value = mock_result
        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 800)

        # Test case 3: Negative score for a customer with late payments
        customer_id = 789
        mock_result = Mock()
        mock_result.fetchone.return_value = (10, 20, 30)
        mock_result.fetchone.return_value = 5
        mock_engine.connect.return_value.execute.return_value = mock_result
        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 350)

        # Test case 4: Error handling for database connection error
        customer_id = 123
        mock_engine.connect.side_effect = psycopg2.Error('mock error')
        result = calculate_credit_score(customer_id)
        self.assertEqual(result, None)

        # Test case 5: Error handling for query error
        customer_id = 456
        mock_result = Mock()
        mock_result.fetchone.side_effect = psycopg2.Error('mock error')
        mock_engine.connect.return_value.execute.return_value = mock_result
        result = calculate_credit_score(customer_id)
        self.assertEqual(result, None)

        # Test case 6: Log the result for a customer with a low score
        customer_id = 789
        mock_log_result = Mock()
        mock_engine.connect.return_value.execute.return_value = mock_log_result
        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 350)

if __name__ == '__main__':
    unittest.main()
