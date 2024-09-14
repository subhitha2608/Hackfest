
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score(self, mock_engine):
        # Test case 1: Happy path
        mock_engine.execute.return_value = [
            (1000.00, 800.00, 200.00),  # Loan amounts
            (500.00,),  # Credit card balance
            (1,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 630)

        # Test case 2: No loans
        mock_engine.execute.return_value = [
            (0.00, 0.00, 0.00),  # Loan amounts
            (500.00,),  # Credit card balance
            (1,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 430)

        # Test case 3: No credit card balance
        mock_engine.execute.return_value = [
            (1000.00, 800.00, 200.00),  # Loan amounts
            (0.00,),  # Credit card balance
            (1,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 630)

        # Test case 4: No late payments
        mock_engine.execute.return_value = [
            (1000.00, 800.00, 200.00),  # Loan amounts
            (500.00,),  # Credit card balance
            (0,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 680)

        # Test case 5: Edge case - extremely high credit card balance
        mock_engine.execute.return_value = [
            (1000.00, 800.00, 200.00),  # Loan amounts
            (99999.00,),  # Credit card balance
            (1,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 300)

        # Test case 6: Edge case - extremely high loan amounts
        mock_engine.execute.return_value = [
            (99999.00, 800.00, 200.00),  # Loan amounts
            (500.00,),  # Credit card balance
            (1,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 850)

        # Test case 7: Edge case - extremely high late payment count
        mock_engine.execute.return_value = [
            (1000.00, 800.00, 200.00),  # Loan amounts
            (500.00,),  # Credit card balance
            (20,)  # Late payment count
        ]
        result = calculate_credit_score(1)
        self.assertEqual(result, 300)

        # Test case 8: Error handling - database error
        mock_engine.execute.side_effect = psycopg2.Error
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(1)

if __name__ == '__main__':
    unittest.main()
